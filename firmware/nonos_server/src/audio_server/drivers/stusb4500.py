#!/usr/bin/env python3
"""STUSB4500 USB Type-C Power Delivery Controller Driver.

https://github.com/timkruse/stusb4500/tree/master/sw

USB Type C Evaluation Board based on STUSB4500 by STM.

This project implements the USB Type C connector based on the STM's STUSB4500 USB Power Delivery controller.
All signals are either routed to the dedicated USB connector or to an external connector to access signals such as I2C
which is the config interface of the STUSB4500.
The power lines are controlled by FETs to suit the 100W specification of USB-C.

Original 2019 by Tim Kruse
Modified 2023 by Patrick Wallner aka MCPat

Modifications:
1. Adapted code to run with Python3
2. Adapted NVM to work with new power supply from RPi5 (5V 5A)
3. Uncommented some comments in set_pdo
4. Bugfix in set_pdo_variable

GUI for NVM can be found at https://github.com/usb-c/STUSB4500/blob/master/GUI/App/STSW-STUSB002%20v1.0.8.zip
"""

import subprocess
from dataclasses import dataclass
from time import sleep

from smbus2 import SMBus


@dataclass
class Version:
    """USB Type-C and USB PD revision information."""

    typec_rev: int
    usbpd_rev: int

    def __str__(self):
        return (
            f"Version(typec_rev={hex(self.typec_rev)}, usbpd_rev={hex(self.usbpd_rev)})"
        )

    __repr__ = __str__


@dataclass
class PortStatus:
    """Port connection status information."""

    stateChanged: int
    attachedDevice: int
    lowPowerStandby: int
    powerMode: int
    dataMode: int
    attached: int

    def __str__(self):
        attachedDeviceAsString = [
            "None",
            "Sink",
            "Source",
            "Debug Accessory",
            "Audio Accessory",
            "Power Accessory",
        ]
        return (
            f"PortStatus(stateChanged={'True' if self.stateChanged == 1 else 'False'}, "
            f"attachedDevice={attachedDeviceAsString[self.attachedDevice] if (self.attachedDevice >= 0 and self.attachedDevice <= 5) else f'undefined({self.attachedDevice})'}, "
            f"lowPowerStandby={'standby mode' if self.lowPowerStandby == 1 else 'normal mode'}, "
            f"powerMode={'Source' if self.powerMode == 1 else 'Sink'}, "
            f"dataMode={'DFP' if self.dataMode == 1 else 'UFP'}, "
            f"attached={'True' if self.attached == 1 else 'False'})"
        )

    __repr__ = __str__


@dataclass
class PDO_Contract:
    """Active Power Delivery Object contract number."""

    num: int


# Supply type strings used by PDO classes
supplyStr = ["Fixed", "Variable", "Battery"]


@dataclass
class PdoSinkFix:
    """Fixed voltage Power Delivery Object for sink."""

    current: int
    voltage: int
    fastRoleReqCur: int
    dualRoleData: int
    usbCommunicationsCapable: int
    unconstrainedPower: int
    higherCapability: int
    dualRolePower: int
    supply: int
    raw: int

    def __str__(self):
        return (
            f"PdoSink(voltage={self.voltage / 20.0}V, "
            f"current={self.current / 100.0}A, "
            f"fastRoleReqCur={self.fastRoleReqCur}, "
            f"dualRoleData={self.dualRoleData}, "
            f"usbCommunicationsCapable={self.usbCommunicationsCapable}, "
            f"unconstrainedPower={self.unconstrainedPower}, "
            f"higherCapability={self.higherCapability}, "
            f"dualRolePower={self.dualRolePower}, "
            f"supply={supplyStr[self.supply] if self.supply >= 0 and self.supply < 3 else 'Undefined'}, "
            f"raw=0x{self.raw:08x})"
        )

    __repr__ = __str__


@dataclass
class PdoSinkVar:
    """Variable voltage Power Delivery Object for sink."""

    min_voltage: int
    max_voltage: int
    current: int
    supply: int
    raw: int

    def __str__(self):
        return (
            f"PdoSink(voltage=[{self.min_voltage / 20.0}V-{self.max_voltage / 20.0}V], "
            f"current={self.current / 100.0}A, "
            f"supply={supplyStr[self.supply] if self.supply >= 0 and self.supply < 3 else 'Undefined'}, "
            f"raw=0x{self.raw:08x})"
        )

    __repr__ = __str__


