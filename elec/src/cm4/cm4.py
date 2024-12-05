from enum import Enum
import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

# Interfaces
from .HDMI import HDMI
from .Ethernet import GigabitEthernet
from .I2S import I2S
# Components
from .HRSHirose_DF40C_100DS_0_4V51 import HRSHirose_DF40C_100DS_0_4V51
from .Texas_Instruments_SN74LVC1G07DBVR import Texas_Instruments_SN74LVC1G07DBVR

logger = logging.getLogger(__name__)


class GPIO_Ref_Voltages(Enum):
    V1_8 = 1.8
    V3_3 = 3.3


class CM4_MINIMAL(Module):
    """
    CM4 module with minimal components
    """

    # Interfaces
    hdmi0: HDMI
    hdmi1: HDMI
    ethernet: GigabitEthernet
    usb2: F.USB2_0
    power_5v: F.ElectricPower
    power_3v3: F.ElectricPower
    power_1v8: F.ElectricPower
    gpio = L.list_field(28, F.ElectricLogic)
    i2s: I2S

    # Components
    hdi_a: HRSHirose_DF40C_100DS_0_4V51
    hdi_b: HRSHirose_DF40C_100DS_0_4V51
    power_led_buffer: Texas_Instruments_SN74LVC1G07DBVR
    power_led: F.LED

    def __init__(self, gpio_ref_voltage: GPIO_Ref_Voltages = GPIO_Ref_Voltages.V3_3) -> None:
        super().__init__()
        self.gpio_ref_voltage = gpio_ref_voltage.value * P.V


    def __preinit__(self) -> None:
        # ------------------------------------
        #           connections
        # ------------------------------------
        #HDMI0
        self.hdmi0.data2.p.signal.connect(self.hdi_b.pins[69])  # HDMI0_D2_P, pin 170
        self.hdmi0.data2.n.signal.connect(self.hdi_b.pins[71])  # HDMI0_D2_N, pin 172
        self.hdmi0.data1.p.signal.connect(self.hdi_b.pins[75])  # HDMI0_D1_P, pin 176
        self.hdmi0.data1.n.signal.connect(self.hdi_b.pins[77])  # HDMI0_D1_N, pin 178
        self.hdmi0.data0.p.signal.connect(self.hdi_b.pins[81])  # HDMI0_D0_P, pin 182
        self.hdmi0.data0.n.signal.connect(self.hdi_b.pins[83])  # HDMI0_D0_N, pin 184

        # Clock pair
        self.hdmi0.clock.p.signal.connect(self.hdi_b.pins[87])  # HDMI0_CK_P, pin 188
        self.hdmi0.clock.n.signal.connect(self.hdi_b.pins[89])  # HDMI0_CK_N, pin 190

        # I2C and control signals
        self.hdmi0.i2c.scl.signal.connect(self.hdi_b.pins[99]) # HDMI0_SCL, pin 200
        self.hdmi0.i2c.sda.signal.connect(self.hdi_b.pins[98])  # HDMI0_SDA, pin 199
        self.hdmi0.cec.signal.connect(self.hdi_b.pins[50])      # HDMI0_CEC, pin 151
        self.hdmi0.hotplug.signal.connect(self.hdi_b.pins[52])  # HDMI0_HOTPLUG, pin 153
        
        # HDMI1
        self.hdmi1.data2.p.signal.connect(self.hdi_b.pins[67])  # HDMI0_D2_P, pin 168
        self.hdmi1.data2.n.signal.connect(self.hdi_b.pins[69])  # HDMI0_D2_N, pin 170
        self.hdmi1.data1.p.signal.connect(self.hdi_b.pins[75])  # HDMI0_D1_P, pin 176
        self.hdmi1.data1.n.signal.connect(self.hdi_b.pins[77])  # HDMI0_D1_N, pin 178
        self.hdmi1.data0.p.signal.connect(self.hdi_b.pins[81])  # HDMI0_D0_P, pin 182
        self.hdmi1.data0.n.signal.connect(self.hdi_b.pins[83])  # HDMI0_D0_N, pin 184

        # Clock pair
        self.hdmi1.clock.p.signal.connect(self.hdi_b.pins[87])  # HDMI0_CK_P, pin 188
        self.hdmi1.clock.n.signal.connect(self.hdi_b.pins[89])  # HDMI0_CK_N, pin 190

        # I2C and control signals
        self.hdmi1.i2c.scl.signal.connect(self.hdi_b.pins[46])      # HDMI0_SCL, pin 147
        self.hdmi1.i2c.sda.signal.connect(self.hdi_b.pins[44])      # HDMI0_SDA, pin 145
        self.hdmi1.cec.signal.connect(self.hdi_b.pins[48])      # HDMI0_CEC, pin 149
        self.hdmi1.hotplug.signal.connect(self.hdi_b.pins[50])  # HDMI0_HOTPLUG, pin 151

        # USBS2
        self.usb2.usb_if.d.p.signal.connect(self.hdi_b.pins[4])  # USB2_D_P, pin 10
        self.usb2.usb_if.d.n.signal.connect(self.hdi_b.pins[2])  # USB2_D_N, pin 11

        # Power
        # 5V power pins
        power_5v_pins = [76, 78, 80, 82, 84, 86]  # pins marked as +5v_(Input)

        for pin in power_5v_pins:
            self.power_5v.hv.connect(self.hdi_a.pins[pin])

        # 3.3V power pins
        power_3v3_pins = [83, 85]

        for pin in power_3v3_pins:
            self.power_3v3.hv.connect(self.hdi_a.pins[pin])

        # 1.8V power pins
        power_1v8_pins = [87, 89]

        for pin in power_1v8_pins:
            self.power_1v8.hv.connect(self.hdi_a.pins[pin])

        # GND pins
        gnd_pins_hdi_a = [
            0, 1, 6, 7, 12, 13, 20, 21, 22, 31, 32, 41, 42, 51, 52, 58,
            59, 64, 65, 70, 73, 97
        ]

        for pin in gnd_pins_hdi_a:
            self.power_5v.lv.connect(self.hdi_a.pins[pin])

        gnd_pins_hdi_b = [
            6, 7, 12, 13, 18, 19, 24, 25, 30, 31, 36, 37, 42, 43, 54, 55,
            60, 61, 66, 67, 72, 73, 78, 79, 84, 85, 90, 91, 96, 97
        ]

        for pin in gnd_pins_hdi_b:
            self.power_5v.lv.connect(self.hdi_b.pins[pin])

        # GPIO mapping
        gpio_mapping = {
            2: 57,  3: 55,  4: 53,  5: 33,  6: 29,  7: 36,  8: 38,  9: 39,
            10: 43, 11: 37, 12: 30, 13: 27, 14: 54, 15: 50, 16: 28, 17: 49,
            18: 48, 19: 25, 20: 26, 21: 24, 22: 45, 23: 46, 24: 44, 25: 40,
            26: 23, 27: 47
        }

        for gpio_num, pin_num in gpio_mapping.items():
            self.gpio[gpio_num].signal.connect(self.hdi_a.pins[pin_num])

        # GPIO Reference voltage setter
        if self.gpio_ref_voltage == GPIO_Ref_Voltages.V1_8:
            self.power_1v8.hv.connect(self.hdi_a.pins[77])
        else:
            self.power_3v3.hv.connect(self.hdi_a.pins[77])

        # Ethernet
        self.ethernet.pair1.p.signal.connect(self.hdi_a.pins[3])
        self.ethernet.pair1.n.signal.connect(self.hdi_a.pins[5])
        self.ethernet.pair0.n.signal.connect(self.hdi_a.pins[9])
        self.ethernet.pair0.p.signal.connect(self.hdi_a.pins[11])
        self.ethernet.pair3.p.signal.connect(self.hdi_a.pins[2])
        self.ethernet.pair3.n.signal.connect(self.hdi_a.pins[4])
        self.ethernet.pair2.n.signal.connect(self.hdi_a.pins[8])
        self.ethernet.pair2.p.signal.connect(self.hdi_a.pins[10])

        # I2S
        self.i2s.sck.connect(self.gpio[18])
        self.i2s.ws.connect(self.gpio[19])
        self.i2s.sd.connect(self.gpio[21]) # output

        # Ethernet LED signals
        self.ethernet.led_link.signal.connect(self.hdi_a.pins[14])
        self.ethernet.led_activity.signal.connect(self.hdi_a.pins[16])

        # Boot selection


        # Power LED
        self.power_led_buffer.power.connect(self.power_3v3)
        self.power_led_buffer.input.signal.connect(self.hdi_a.pins[95])
        self.power_led.connect_via_current_limiting_resistor_to_power(
            F.Resistor(),
            self.power_3v3,
            low_side=True
        )
        self.power_led.cathode.connect(self.power_led_buffer.output.signal)

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.power_5v.voltage.merge(F.Range.from_center_rel(5 * P.V, 0.05))
        self.power_3v3.voltage.merge(F.Range.from_center_rel(3.3 * P.V, 0.05))
        self.power_1v8.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))

        if self.gpio_ref_voltage == GPIO_Ref_Voltages.V1_8:
            for gpio in self.gpio:
                gpio.reference.voltage.merge(self.power_1v8.voltage)
        else:
            for gpio in self.gpio:
                gpio.reference.voltage.merge(self.power_3v3.voltage)