import signal
import threading

import smbus2
import typer

from audio_server.drivers.adau1452 import ADAU1452
from audio_server.drivers.cap1188 import CAP1188, Button, Buttons
from audio_server.drivers.stusb4500 import STUSB4500
from audio_server.drivers.tas5825 import TAS5825
from audio_server.processing.chain import enable_filter_chain

I2C_BUS = "/dev/i2c-0"
DSP_I2C_ADDRESS = 0x3B
AMP_I2C_ADDRESS = 0x4E
PD_CONTROLLER_ADDRESS = 0x28

HAT_I2C_BUS = 1
CAP1188_I2C_ADDRESS = 0x2B

DSP_GPIO_ENABLE = 20


def slider_handler(amp: TAS5825, button: Button):
    volume_map_db = {
        Buttons.SLIDER_0: -100,
        Buttons.SLIDER_1: -18,
        Buttons.SLIDER_2: -12,
        Buttons.SLIDER_3: -6,
        Buttons.SLIDER_4: 0,
    }

    volume = volume_map_db[button.id]
    print(f"Setting volume to {volume} dB")
    amp.set_volume(volume)


def signal_handler(instances: list, signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down...")
    for instance in instances:
        instance.running = False


def main(init: bool = True, reload_filter: bool = True):
    i2c = smbus2.SMBus(I2C_BUS)
    dsp = ADAU1452(i2c, DSP_I2C_ADDRESS, DSP_GPIO_ENABLE)
    amp = TAS5825(i2c, AMP_I2C_ADDRESS)
    pd_controller = STUSB4500(i2c, PD_CONTROLLER_ADDRESS, reset_pin=None)

    if init:
        dsp.enable()
        amp.enable_shortcut()

    rdo = pd_controller.read_rdo()
    print(rdo)

    # This is quite dangerous
    if init:
        pd_controller.ensure_nvm_custom()

    # set to 0 dB
    amp.set_volume(0)

    if reload_filter:
        enable_filter_chain()

    cap1188 = CAP1188(HAT_I2C_BUS, CAP1188_I2C_ADDRESS)
    for slider in [
        Buttons.SLIDER_0,
        Buttons.SLIDER_1,
        Buttons.SLIDER_2,
        Buttons.SLIDER_3,
        Buttons.SLIDER_4,
    ]:
        cap1188.subscribe(slider, lambda button: slider_handler(amp, button))

    buttons = threading.Thread(target=cap1188.run)

    signal.signal(
        signal.SIGINT, lambda signum, frame: signal_handler([buttons], signum, frame)
    )
    buttons.start()
    print("Buttons thread started")
    buttons.join()


if __name__ == "__main__":
    typer.run(main)
