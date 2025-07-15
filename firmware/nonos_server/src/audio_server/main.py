import subprocess

import smbus2
import typer
from drivers.stusb4500 import STUSB4500
from drivers.tas5825 import TAS5825

I2C_BUS = "/dev/i2c-0"
DSP_I2C_ADDRESS = 0x3B
AMP_I2C_ADDRESS = 0x4E
PD_CONTROLLER_ADDRESS = 0x28

DSP_GPIO_ENABLE = 20


def set_gpio_output(gpio: int, high: bool):
    subprocess.check_output(["pinctrl", "set", str(gpio), "op"])
    subprocess.check_output(["pinctrl", "set", str(gpio), f"d{'h' if high else 'l'}"])


class DSP:
    def __init__(self, bus: smbus2.SMBus, address: int, gpio_enable: int):
        self.bus = bus
        self.address = address
        self.gpio_enable = gpio_enable

    def enable(self):
        set_gpio_output(self.gpio_enable, True)


def main():
    i2c = smbus2.SMBus(I2C_BUS)
    dsp = DSP(i2c, DSP_I2C_ADDRESS, DSP_GPIO_ENABLE)
    amp = TAS5825(i2c, AMP_I2C_ADDRESS)
    pd_controller = STUSB4500(i2c, PD_CONTROLLER_ADDRESS, reset_pin=None)

    dsp.enable()
    amp.enable_shortcut()

    print(pd_controller.read_rdo())

    # set to 0 dB
    amp.set_volume(0.0)


if __name__ == "__main__":
    typer.run(main)
