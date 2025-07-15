from enum import IntEnum

import smbus2
import typer


class Map:
    # RESET = 0x00
    # TODO wtf is this?
    BOOK = 0x7F

    RESET_CTRL = 0x01
    DEVICE_CTRL_1 = 0x02
    DEVICE_CTRL2 = 0x03  # play mode
    I2C_PAGE_AUTO_INC = 0x0F
    SIG_CH_CTRL = 0x28
    CLOCK_DET_CTRL = 0x29
    SDOUT_SEL = 0x30
    I2S_CTRL = 0x31
    SAP_CTRL1 = 0x33
    SAP_CTRL2 = 0x34
    SAP_CTRL3 = 0x35
    FS_MON = 0x37
    BCK_SCLK_MON = 0x38
    CLKDET_STATUS = 0x39
    DSP_PGM_MODE = 0x40
    DSP_CTRL = 0x46
    DIG_VOL = 0x4C  # digital volume
    DIG_VOL_CTRL1 = 0x4E
    DIG_VOL_CTRL2 = 0x4F
    AUTO_MUTE_CTRL = 0x50
    AUTO_MUTE_TIME = 0x51
    ANA_CTRL = 0x53
    AGAIN = 0x54  # Analog Gain
    SPI_CLK = 0x55
    EEPROM_CTRL0 = 0x56
    EEPROM_RD_CMD = 0x57
    EEPROM_ADDR_START0 = 0x58
    EEPROM_ADDR_START1 = 0x59
    EEPROM_ADDR_START2 = 0x5A
    EEPROM_BOOT_STATUS = 0x5B
    BQ_WR_CTRL1 = 0x5C
    PVDD_ADC = 0x5E
    GPIO_CTRL = 0x60
    GPIO0_SEL = 0x61
    GPIO1_SEL = 0x62
    GPIO2_SEL = 0x63
    GPIO_INPUT_SEL = 0x64
    GPIO_OUT = 0x65
    GPIO_OUT_INV = 0x66
    DIE_ID = 0x67
    POWER_STATE = 0x68
    AUTOMUTE_STATE = 0x69
    PHASE_CTRL = 0x6A
    SS_CTRL0 = 0x6B
    SS_CTRL1 = 0x6C
    SS_CTRL2 = 0x6D
    SS_CTRL3 = 0x6E
    SS_CTRL4 = 0x6F
    CHAN_FAULT = 0x70
    GLOBAL_FAULT1 = 0x71
    GLOBAL_FAULT2 = 0x72
    WARNING = 0x73
    PIN_CONTROL1 = 0x74
    PIN_CONTROL2 = 0x75
    MISC_CONTROL = 0x76
    CBC_CONTROL = 0x77
    FAULT_CLEAR = 0x78


class Register:
    ADDR = 0x00

    def __init__(self, device: "TAS5825"):
        self.address = self.ADDR
        assert self.address != 0x00, "0x00 is reserved"
        self.device = device

    @property
    def value(self) -> int:
        return self.device.read_register(self.address)

    @value.setter
    def value(self, value: int):
        self.device.write_register(self.address, value)

    def set_bit(self, bit: int, value: bool):
        if value:
            self.value |= 1 << bit
        else:
            self.value &= ~(1 << bit)

    def read_bit(self, bit: int) -> bool:
        return bool(self.value & (1 << bit))

    def set_bits(self, mask: int, value: int):
        self.value = (self.value & ~mask) | (value & mask)


class Field:
    def __init__(self, register: Register):
        self.register = register


class FieldBit(Field):
    BIT = -1

    def __init__(self, register: Register):
        super().__init__(register)
        assert self.BIT != -1, "BIT must be set"

    @property
    def value(self) -> bool:
        return self.register.read_bit(self.BIT)

    @value.setter
    def value(self, value: bool):
        self.register.set_bit(self.BIT, value)


class Reset(Register):
    ADDR = 0x01

    def clear(self):
        self.value = 0x00


class DigitalVolume(Register):
    ADDR = 0x4C

    """
    These bits control both left and right channel digital volume. The
    digital volume is 24 dB to -103 dB in -0.5 dB step.
    00000000: +24.0 dB
    00000001: +23.5 dB
    ........
    and 00101111: +0.5 dB
    00110000: 0.0 dB
    00110001: -0.5 dB
    .......
    11111110: -103 dB
    11111111: Mute
    """

    @property
    def db(self) -> float:
        return -(self.value / 2)

    @db.setter
    def db(self, db: float) -> None:
        if db > 24:
            raise ValueError("Invalid volume, has to be <24dB")
        if db < -103:
            value = 0xFF  # mute
        else:
            value = int(-(db - 24) * 2)
        self.value = value


