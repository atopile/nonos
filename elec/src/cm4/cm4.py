from enum import Enum
import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

# Interfaces

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
    hdmi0: F.HDMI
    hdmi1: F.HDMI
    ethernet: F.Ethernet
    usb2: F.USB2_0
    power_5v: F.ElectricPower
    power_3v3: F.ElectricPower
    power_1v8: F.ElectricPower
    gpio_ref: F.ElectricPower
    gpio = L.list_field(28, F.ElectricLogic)
    i2s: F.I2S
    i2c: F.I2C

    uart_rx: F.ElectricLogic
    uart_tx: F.ElectricLogic

    # Components
    hdi_a: HRSHirose_DF40C_100DS_0_4V51
    hdi_b: HRSHirose_DF40C_100DS_0_4V51
    power_led_buffer: Texas_Instruments_SN74LVC1G07DBVR
    power_led: F.LED
    power_led_resistor: F.Resistor
    activity_led: F.LED
    activity_led_resistor: F.Resistor

    def __init__(
        self, gpio_ref_voltage: GPIO_Ref_Voltages = GPIO_Ref_Voltages.V3_3
    ) -> None:
        super().__init__()
        self.gpio_ref_voltage = gpio_ref_voltage.value * P.V

    def __preinit__(self) -> None:
        # ------------------------------------
        #           connections
        # ------------------------------------
        # HDMI0
        self.hdmi0.data[2].p.signal.connect(self.hdi_b.pins[69])
        self.hdmi0.data[2].n.signal.connect(self.hdi_b.pins[71])
        self.hdmi0.data[1].p.signal.connect(self.hdi_b.pins[75])
        self.hdmi0.data[1].n.signal.connect(self.hdi_b.pins[77])
        self.hdmi0.data[0].p.signal.connect(self.hdi_b.pins[81])
        self.hdmi0.data[0].n.signal.connect(self.hdi_b.pins[83])

        # Clock pair
        self.hdmi0.clock.p.signal.connect(self.hdi_b.pins[87])
        self.hdmi0.clock.n.signal.connect(self.hdi_b.pins[89])

        # I2C and control signals
        self.hdmi0.i2c.scl.signal.connect(self.hdi_b.pins[99])
        self.hdmi0.i2c.sda.signal.connect(self.hdi_b.pins[98])
        self.hdmi0.cec.signal.connect(self.hdi_b.pins[50])
        self.hdmi0.hotplug.signal.connect(self.hdi_b.pins[52])

        # HDMI1
        self.hdmi1.data[2].p.signal.connect(self.hdi_b.pins[45])
        self.hdmi1.data[2].n.signal.connect(self.hdi_b.pins[47])
        self.hdmi1.data[1].p.signal.connect(self.hdi_b.pins[51])
        self.hdmi1.data[1].n.signal.connect(self.hdi_b.pins[53])
        self.hdmi1.data[0].p.signal.connect(self.hdi_b.pins[57])
        self.hdmi1.data[0].n.signal.connect(self.hdi_b.pins[59])

        # Clock pair
        self.hdmi1.clock.p.signal.connect(self.hdi_b.pins[63])
        self.hdmi1.clock.n.signal.connect(self.hdi_b.pins[65])

        # I2C and control signals
        self.hdmi1.i2c.scl.signal.connect(self.hdi_b.pins[46])
        self.hdmi1.i2c.sda.signal.connect(self.hdi_b.pins[44])
        self.hdmi1.cec.signal.connect(self.hdi_b.pins[48])
        self.hdmi1.hotplug.signal.connect(self.hdi_b.pins[42])

        # USBS2
        self.usb2.usb_if.d.p.signal.connect(self.hdi_b.pins[4])
        self.usb2.usb_if.d.n.signal.connect(self.hdi_b.pins[2])

        # UART
        F.Net.with_name("UART_TX").part_of.connect(self.gpio[13].signal, self.uart_tx.signal)
        F.Net.with_name("UART_RX").part_of.connect(self.gpio[14].signal, self.uart_rx.signal)

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
            0,
            1,
            6,
            7,
            12,
            13,
            20,
            21,
            22,
            31,
            32,
            41,
            42,
            51,
            52,
            58,
            59,
            64,
            65,
            70,
            73,
            97,
        ]

        for pin in gnd_pins_hdi_a:
            self.power_5v.lv.connect(self.hdi_a.pins[pin])

        gnd_pins_hdi_b = [
            6,
            7,
            12,
            13,
            18,
            19,
            24,
            25,
            30,
            31,
            36,
            37,
            43,
            54,
            55,
            60,
            61,
            66,
            67,
            72,
            73,
            78,
            79,
            84,
            85,
            90,
            91,
            96,
            97,
        ]

        for pin in gnd_pins_hdi_b:
            self.power_5v.lv.connect(self.hdi_b.pins[pin])

        # GPIO mapping
        gpio_mapping = {
            2: 57,
            3: 55,
            4: 53,
            5: 33,
            6: 29,
            7: 36,
            8: 38,
            9: 39,
            10: 43,
            11: 37,
            12: 30,
            13: 27,
            14: 54,
            15: 50,
            16: 28,
            17: 49,
            18: 48,
            19: 25,
            20: 26,
            21: 24,
            22: 45,
            23: 46,
            24: 44,
            25: 40,
            26: 23,
            27: 47,
        }

        for gpio_num, pin_num in gpio_mapping.items():
            self.gpio[gpio_num].signal.connect(self.hdi_a.pins[pin_num])

        # GPIO Reference voltage setter
        if self.gpio_ref_voltage == GPIO_Ref_Voltages.V1_8:
            self.power_1v8.hv.connect(self.hdi_a.pins[77])
        else:
            self.power_3v3.hv.connect(self.hdi_a.pins[77])

        # Ethernet
        self.ethernet.pairs[1].p.signal.connect(self.hdi_a.pins[3])
        self.ethernet.pairs[1].n.signal.connect(self.hdi_a.pins[5])
        self.ethernet.pairs[0].n.signal.connect(self.hdi_a.pins[9])
        self.ethernet.pairs[0].p.signal.connect(self.hdi_a.pins[11])
        self.ethernet.pairs[3].p.signal.connect(self.hdi_a.pins[2])
        self.ethernet.pairs[3].n.signal.connect(self.hdi_a.pins[4])
        self.ethernet.pairs[2].n.signal.connect(self.hdi_a.pins[8])
        self.ethernet.pairs[2].p.signal.connect(self.hdi_a.pins[10])

        # Ethernet LED signals
        self.ethernet.led_link.signal.connect(self.hdi_a.pins[14])
        self.ethernet.led_speed.signal.connect(self.hdi_a.pins[16])

        # I2S
        self.i2s.sck.connect(self.gpio[18])
        self.i2s.ws.connect(self.gpio[19])
        self.i2s.sd.connect(self.gpio[21])

        # I2C
        self.i2c.scl.signal.connect(self.hdi_a.pins[79])
        self.i2c.sda.signal.connect(self.hdi_a.pins[81])

        # Power LEDs
        self.power_led_buffer.power.connect(self.power_3v3)
        self.power_led_buffer.input.signal.connect(self.hdi_a.pins[95])
        self.power_3v3.hv.connect_via(
            [self.power_led, self.power_led_resistor], self.power_led_buffer.output.signal
        )

        # Activity LED
        self.power_3v3.hv.connect_via([self.activity_led, self.activity_led_resistor], self.hdi_a.pins[19])

        # Net name overrides
        F.Net.with_name("VCC_5V").part_of.connect(self.power_5v.hv)
        F.Net.with_name("VCC_3V3").part_of.connect(self.power_3v3.hv)
        F.Net.with_name("VCC_1V8").part_of.connect(self.power_1v8.hv)
        F.Net.with_name("GND").part_of.connect(self.power_5v.lv)
        F.Net.with_name("SCL").part_of.connect(self.i2c.scl.signal)
        F.Net.with_name("SDA").part_of.connect(self.i2c.sda.signal)
        F.Net.with_name("HDMI0_D0_P").part_of.connect(self.hdmi0.data[0].p.signal)
        F.Net.with_name("HDMI0_D0_N").part_of.connect(self.hdmi0.data[0].n.signal)
        F.Net.with_name("HDMI0_D1_P").part_of.connect(self.hdmi0.data[1].p.signal)
        F.Net.with_name("HDMI0_D1_N").part_of.connect(self.hdmi0.data[1].n.signal)
        F.Net.with_name("HDMI0_D2_P").part_of.connect(self.hdmi0.data[2].p.signal)
        F.Net.with_name("HDMI0_D2_N").part_of.connect(self.hdmi0.data[2].n.signal)
        F.Net.with_name("HDMI0_CK_P").part_of.connect(self.hdmi0.clock.p.signal)
        F.Net.with_name("HDMI0_CK_N").part_of.connect(self.hdmi0.clock.n.signal)
        F.Net.with_name("HDMI0_CEC").part_of.connect(self.hdmi0.cec.signal)
        F.Net.with_name("HDMI0_HOTPLUG").part_of.connect(self.hdmi0.hotplug.signal)
        F.Net.with_name("HDMI1_D0_P").part_of.connect(self.hdmi1.data[0].p.signal)
        F.Net.with_name("HDMI1_D0_N").part_of.connect(self.hdmi1.data[0].n.signal)
        F.Net.with_name("HDMI1_D1_P").part_of.connect(self.hdmi1.data[1].p.signal)
        F.Net.with_name("HDMI1_D1_N").part_of.connect(self.hdmi1.data[1].n.signal)
        F.Net.with_name("HDMI1_D2_P").part_of.connect(self.hdmi1.data[2].p.signal)
        F.Net.with_name("HDMI1_D2_N").part_of.connect(self.hdmi1.data[2].n.signal)
        F.Net.with_name("HDMI1_CK_P").part_of.connect(self.hdmi1.clock.p.signal)
        F.Net.with_name("HDMI1_CK_N").part_of.connect(self.hdmi1.clock.n.signal)
        F.Net.with_name("HDMI1_CEC").part_of.connect(self.hdmi1.cec.signal)
        F.Net.with_name("HDMI1_HOTPLUG").part_of.connect(self.hdmi1.hotplug.signal)
        F.Net.with_name("USB2_D_P").part_of.connect(self.usb2.usb_if.d.p.signal)
        F.Net.with_name("USB2_D_N").part_of.connect(self.usb2.usb_if.d.n.signal)
        F.Net.with_name("ETH_P0_P").part_of.connect(self.ethernet.pairs[0].p.signal)
        F.Net.with_name("ETH_P0_N").part_of.connect(self.ethernet.pairs[0].n.signal)
        F.Net.with_name("ETH_P1_P").part_of.connect(self.ethernet.pairs[1].p.signal)
        F.Net.with_name("ETH_P1_N").part_of.connect(self.ethernet.pairs[1].n.signal)
        F.Net.with_name("ETH_P2_P").part_of.connect(self.ethernet.pairs[2].p.signal)
        F.Net.with_name("ETH_P2_N").part_of.connect(self.ethernet.pairs[2].n.signal)
        F.Net.with_name("ETH_P3_P").part_of.connect(self.ethernet.pairs[3].p.signal)
        F.Net.with_name("ETH_P3_N").part_of.connect(self.ethernet.pairs[3].n.signal)
        F.Net.with_name("ETH_LED_LINK").part_of.connect(self.ethernet.led_link.signal)
        F.Net.with_name("ETH_LED_ACTIVITY").part_of.connect(
            self.ethernet.led_speed.signal
        )
        F.Net.with_name("I2S_SCK").part_of.connect(self.i2s.sck.signal)
        F.Net.with_name("I2S_WS").part_of.connect(self.i2s.ws.signal)
        F.Net.with_name("I2S_SD").part_of.connect(self.i2s.sd.signal)
        F.Net.with_name("PWR_LED").part_of.connect(self.power_led_buffer.input.signal)

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        # self.power_5v.voltage.constrain_subset(L.Range.from_center_rel(5 * P.V, 0.05))
        # self.power_3v3.voltage.constrain_subset(
        #     L.Range.from_center_rel(3.3 * P.V, 0.05)
        # )
        # self.power_1v8.voltage.constrain_subset(
        #     L.Range.from_center_rel(1.8 * P.V, 0.05)
        # )

        self.power_3v3.connect(
            F.ElectricLogic.connect_all_node_references(
                nodes=self.gpio
                + [self.i2c, self.hdmi0, self.hdmi1, self.ethernet, self.usb2, self.i2s]
            )
        )

        if self.gpio_ref_voltage == GPIO_Ref_Voltages.V1_8:
            self.gpio_ref.voltage.constrain_subset(self.power_1v8.voltage)
            self.gpio_ref.connect(self.power_1v8)
        else:
            self.gpio_ref.voltage.constrain_subset(self.power_3v3.voltage)
            self.gpio_ref.connect(self.power_3v3)
