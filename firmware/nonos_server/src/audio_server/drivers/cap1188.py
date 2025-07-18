"""
CAP1188 Touch Monitor - Python version
Monitors touch events from CAP1188 capacitive touch controller
"""

import time
from collections.abc import Callable
from datetime import datetime
from enum import IntEnum

import gpiod
import smbus2
import typer
from gpiod.line import Direction, Edge


class _Registers(IntEnum):
    PRODUCT_ID = 0xFD
    MANUFACTURER_ID = 0xFE
    SENSITIVITY = 0x1F
    MAIN_CONTROL = 0x00
    SENSOR_INPUT_ENABLE = 0x21
    RECALIBRATION_CONFIGURATION = 0x2F
    INTERRUPT_ENABLE = 0x27
    TOUCH_STATUS = 0x03


class Buttons(IntEnum):
    BOT_MIDDLE = 0
    BOT_LEFT = 1
    BOT_RIGHT = 2
    SLIDER_0 = 3
    SLIDER_1 = 4
    SLIDER_2 = 5
    SLIDER_3 = 6
    SLIDER_4 = 7


DEBOUNCE_MS = 100


class Button:
    def __init__(self, id: Buttons, debounce_ms: int = DEBOUNCE_MS):
        self.id = id
        self.callbacks: list[Callable[[Button], None]] = []
        self.last_pressed = None
        self.debounce_ms = debounce_ms

    def feed(self, pressed: bool):
        if pressed:
            now = time.monotonic()
            if self.last_pressed is not None and (now - self.last_pressed) < (
                self.debounce_ms / 1000
            ):
                print(f"Button {self.id.name} pressed but debounced")
                return
            print(now)
            self.last_pressed = now
            print(f"Button {self.id.name} pressed (delta {now - self.last_pressed})")
            for callback in self.callbacks:
                callback(self)

    def subscribe(self, callback: "Callable[[Button], None]"):
        self.callbacks.append(callback)


