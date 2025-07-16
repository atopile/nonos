import smbus2
import typer

from audio_server.drivers.adau1452 import ADAU1452
from audio_server.drivers.stusb4500 import STUSB4500
from audio_server.drivers.tas5825 import TAS5825

I2C_BUS = "/dev/i2c-0"
DSP_I2C_ADDRESS = 0x3B
AMP_I2C_ADDRESS = 0x4E
PD_CONTROLLER_ADDRESS = 0x28

DSP_GPIO_ENABLE = 20


def main():
    i2c = smbus2.SMBus(I2C_BUS)
    dsp = ADAU1452(i2c, DSP_I2C_ADDRESS, DSP_GPIO_ENABLE)
    amp = TAS5825(i2c, AMP_I2C_ADDRESS)
    pd_controller = STUSB4500(i2c, PD_CONTROLLER_ADDRESS, reset_pin=None)

    dsp.enable()
    amp.enable_shortcut()

    print(pd_controller.read_rdo())

    # set to 0 dB
    amp.set_volume(-12.0)


if __name__ == "__main__":
    typer.run(main)
