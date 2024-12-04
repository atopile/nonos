import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

# Interfaces
from .HDMI import HDMI

# Components
from .HRSHirose_DF40C_100DS_0_4V51 import HRSHirose_DF40C_100DS_0_4V51


logger = logging.getLogger(__name__)

class CM4_MINIMAL(Module):
    """
    CM4 module with minimal components
    """

    # Interfaces
    hdmi0: HDMI
    hdmi1: HDMI
    usb2: F.USB2_0
    power_5v: F.ElectricPower
    power_3v3: F.ElectricPower
    power_1v8: F.ElectricPower
    gpio = L.list_field(26, F.Electrical)

    # Components
    hdi_a: HRSHirose_DF40C_100DS_0_4V51
    hdi_b: HRSHirose_DF40C_100DS_0_4V51


    def __preinit__(self) -> None:
        # ------------------------------------
        #           connections
        # ------------------------------------
        #HDMI0
        self.hdmi0.data2.p.connect(self.hdi_b.pins[70])  # HDMI0_D2_P, pin 170
        self.hdmi0.data2.n.connect(self.hdi_b.pins[72])  # HDMI0_D2_N, pin 172
        self.hdmi0.data1.p.connect(self.hdi_b.pins[76])  # HDMI0_D1_P, pin 176
        self.hdmi0.data1.n.connect(self.hdi_b.pins[78])  # HDMI0_D1_N, pin 178
        self.hdmi0.data0.p.connect(self.hdi_b.pins[82])  # HDMI0_D0_P, pin 182
        self.hdmi0.data0.n.connect(self.hdi_b.pins[84])  # HDMI0_D0_N, pin 184

        # Clock pair
        self.hdmi0.clock.p.connect(self.hdi_b.pins[88])  # HDMI0_CK_P, pin 188
        self.hdmi0.clock.n.connect(self.hdi_b.pins[90])  # HDMI0_CK_N, pin 190

        # I2C and control signals
        self.hdmi0.i2c.scl.connect(self.hdi_b.pins[100]) # HDMI0_SCL, pin 200
        self.hdmi0.i2c.sda.connect(self.hdi_b.pins[99])  # HDMI0_SDA, pin 199
        self.hdmi0.cec.connect(self.hdi_b.pins[51])      # HDMI0_CEC, pin 151
        self.hdmi0.hotplug.connect(self.hdi_b.pins[53])  # HDMI0_HOTPLUG, pin 153
        
        # HDMI1
        self.hdmi1.data2.p.connect(self.hdi_b.pins[68])  # HDMI0_D2_P, pin 168
        self.hdmi1.data2.n.connect(self.hdi_b.pins[70])  # HDMI0_D2_N, pin 170
        self.hdmi1.data1.p.connect(self.hdi_b.pins[76])  # HDMI0_D1_P, pin 176
        self.hdmi1.data1.n.connect(self.hdi_b.pins[78])  # HDMI0_D1_N, pin 178
        self.hdmi1.data0.p.connect(self.hdi_b.pins[82])  # HDMI0_D0_P, pin 182
        self.hdmi1.data0.n.connect(self.hdi_b.pins[84])  # HDMI0_D0_N, pin 184

        # Clock pair
        self.hdmi1.clock.p.connect(self.hdi_b.pins[88])  # HDMI0_CK_P, pin 188
        self.hdmi1.clock.n.connect(self.hdi_b.pins[90])  # HDMI0_CK_N, pin 190

        # I2C and control signals
        self.hdmi1.i2c.scl.connect(self.hdi_b.pins[47])      # HDMI0_SCL, pin 147
        self.hdmi1.i2c.sda.connect(self.hdi_b.pins[45])      # HDMI0_SDA, pin 145
        self.hdmi1.cec.connect(self.hdi_b.pins[49])      # HDMI0_CEC, pin 149
        self.hdmi1.hotplug.connect(self.hdi_b.pins[51])  # HDMI0_HOTPLUG, pin 151

        # USBS2
        self.usb2.usb_if.Data.p.connect(self.hdi_b.pins[5])  # USB2_D_P, pin 10
        self.usb2.usb_if.Data.n.connect(self.hdi_b.pins[3])  # USB2_D_N, pin 11


        # Power
        
        # 5V power pins
        power_5v_pins = [77, 79, 81, 83, 85, 87]  # pins marked as +5v_(Input)

        for pin in power_5v_pins:
            self.power_5v.hv.connect(self.hdi_a.pins[pin])

        # 3.3V power pins
        power_3v3_pins = [84, 86]

        for pin in power_3v3_pins:
            self.power_3v3.hv.connect(self.hdi_a.pins[pin])

        # 1.8V power pins
        power_1v8_pins = [88, 90]

        for pin in power_1v8_pins:
            self.power_1v8.hv.connect(self.hdi_a.pins[pin])

        # GND pins
        gnd_pins_hdi_a = [
            1, 2, 7, 8, 13, 14, 21, 22, 23, 32, 33, 42, 43, 52, 53, 59,
            60, 65, 66, 71, 74, 98
        ]

        for pin in gnd_pins_hdi_a:
            self.power_5v.lv.connect(self.hdi_a.pins[pin])

        gnd_pins_hdi_b = [
            7, 8, 13, 14, 19, 20, 25, 26, 31, 32, 37, 38, 43, 44, 55, 56,
            61, 62, 67, 68, 73, 74, 79, 80, 85, 86, 91, 92, 97, 98
        ]

        for pin in gnd_pins_hdi_b:
            self.power_5v.lv.connect(self.hdi_b.pins[pin])

        # GPIO mapping
        gpio_mapping = {
            2: 58,  3: 56,  4: 54,  5: 34,  6: 30,  7: 37,  8: 39,  9: 40,
            10: 44, 11: 38, 12: 31, 13: 28, 14: 55, 15: 51, 16: 29, 17: 50,
            18: 49, 19: 26, 20: 27, 21: 25, 22: 46, 23: 47, 24: 45, 25: 41,
            26: 24, 27: 48
        }

        for gpio_num, pin_num in gpio_mapping.items():
            self.gpio[gpio_num].connect(self.hdi_a.pins[pin_num])

