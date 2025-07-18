import signal
import socket
import threading

import smbus2
import typer

from audio_server.drivers.adau1452 import ADAU1452
from audio_server.drivers.cap1188 import CAP1188, Button, Buttons
from audio_server.drivers.stusb4500 import STUSB4500
from audio_server.drivers.tas5825 import TAS5825
from audio_server.mediactrl import (
    next_track,
    play_mpv,
    play_pause_track,
    previous_track,
)
from audio_server.processing.chain import enable_filter_chain

I2C_BUS = "/dev/i2c-0"
DSP_I2C_ADDRESS = 0x3B
AMP_I2C_ADDRESS = 0x4E
PD_CONTROLLER_ADDRESS = 0x28

HAT_I2C_BUS = 1
CAP1188_I2C_ADDRESS = 0x2B

DSP_GPIO_ENABLE = 20

g_last_slider: Button | None = None


def slider_handler(amp: TAS5825, button: Button):
    global g_last_slider

    volume_map_db = {
        Buttons.SLIDER_0: -24,
        Buttons.SLIDER_1: -18,
        Buttons.SLIDER_2: -12,
        Buttons.SLIDER_3: -6,
        Buttons.SLIDER_4: 0,
    }

    volume = volume_map_db[button.id]

    # Mute
    if g_last_slider is not None:
        if button.id == Buttons.SLIDER_0 and g_last_slider.id == Buttons.SLIDER_0:
            print("Mute")
            volume = -100
        # Boost
        if button.id == Buttons.SLIDER_4 and g_last_slider.id == Buttons.SLIDER_4:
            print("Boost")
            volume = 6

    g_last_slider = button

    print(f"Setting volume to {volume} dB")
    amp.set_volume(volume)


def play_pause_handler(_: Button):
    print("Play/Pause")
    try:
        play_pause_track()
    except Exception as e:
        print(f"Error playing/pausing: {e}")


def prev_handler(_: Button):
    print("Previous")
    try:
        previous_track()
    except Exception as e:
        print(f"Error playing/pausing: {e}")


def next_handler(_: Button):
    print("Next")
    try:
        next_track()
    except Exception as e:
        print(f"Error playing/pausing: {e}")


def signal_handler(instances: list, signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down...")
    for instance in instances:
        print("Setting", instance, "running to False")
        instance.running = False


PER_HOST_DEFAULTS = {
    "nonos-2": {
        "mpv": True,
    },
    "nonos-3": {
        "mpv": True,
    },
}
hostname = socket.gethostname()
HOST_CONFIG = PER_HOST_DEFAULTS.get(hostname, {})


def main(
    init: bool = True,
    reload_filter: bool = True,
    mpv: bool = HOST_CONFIG.get("mpv", True),
):
    i2c = smbus2.SMBus(I2C_BUS)
    dsp = ADAU1452(i2c, DSP_I2C_ADDRESS, DSP_GPIO_ENABLE)
    amp = TAS5825(i2c, AMP_I2C_ADDRESS)
    pd_controller = STUSB4500(i2c, PD_CONTROLLER_ADDRESS, reset_pin=None)
    buttons = CAP1188(HAT_I2C_BUS, CAP1188_I2C_ADDRESS)

    if init:
        dsp.enable()
        amp.enable_shortcut()

    rdo = pd_controller.read_rdo()
    print(rdo)

    # This is quite dangerous
    if init:
        pd_controller.ensure_nvm_custom()
        # set to 0 dB
        amp.set_volume(-12)

    if reload_filter:
        enable_filter_chain()

    for slider in [
        Buttons.SLIDER_0,
        Buttons.SLIDER_1,
        Buttons.SLIDER_2,
        Buttons.SLIDER_3,
        Buttons.SLIDER_4,
    ]:
        buttons.subscribe(
            slider, lambda button: slider_handler(amp, button)
        ).debounce_ms = 250

    buttons.subscribe(Buttons.BOT_MIDDLE, play_pause_handler).debounce_ms = 500
    buttons.subscribe(Buttons.BOT_LEFT, prev_handler).debounce_ms = 250
    buttons.subscribe(Buttons.BOT_RIGHT, next_handler).debounce_ms = 250

    buttons_thread = threading.Thread(target=buttons.run)  # noqa: F841

    signal.signal(
        signal.SIGINT,
        lambda signum, frame: signal_handler([buttons], signum, frame),
    )

    if mpv:
        play_mpv()
    buttons.run()
    # buttons_thread.start()
    # print("Buttons thread started")
    # buttons_thread.join()


if __name__ == "__main__":
    typer.run(main)