@dataclass
class PdoSinkBat:
    """Battery Power Delivery Object for sink."""

    min_voltage: int
    max_voltage: int
    power: int
    supply: int
    raw: int

    def __str__(self):
        return (
            f"PdoSink(voltage=[{self.min_voltage / 20.0}V-{self.max_voltage / 20.0}V], "
            f"power={self.power}W, "
            f"supply={supplyStr[self.supply] if self.supply >= 0 and self.supply < 3 else 'Undefined'}, "
            f"raw=0x{self.raw:08x})"
        )

    __repr__ = __str__


@dataclass
class Rdo:
    """Requested Data Object containing negotiated power parameters."""

    voltage: float
    current: int
    maxCurrent: int
    unchunkedMess_sup: int
    usbSuspend: int
    usbComCap: int
    capaMismatch: int
    giveBack: int
    objectPos: int
    raw: int

    def __str__(self):
        return (
            f"RDO(voltage={self.voltage}V, "
            f"current={self.current / 100.0}A, "
            f"maxCurrent={self.maxCurrent / 100.0}A, "
            f"unchunkedMess_sup={self.unchunkedMess_sup}, "
            f"usbSuspend={self.usbSuspend}, "
            f"usbComCap={self.usbComCap}, "
            f"capaMismatch={self.capaMismatch}, "
            f"giveBack={self.giveBack}, "
            f"objectPos={self.objectPos}, "
            f"raw=0x{self.raw:08x})"
        )

    __repr__ = __str__


@dataclass
class Vbus:
    """VBUS control and discharge configuration."""

    discharge_0v: int
    discharge_trans: int
    vbus_discharge: bool
    vsrc_discharge: bool
    sink_vbus_en: bool

    def __str__(self):
        return (
            f"VBUS(discharge_time_transition={self.discharge_trans * 24}ms, "
            f"discharge_to_0V={self.discharge_0v * 84}ms, "
            f"vbus_discharge={'Enabled' if self.vbus_discharge else 'Disabled'}, "
            f"vsrc_discharge={'Enabled' if self.vsrc_discharge else 'Disabled'}, "
            f"sink_vbus_en={'Enabled' if self.sink_vbus_en else 'Disabled'})"
        )

    __repr__ = __str__


