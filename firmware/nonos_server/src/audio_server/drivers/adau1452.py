from enum import IntEnum
from time import sleep

from smbus2 import SMBus

from audio_server.drivers.common import (
    set_gpio_output,
)
from tcp_i2c_bridge.i2c_backend import SMBusI2CBackend

SLEEP_TIME = 0.5


class _Register(IntEnum):
    SOFT_RESET = 0xF890
    HIBERNATE = 0xF400
    KILL_CORE = 0xF403
    PLL_ENABLE = 0xF003
    PLL_CTRL0 = 0xF000
    PLL_CTRL1 = 0xF001
    PLL_CLK_SRC = 0xF002
    MCLK_OUT = 0xF005
    POWER_ENABLE0 = 0xF050
    POWER_ENABLE1 = 0xF051
    SOUT_SOURCE0 = 0xF180
    SERIAL_BYTE_0_0 = 0xF200
    PROGRAM_DATA = 0xC000
    DM0 = 0x0000
    DM1 = 0x6000
    START_ADDRESS = 0xF401
    START_PULSE = 0xF402
    START_CORE = 0xF405


class ADAU1452:
    def __init__(self, smbus: SMBus, addr: int = 0x3B, gpio_enable: int = 20):
        self.smbus = smbus
        self.addr = addr
        self.gpio_enable = gpio_enable
        self.i2c = SMBusI2CBackend(smbus, addr)

    def write_reg(self, addr: int | _Register, data: str) -> None:
        data_bytes = bytes.fromhex(data)

        print(
            f"Writing {data_bytes} to {addr.name if isinstance(addr, _Register) else hex(addr)}"
        )
        self.i2c.write(addr, data_bytes)

    def read_reg(self, addr: int, length: int = 2) -> bytearray:
        return bytearray(self.i2c.read(addr, length))

    def read_reg_int(self, addr: int, length: int = 2) -> int:
        return int.from_bytes(self.read_reg(addr, length), "big")

    def check(self, addr: _Register, expected: str, length: int = 2) -> None:
        val = self.read_reg(addr, length)
        expected_bytes = bytes.fromhex(expected)
        if val != expected_bytes:
            raise Exception(
                f"Expected {expected_bytes.hex()} at {addr.name}, got {val.hex()}"
            )

    def set_sout_source(self, index: int, source: str) -> None:
        assert 0 <= index <= 23
        self.write_reg(_Register.SOUT_SOURCE0 + index, source)

    def set_serial_byte(self, index: int, data: str) -> None:
        assert 0 <= index <= 7
        self.write_reg(_Register.SERIAL_BYTE_0_0 + index * 4, data)

    def enable(self):
        set_gpio_output(self.gpio_enable, True)
        sleep(0.5)

        # Soft reset
        self.write_reg(_Register.SOFT_RESET, "0000")
        self.write_reg(_Register.SOFT_RESET, "0001")
        sleep(SLEEP_TIME)

        # Hibernate
        self.write_reg(_Register.HIBERNATE, "0000")
        self.write_reg(_Register.HIBERNATE, "0001")
        sleep(SLEEP_TIME)

        self.check(_Register.HIBERNATE, "0001")

        # Kill Core
        self.write_reg(_Register.KILL_CORE, "0000")
        self.write_reg(_Register.KILL_CORE, "0001")

        # PLL Enable
        self.write_reg(_Register.PLL_ENABLE, "0000")
        self.write_reg(_Register.PLL_CTRL0, "0060")
        self.write_reg(_Register.PLL_CTRL1, "0002")
        self.write_reg(_Register.PLL_CLK_SRC, "0001")
        self.write_reg(_Register.MCLK_OUT, "0005")
        self.write_reg(_Register.PLL_ENABLE, "0001")
        sleep(SLEEP_TIME)

        # Power Enable
        self.write_reg(_Register.POWER_ENABLE0, "1fff")
        self.write_reg(_Register.POWER_ENABLE1, "001f")

        # SOUT_SOURCE0-23
        self.set_sout_source(0, "0001")
        self.set_sout_source(1, "0001")
        for i in range(2, 24):
            self.set_sout_source(i, "0002")

        # Serial Byte 0_0 -> 7_0
        self.set_serial_byte(0, "0040")
        for i in range(1, 8):
            self.set_serial_byte(i, "9000")

        # Program Data
        self.write_reg(
            _Register.PROGRAM_DATA,
            "000000020c00dcdc0d00ffd20d00ffd00d00f4500d00f400c000238080000000c000230080000000c00023c080000010c0002200800000000880dce00c00dcdc0a210012080000100100001406405010c0002000800000270d00ffc1c0002000800000010d00f462c0002000800000000d00f462c0002000800000020d00ffd1000000030d00ffd2000000050000000000000000020100220000000000000000089edce0089c001000000000c0000000824f0000088adce00a230006008c20000aa700050209003ec000287080006000008c119100000023000000003000bce90000c2f10100003d060050143640501526404015092b0006000000000890001b0c7000140e3d001700f4ae0f0a25dcdc0ae100150000dc700000a4d800d621010000e02907058808008419b30004459000442c3000044928009408870be10015054d100e0c00fc400640102e0c00fc410640103e0600100e0640101e0d00002a000400000ae100210c40001e001c804000840881008c18890be100210ba1002800d7ed080bb500290600101e0d00fcc00600102e0640104e0d000038000400000ae1002f0c40002c001c804000840881008c18890be1002f0ba1003600d7ed080bb50037089c00100000000000002e0100000000099c0010000000020c10f46002c2000000000000000000000000000000000000",
        )
        # DM0
        self.write_reg(
            _Register.DM0,
            "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000080000000800000000010000000000000000000000000007ffffffffff00055555000000000000c0000000c0000000080000009d61000001e000000e39000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009d61000001e000000e39000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        )
        # DM1
        self.write_reg(
            _Register.DM1,
            "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        )
        # Kill Core
        self.write_reg(_Register.KILL_CORE, "0000")
        # Start Address
        self.write_reg(_Register.START_ADDRESS, "0000")
        # Start Pulse
        self.write_reg(_Register.START_PULSE, "0002")
        # Start Core
        self.write_reg(_Register.START_CORE, "0000")
        self.write_reg(_Register.START_CORE, "0001")
        sleep(SLEEP_TIME)

        # Hibernate
        self.write_reg(_Register.HIBERNATE, "0000")

        # READ addr=0xF405 len=2 data=0000

        self.check(_Register.HIBERNATE, "0000")
        self.check(_Register.KILL_CORE, "0000")
