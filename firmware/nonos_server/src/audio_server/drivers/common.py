import subprocess


def set_gpio_output(gpio: int, high: bool):
    subprocess.check_output(["pinctrl", "set", str(gpio), "op"])
    subprocess.check_output(["pinctrl", "set", str(gpio), f"d{'h' if high else 'l'}"])