class CAP1188:
    def __init__(
        self, i2c_bus=1, i2c_address=0x2B, gpio_chip="gpiochip0", interrupt_pin=22
    ):
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.gpio_chip_name = gpio_chip
        self.interrupt_pin = interrupt_pin

        # Initialize components
        self.bus = smbus2.SMBus(self.i2c_bus)

        # Initialize GPIO using modern gpiod v2.0+ API
        self.interrupt_request = gpiod.request_lines(
            "/dev/" + self.gpio_chip_name,
            consumer="cap1188-monitor",
            config={
                self.interrupt_pin: gpiod.LineSettings(
                    direction=Direction.INPUT,
                    edge_detection=Edge.FALLING,
                )
            },
        )
        print(f"GPIO {self.interrupt_pin} initialized for interrupts")

        self.running = False  # Initialize components

        self.buttons = [Button(id) for id in Buttons]

    def subscribe(self, button: Buttons, callback: "Callable[[Button], None]"):
        b = self.buttons[button]
        b.subscribe(callback)
        return b

    def write_reg(self, reg: int, data: int):
        self.bus.write_byte_data(self.i2c_address, reg, data)

    def read_reg(self, reg: int):
        return self.bus.read_byte_data(self.i2c_address, reg)

    def set_sensitivity(
        self, sensitivity_multiplier_pow_2: int, base_shift_pow_2: int | None = None
    ):
        """
        sensitivity_multiplier: 1 - 128 (2**0 - 2**7)
        base_shift: 1 - 256
        """

        """
        https://ww1.microchip.com/downloads/en/DeviceDoc/CAP1188-Touch-Monitor-Data-Sheet-DS20005882A.pdf
        DELTA_SENSE[2:0] - Controls the sensitivity of a touch detection. The sensitivity settings act to scale the rel-
        ative delta count value higher or lower based on the system parameters. At the more sensitive settings, touches are detected for a smaller delta capacitance
        corresponding to a "lighter" touch. These settings are more sensitive to noise, however, and a noisy environment may
        flag more false touches with higher sensitivity levels.

        BASE_SHIFT[3:0] - Controls the scaling and data presentation of the Base Count registers. The higher the
        value of these bits, the larger the range and the lower the resolution of the data presented. The scale factor represents
        the multiplier to the bit-weighting presented in these register descriptions.
        """

        if not base_shift_pow_2:
            base_shift_pow_2 = self.read_reg(_Registers.SENSITIVITY) & 0x0F
            if base_shift_pow_2 > 8:
                base_shift_pow_2 = 8

        assert 0 <= sensitivity_multiplier_pow_2 <= 7
        assert 0 <= base_shift_pow_2 <= 8

        delta_sense = (~sensitivity_multiplier_pow_2) & 0x7

        data = (delta_sense << 4) | (base_shift_pow_2 & 0x0F)

        self.write_reg(_Registers.SENSITIVITY, data)

    def clear_interrupt(self):
        self.write_reg(
            _Registers.MAIN_CONTROL, self.read_reg(_Registers.MAIN_CONTROL) & ~(0x1)
        )

    def enable(self):
        """Initialize CAP1188 touch controller"""
        # Check device ID
        product_id = self.read_reg(_Registers.PRODUCT_ID)
        if product_id != 0x50:
            print(f"Warning: Unexpected product ID: 0x{product_id:02X} (expected 0x50)")

        manufacturer_id = self.read_reg(_Registers.MANUFACTURER_ID)
        if manufacturer_id != 0x5D:
            print(
                f"Warning: Unexpected manufacturer ID: 0x{manufacturer_id:02X} (expected 0x5D)"
            )

        print(
            f"CAP1188 detected - Product ID: 0x{product_id:02X}, Manufacturer ID: 0x{manufacturer_id:02X}"
        )

        # Initialize registers
        self.clear_interrupt()
        self.write_reg(_Registers.SENSOR_INPUT_ENABLE, 0xFF)  # Enable all sensors
        self.set_sensitivity(7)  # Set sensitivity
        self.write_reg(_Registers.INTERRUPT_ENABLE, 0xFF)  # Enable interrupts

        print("CAP1188 initialized successfully")

    def read_touch_status(self):
        """Read touch status from CAP1188"""
        try:
            return self.read_reg(_Registers.TOUCH_STATUS)
        except Exception as e:
            print(f"Error reading touch status: {e}")
            return 0

    def decode_touch(self, touch_status):
        """Decode and display touch status"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{timestamp} - Touch interrupt detected!")
        print(f"Touch status: {touch_status:08b}")

        for b in self.buttons:
            b.feed(touch_status & (1 << b.id))

        # Check each bit for touched sensors
        # touched_sensors = []
        # for i in range(8):
        #     if touch_status & (1 << i):
        #         button_name = Buttons(i).name
        #         print(f"  ✓ {button_name}")
        #         touched_sensors.append(i)

        # Analyze slider activity
        # slider_bits = (touch_status >> 3) & 0x1F  # Extract bits 3-7
        # if slider_bits > 0:
        #    print(f"  → Slider active: pattern 0x{slider_bits:02X}")

        #    # Simple gesture detection
        #    if slider_bits in [0x01, 0x02, 0x04, 0x08, 0x10]:
        #        print("  → Single touch detected")
        #    elif bin(slider_bits).count("1") > 1:
        #        print("  → Multi-touch detected")

        # if not touched_sensors:
        #     print("  (No sensors touched - possible noise)")

        print("-" * 40)

    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, "interrupt_request"):
            self.interrupt_request.release()
        if self.bus:
            self.bus.close()
        print("Cleanup complete")

    def run(self):
        """Main monitoring loop"""
        print("CAP1188 Touch Monitor (Python version)")
        print("=" * 40)

        self.enable()

        print("\nMonitoring for touch events (Ctrl+C to exit)...")
        print("Touch the buttons or slider to see events.\n")

        self.running = True
        try:
            while self.running:
                # Wait for interrupt (1 second timeout)
                if self.interrupt_request.wait_edge_events(timeout=1.0):
                    events = self.interrupt_request.read_edge_events()
                    for event in events:
                        if event.event_type == gpiod.EdgeEvent.Type.FALLING_EDGE:
                            # Read and decode touch status
                            touch_status = self.read_touch_status()
                            self.decode_touch(touch_status)

                            # Clear interrupt
                            self.clear_interrupt()

        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self.cleanup()


def main():
    """Main function"""

    # Create and run monitor
    monitor = CAP1188()
    monitor.run()


if __name__ == "__main__":
    typer.run(main)