class DeviceControl2(Register):
    ADDR = 0x03

    class DisableDsp(FieldBit):
        """
        DSP reset
        When the bit is made 0, DSP starts powering up and send out data.
        This needs to be made 0 only after all the input clocks are settled so
        that DMA channels do not go out of sync.
        0: Normal operation
        1: Reset the DSP
        """

        BIT = 4

    class Mute(FieldBit):
        """
        Mute both Left and Right Channel
        This bit issues soft mute request for both left and right channel. The
        volume is smoothly ramped down/up to avoid pop/click noise.
        0: Normal volume
        1: Mute
        """

        BIT = 3

    class PlayMode(Field):
        class State(IntEnum):
            DeepSleep = 0x00
            Normal = 0x01
            Hiz = 0x02
            Play = 0x03

        @property
        def value(self) -> State:
            return self.State(self.register.value & 0x03)

        @value.setter
        def value(self, value: State):
            self.register.set_bits(0x03, value.value)


class SAP_CTRL1(Register):
    ADDR = 0x33

    class I2S_SHIFT_MSB(FieldBit):
        BIT = 7

    class DATA_FORMAT(Field):
        class Format(IntEnum):
            I2S = 0x00
            TDM_DSP = 0x01
            RTJ = 0x2
            LTJ = 0x3

        @property
        def value(self) -> Format:
            return self.Format(self.register.value & 0x03)

        @value.setter
        def value(self, value: Format):
            self.register.set_bits(0x03, value.value)

    # class I2S_LRCLK_PULSE(Field):

    class WORD_LENGTH(Field):
        class Length(IntEnum):
            B16 = 0x00
            B20 = 0x01
            B24 = 0x02
            B32 = 0x03

        @property
        def value(self) -> Length:
            return self.Length(self.register.value & 0x03)

        @value.setter
        def value(self, value: Length):
            self.register.set_bits(0x03, value.value)


class SAP_CTRL2(Register):
    ADDR = 0x34


class SAP_CTRL3(Register):
    ADDR = 0x35


class FS_MON(Register):
    ADDR = 0x37

    class FS_MON_STATUS(Field):
        class Status(IntEnum):
            """
            4 'b0000 FS Error
            4 'b0100 16 KHz
            4 'b0110 32 KHz
            4 'b1000 Reserved
            4 'b1001 48 KHz
            4 'b1011 96 KHz
            4 'b1101 192 KHz
            Others Reserved
            """

            FS_ERROR = 0x00
            FS_16K = 0x04
            FS_32K = 0x06
            FS_48K = 0x09
            FS_96K = 0x0B
            FS_192K = 0x0D


class AnalogGain(Register):
    ADDR = 0x54

    """
    Analog Gain Control
    This bit controls the analog gain.
    00000: 0 dB (29.5V peak voltage)
    00001:-0.5db 11111: -15.5 dB
    """

    @property
    def db(self) -> float:
        return -(self.value / 2)

    @db.setter
    def db(self, db: float) -> None:
        if db > 0 or db < -15.5:
            raise ValueError("Invalid gain, has to be between 0 and -15.5")
        self.value = int(-db * 2)


class FaultClear(Register):
    ADDR = 0x78

    def clear(self):
        self.value = 0x80


class TAS5825:
    def __init__(self, bus: smbus2.SMBus, address: int):
        self.bus = bus
        self.address = address

    def _write_register(self, register: int, value: int) -> None:
        print(f"Writing {register:02X} = {value:02X}")
        self.bus.write_byte_data(self.address, register, value)

    def write_register(self, register: int, value: int) -> None:
        pre_value = self.read_register(register)
        self._write_register(register, value)
        value_read = self.read_register(register)
        if pre_value != value:
            print(f"Changed register {register:02X}: {pre_value:02X} -> {value:02X}")
            return

        if value_read != value:
            print(f"Write failed {register:02X}: {value_read:02X} != {value:02X}")

    def read_register(self, register: int) -> int:
        return self.bus.read_byte_data(self.address, register)

    def enable_shortcut(self) -> None:
        Reset(device=self).clear()
        # tas5825.book()
        DigitalVolume(device=self).db = -12.0
        ctrl2 = DeviceControl2(device=self)
        DeviceControl2.DisableDsp(ctrl2).value = False
        DeviceControl2.Mute(ctrl2).value = False
        DeviceControl2.PlayMode(ctrl2).value = DeviceControl2.PlayMode.State.Play
        AnalogGain(device=self).db = 0.0
        FaultClear(device=self).clear()

    def set_volume(self, db: float) -> None:
        DigitalVolume(device=self).db = db


def main() -> None:
    bus = smbus2.SMBus("/dev/i2c-0")
    tas5825 = TAS5825(bus, 0x4E)

    d = tas5825
    print("Resetting")
    d.enable_shortcut()

    sap_ctrl2 = SAP_CTRL2(device=d)
    print(SAP_CTRL1.DATA_FORMAT(sap_ctrl2).value)
    print(SAP_CTRL1.WORD_LENGTH(sap_ctrl2).value)

    # d.set_volume(0xFF)
    print("Done")


if __name__ == "__main__":
    typer.run(main)