class STUSB4500:
    """Driver for STUSB4500 USB Type-C Power Delivery Controller.

    This class provides methods to interact with the STUSB4500 chip via I2C,
    including reading status, configuring PDOs, and managing NVM.

    Args:
        i2c_bus: I2C bus number (default: 0).
        i2c_addr: I2C address of the chip (default: 0x28).
        reset_pin: GPIO pin number for hardware reset (default: 4).
    """

    def __init__(
        self, i2c_bus: SMBus, i2c_addr: int = 0x28, reset_pin: int | None = None
    ):
        self.addr = i2c_addr
        self.bus = i2c_bus
        self.reset_pin = reset_pin

    def _set_gpio_output(self, gpio: int, high: bool):
        """Set GPIO output state using pinctrl."""
        subprocess.check_output(["pinctrl", "set", str(gpio), "op"])
        subprocess.check_output(
            ["pinctrl", "set", str(gpio), f"d{'h' if high else 'l'}"]
        )

    def hard_reset(self):
        """Perform a hardware reset of the STUSB4500 chip using GPIO."""
        if self.reset_pin is None:
            raise ValueError("Reset pin is not set")

        self._set_gpio_output(self.reset_pin, True)
        sleep(0.2)
        self._set_gpio_output(self.reset_pin, False)

    def version(self):
        """Read Type-C and USB PD revision information from the chip.

        Returns:
            Version: Object containing typec_rev and usbpd_rev.
        """
        BCD_TYPEC_REV_LOW = self.bus.read_byte_data(self.addr, 0x06)
        BCD_TYPEC_REV_HIGH = self.bus.read_byte_data(self.addr, 0x07)
        typec_rev = BCD_TYPEC_REV_HIGH << 8 | BCD_TYPEC_REV_LOW

        BCD_USBPD_REV_LOW = self.bus.read_byte_data(self.addr, 0x08)
        BCD_USBPD_REV_HIGH = self.bus.read_byte_data(self.addr, 0x09)
        usbpd_rev = BCD_USBPD_REV_HIGH << 8 | BCD_USBPD_REV_LOW

        return Version(typec_rev=typec_rev, usbpd_rev=usbpd_rev)

    def port_status(self):
        """Read the current status of the USB Type-C port.

        Returns:
            PortStatus: Object containing port connection and power status.
        """
        PORT_STATUS_0 = self.bus.read_byte_data(self.addr, 0x0D)
        PORT_STATUS_1 = self.bus.read_byte_data(self.addr, 0x0E)

        return PortStatus(
            stateChanged=PORT_STATUS_0 & 0x01,
            attachedDevice=PORT_STATUS_1 >> 5 & 0x07,
            lowPowerStandby=PORT_STATUS_1 >> 4 & 0x01,
            powerMode=PORT_STATUS_1 >> 3 & 0x01,
            dataMode=PORT_STATUS_1 >> 2 & 0x01,
            attached=PORT_STATUS_1 & 0x01,
        )

    def active_contract(self):
        """Read the currently active PDO contract number.

        Returns:
            PDO_Contract: Object containing the active PDO number (0-3).
        """
        DPM_PDO_NUMB = self.bus.read_byte_data(self.addr, 0x70)
        return PDO_Contract(num=DPM_PDO_NUMB & 3)

    def set_active_contract(self, newValue):
        """Force the use of a specific PDO contract.

        The STUSB4500 offers 3 PDO contracts and changes take effect after a soft reset.

        Args:
            newValue: PDO contract number (0-3).
        """
        if newValue >= 0 and newValue < 4:
            return self.bus.write_byte_data(self.addr, 0x70, newValue)

    def read_pdo(self):
        """Read all currently configured PDOs from the chip.

        Note: REQ_SRC_CURRENT == unconstrainedPower

        Returns:
            dict: Dictionary with PDO numbers (1-3) as keys and PDO objects as values.
        """
        bvalues = []  # byte values
        for reg in range(0x85, 0x91):
            bvalues.append(self.bus.read_byte_data(self.addr, reg))

        pdo = {}
        for i in range(0, 3):
            reg = (
                bvalues[i * 4 + 3] << 24
                | bvalues[i * 4 + 2] << 16
                | bvalues[i * 4 + 1] << 8
                | bvalues[i * 4]
            )
            supply = reg >> 30 & 0x3
            if supply == 0:  #  fixed
                pdo[i + 1] = PdoSinkFix(
                    supply=supply,
                    dualRolePower=reg >> 29 & 0x1,
                    higherCapability=reg >> 28 & 0x1,
                    unconstrainedPower=reg >> 27 & 0x1,
                    usbCommunicationsCapable=reg >> 26 & 0x1,
                    dualRoleData=reg >> 25 & 0x1,
                    fastRoleReqCur=reg >> 23 & 0x3,
                    voltage=reg >> 10 & 0x3FF,
                    current=reg & 0x3FF,
                    raw=reg,
                )
            elif supply == 1:  # variable
                pdo[i + 1] = PdoSinkVar(
                    supply=supply,
                    max_voltage=reg >> 20 & 0x3FF,
                    min_voltage=reg >> 10 & 0x3FF,
                    current=reg & 0x3FF,
                    raw=reg,
                )
            elif supply == 2:  # battery
                pdo[i + 1] = PdoSinkBat(
                    supply=supply,
                    max_voltage=reg >> 20 & 0x3FF,
                    min_voltage=reg >> 10 & 0x3FF,
                    power=reg & 0x3FF,
                    raw=reg,
                )
        return pdo

    def print_pdo(self):
        """Read and print all Power Data Objects."""
        for k, v in self.read_pdo().items():
            print("PDO#" + str(k) + ": ", v)

    def read_rdo(self):
        """Read the Requested Data Object (RDO).

        Returns:
            Rdo: Object containing the negotiated power parameters.
        """
        bvalues = []  # byte values
        for reg in range(0x91, 0x95):
            bvalues.append(self.bus.read_byte_data(self.addr, reg))

        requested_voltage = self.bus.read_byte_data(self.addr, 0x21)  # *100mV
        requested_voltage /= 10.0  # I want it in Volt not milli volt

        reg = bvalues[3] << 24 | bvalues[2] << 16 | bvalues[1] << 8 | bvalues[0]
        return Rdo(
            voltage=requested_voltage,
            objectPos=reg >> 28 & 0x7,
            giveBack=reg >> 27 & 0x1,
            capaMismatch=reg >> 26 & 0x1,
            usbComCap=reg >> 25 & 0x1,
            usbSuspend=reg >> 24 & 0x1,
            unchunkedMess_sup=reg >> 23 & 0x1,
            current=reg >> 10 & 0x3FF,
            maxCurrent=reg & 0x3FF,
            raw=reg,
        )

    def reset(self):
        """Perform a software reset of the STUSB4500.

        Uses RESET_CTRL Register @0x23 bit 0 = {1 := reset, 0 := no reset}.
        """
        RESET_CTRL = self.bus.read_byte_data(self.addr, 0x23)
        self.bus.write_byte_data(self.addr, 0x23, RESET_CTRL | 0x01)
        sleep(0.25)
        self.bus.write_byte_data(self.addr, 0x23, RESET_CTRL & ~0x01)

    def set_pdo(self, num, volt, current):
        """Set a fixed voltage PDO configuration.

        Args:
            num: PDO number to configure (1-3).
            volt: Desired voltage in mV.
            current: Desired current in mA.
        """
        if num > 0 and num < 4:
            reg32 = (int(current / 10) & 0x3FF) | int(volt / 50) << 10 | (1 << 29)
            self.bus.write_byte_data(self.addr, 0x85 + (num - 1) * 4, reg32 & 0xFF)
            self.bus.write_byte_data(
                self.addr, 0x86 + (num - 1) * 4, (reg32 >> 8) & 0xFF
            )
            self.bus.write_byte_data(
                self.addr, 0x87 + (num - 1) * 4, (reg32 >> 16) & 0xFF
            )
            self.bus.write_byte_data(
                self.addr, 0x88 + (num - 1) * 4, (reg32 >> 24) & 0xFF
            )
        else:
            print(num, " is no valid pdo!")

    def set_pdo_variable(self, pdo_num, current, min_voltage, max_voltage):
        """Configure a PDO with variable voltage range.

        Args:
            pdo_num: PDO number to configure (2-3, PDO1 cannot be variable).
            current: Desired current in mA.
            min_voltage: Minimum voltage in mV (5000-20000).
            max_voltage: Maximum voltage in mV (5000-20000).
        """
        if pdo_num > 1 and pdo_num <= 3:
            if (
                min_voltage >= 5000
                and min_voltage <= 20000
                and max_voltage >= 5000
                and max_voltage <= 20000
                and min_voltage <= max_voltage
            ):
                reg32 = 1 << 30  # variable supply
                reg32 |= int(current / 10)
                reg32 |= int(min_voltage / 50) << 10  # min voltage
                reg32 |= int(max_voltage / 50) << 20  # max voltage

                self.bus.write_byte_data(
                    self.addr, 0x85 + (pdo_num - 1) * 4, reg32 & 0xFF
                )
                self.bus.write_byte_data(
                    self.addr, 0x86 + (pdo_num - 1) * 4, (reg32 >> 8) & 0xFF
                )
                self.bus.write_byte_data(
                    self.addr, 0x87 + (pdo_num - 1) * 4, (reg32 >> 16) & 0xFF
                )
                self.bus.write_byte_data(
                    self.addr, 0x88 + (pdo_num - 1) * 4, (reg32 >> 24) & 0xFF
                )
        elif pdo_num == 1:
            print("PDO#1 cannot have a variable supply")

    def nvm_lock(self, lock):
        """Lock or unlock the internal NVM registers.

        Args:
            lock: True to lock, False to unlock.
        """
        if lock is False:
            self.bus.write_byte_data(self.addr, 0x95, 0x47)
        else:
            self.bus.write_byte_data(self.addr, 0x95, 0x00)

    def nvm_dump(self):
        """Dump the contents of the NVM (Non-Volatile Memory).

        Factory NVM dump reference:
            00 00 b0 aa 00 45 00 00 (0xc0-0xc7 hidden)
            10 40 9c 1c ff 01 3c df (0xc8-0xcf)
            02 40 0f 00 32 00 fc f1 (0xd0-0xd7)
            00 19 56 af f5 35 5f 00 (0xd8-0xdf)
            00 4b 90 21 43 00 40 fb (0xe0-0xe7)
        """
        self.nvm_lock(False)  # unlock NVM

        def nvm_wait_for_execution():
            while True:
                reg8 = self.bus.read_byte_data(self.addr, 0x96)
                if reg8 & 0x10 == 0x00:
                    break

        sector_data = []
        for num_sector in range(0, 5):
            # send command opcode READ(0x00) to FTP_CTRL_1(0x97)
            self.bus.write_byte_data(self.addr, 0x97, 0 & 0x07)
            # execute command
            self.bus.write_byte_data(
                self.addr, 0x96, (num_sector & 0x07) | 0x80 | 0x40 | 0x10
            )
            nvm_wait_for_execution()
            # read 8 bytes that are copied from nvm to 0x53-0x5a
            sector = []
            for i in range(0, 8):
                sector.append(self.bus.read_byte_data(self.addr, 0x53 + i))
            sector_data.append(sector)
        self.nvm_lock(True)  # lock NVM

        # nicely print out the values
        sec = 0
        for sector in sector_data:
            line = f"{sec}: ["
            sec += 1
            for byte in sector:
                line += "0x" + format(byte, "02x") + ", "
            line = line[:-2]  # remove trailing comma
            line += "]"
            print(line)

    # Write procedure:
    # Enter Write mode:
    # 1. PASSWORD_REG(0x95) <= PASSWORD(0x47) to unlock flash
    # 2. RW_BUFFER(0x53) <= 0 if partial erasing sectors
    # 3. CTRL_0(0x96) <= PWR | RST_N to soft reset chip and power on
    # 4. CTRL_1(0x97) <= SECTORS_TOBE_ERASED_MASK << 3 | WRITE_SER to send erase command for the specified sectors (1 hot encoded)
    # 5. CTRL_0(0x96) <= PWR | RST_N | REQ to commit command in CTRL_1
    # 6. Wait until REQ bit in CTRL_0 is cleared
    # 7. CTRL_1(0x97) <= SOFT_PROG_SECTOR
    # 8. CTRL_0(0x96) <= PWR | RST_N | REQ to commit command in CTRL_1
    # 9. Wait until REQ bit in CTRL_0 is cleared
    # 10. CTRL_1(0x97) <= ERASE_SECTOR
    # 11. CTRL_0(0x96) <= PWR | RST_N | REQ to commit command in CTRL_1
    # 12. Wait until REQ bit in CTRL_0 is cleared
    # Write Sector:
    # 1. Write sector data into RW_BUFFER(0x53-0x5A)
    # 2. CTRL_0(0x96) <= PWR | RST_N
    # 3. CTRL_1(0x97) <= WRITE_PLR
    # 4. CTRL_0(0x96) <= PWR | RST_N | REQ to commit command in CTRL_1
    # 5. Wait until REQ bit in CTRL_0 is cleared
    # 6. CTRL_1(0x97) <= PROG_SECTOR
    # 7. CTRL_0(0x96) <= PWR | RST_N | REQ | SECTOR to commit command in CTRL_1
    # 8. Wait until REQ bit in CTRL_0 is cleared
    # Exit Programming mode:
    # 1. CTRL_0(0x96) <= RST_N
    # 2. CTRL_1(0x97) <= 0
    # 3. PASSWD(0x95) <= 0

    def nvm_write(self, sector_data):
        """Write data into NVM (Non-Volatile Memory).

        Args:
            sector_data: Dictionary where keys are sector numbers (0-4) and values are lists of 8 bytes.

        Note:
            Requires a hard reset to take effect.
        """
        pwr = 0x80
        rst_n = 0x40
        req = 0x10

        def nvm_wait_for_execution():
            while True:
                reg8 = self.bus.read_byte_data(self.addr, 0x96)
                if reg8 & 0x10 == 0x00:
                    break

        section_mask = 0
        for k, v in sector_data.items():
            if k >= 0 and k <= 4:
                if len(v) == 8:
                    section_mask |= 1 << k
                else:
                    print(f"New sector data has to many bytes (sector: {k})")
                    return
            else:
                print(f"Invalid sector {k}")
                return

        self.nvm_lock(False)
        # Erase specified sectors to be able to program them
        # self.bus.write_byte_data(self.addr, 0x53, 0x00)
        # self.bus.write_byte_data(self.addr, 0x96, pwr | rst_n)
        self.bus.write_byte_data(
            self.addr, 0x97, section_mask << 3 | 0x02
        )  # WRITE_SER opcode
        self.bus.write_byte_data(self.addr, 0x96, pwr | rst_n | req)
        nvm_wait_for_execution()
        self.bus.write_byte_data(self.addr, 0x97, 0x07)  # Soft_prog_sector opcode
        self.bus.write_byte_data(self.addr, 0x96, pwr | rst_n | req)
        nvm_wait_for_execution()
        self.bus.write_byte_data(self.addr, 0x97, 0x05)  # erase_sector opcode
        self.bus.write_byte_data(self.addr, 0x96, pwr | rst_n | req)
        nvm_wait_for_execution()
        # Write data to sectors
        for k, v in sector_data.items():
            # write new data into rw_bufer@0x53
            rw_buffer = 0x53
            for byte in v:
                self.bus.write_byte_data(self.addr, rw_buffer, byte)
                rw_buffer += 1
            self.bus.write_byte_data(self.addr, 0x97, 0x01)  # WRITE_PLR opcode
            self.bus.write_byte_data(self.addr, 0x96, pwr | rst_n | req)
            nvm_wait_for_execution()
            self.bus.write_byte_data(self.addr, 0x97, 0x06)  # PROG_SECTOR opcode
            self.bus.write_byte_data(self.addr, 0x96, pwr | rst_n | req | k)
            nvm_wait_for_execution()
        # Exit programming mode
        self.bus.write_byte_data(self.addr, 0x96, rst_n)
        self.bus.write_byte_data(self.addr, 0x97, 0)
        self.nvm_lock(True)

    def vbus_ctrl(self):
        """Read VBUS control and discharge configuration.

        Returns:
            Vbus: Object containing VBUS discharge and control settings.
        """
        # Read out relevant registers
        VBUS_DISCHARGE_TIME_CTRL = self.bus.read_byte_data(self.addr, 0x25)
        VBUS_DISCHARGE_CTRL = self.bus.read_byte_data(self.addr, 0x26)
        VBUS_CTRL = self.bus.read_byte_data(self.addr, 0x27)

        # Map data to the type
        return Vbus(
            discharge_0v=VBUS_DISCHARGE_TIME_CTRL >> 4 & 0x0F,
            discharge_trans=VBUS_DISCHARGE_TIME_CTRL & 0x0F,
            vbus_discharge=True if VBUS_DISCHARGE_CTRL >> 7 & 0x01 else False,
            vsrc_discharge=True if VBUS_DISCHARGE_CTRL >> 6 & 0x01 else False,
            sink_vbus_en=True if VBUS_CTRL >> 1 & 0x01 else False,
        )


# Default NVM values programmed by factory for SparkFun board
nvm_factory_defaults_sparkfun = {
    0: [0x00, 0x00, 0x60, 0x55, 0x01, 0x8A, 0x00, 0x00],
    1: [0x10, 0x40, 0x9C, 0x1C, 0xFF, 0x01, 0x3C, 0xDF],
    2: [0x02, 0x40, 0x0F, 0x00, 0x32, 0x00, 0xFC, 0xF1],
    3: [0x00, 0x19, 0x56, 0xAF, 0xF5, 0x35, 0x5F, 0x00],
    4: [0x00, 0x4B, 0x90, 0x21, 0x43, 0x00, 0x40, 0xFB],
}

# NVM configuration for Raspberry Pi 5 power requirements (5V up to 5A)
nvm_pi5 = {
    0: [0x00, 0x00, 0x60, 0x55, 0x01, 0x8A, 0x00, 0x00],
    1: [0x10, 0x40, 0x9D, 0x1C, 0xF0, 0x01, 0x38, 0xDF],
    2: [0xC2, 0x40, 0x0F, 0x01, 0x32, 0x00, 0xFC, 0xF1],
    3: [0x00, 0x19, 0x56, 0x5F, 0x5B, 0xF5, 0x55, 0x00],
    4: [0x00, 0x19, 0x64, 0x20, 0x43, 0x00, 0x40, 0xFB],
}

#  5V 1.5A
# 20V Flex 5A
# 20V 3A
nvm_custom = {
    0: [0x00, 0x00, 0xB0, 0xAB, 0x00, 0x45, 0x00, 0x00],
    1: [0x10, 0x40, 0x9C, 0x1C, 0xFF, 0x01, 0x3C, 0xDF],
    2: [0x02, 0x40, 0x0F, 0x00, 0x32, 0x00, 0xFC, 0xF1],
    3: [0x00, 0x19, 0x56, 0xAF, 0xF0, 0xB5, 0x5F, 0x00],
    4: [0x00, 0x64, 0x90, 0xD1, 0x47, 0x00, 0x40, 0xFB],
}


# Example usage
if __name__ == "__main__":
    # Create instance of STUSB4500
    stusb = STUSB4500(SMBus(0))

    # Dump NVM to compare
    stusb.nvm_dump()
    # stusb.nvm_write(nvm_custom)
    # stusb.reset()

    print(stusb.read_rdo())
    stusb.print_pdo()
    print(stusb.active_contract())
    print(stusb.port_status())
