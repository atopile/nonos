# SPDX-License-Identifier: MIT

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.brightness import TypicalLuminousIntensity
from faebryk.libs.units import P  # noqa: F401

# Components
from components.TYPE_C_16PIN_2MD073 import TYPE_C_16PIN_2MD073
from components.STUSB4500 import STUSB4500QTR
from components.ESDA25W import ESDA25W
from components.ESDA25P35_1U1M import ESDA25P35_1U1M
from components.XT30 import XT30PW
from components.STEMMA import STEMMA_RIGHT_ANGLE


class App(Module):
    PD_CONTROLLER: STUSB4500QTR
    USB_CONNECTOR: TYPE_C_16PIN_2MD073
    ESD_CC: ESDA25W
    VSINK_MOSFET: F.MOSFET
    XT30PW: XT30PW
    STEMMA: STEMMA_RIGHT_ANGLE
    VSYNC_LED: F.PoweredLED
    PDO2_LED: F.PoweredLED
    PDO3_LED: F.PoweredLED

    # Passive components
    VBUS_VS_DISCH_R: F.Resistor
    Vreg_2V7_CAP: F.Capacitor
    Vreg_1V2_CAP: F.Capacitor
    VBUS_CAP: F.Capacitor
    VBUS_ESD_DIODE: ESDA25P35_1U1M
    VSINK_ESD_DIODE: ESDA25P35_1U1M
    VSINK_GATE_R: F.Resistor
    VSINK_GATE_PULLUP: F.Resistor
    VSINK_GATE_SNUB_R: F.Resistor
    VSINK_GATE_SNUB_C: F.Capacitor
    DISCH_R: F.Resistor

    VSINK: F.ElectricPower
    VMCU: F.ElectricPower
    VBUS: F.ElectricPower
    I2C: F.I2C

    def __preinit__(self):
        # Tie gnd together
        gnd = F.Net.with_name("GND")
        gnd.part_of.connect(
            self.VSINK.lv,
            self.VBUS.lv,
            self.VMCU.lv,
            self.PD_CONTROLLER.VDD.lv,
            self.PD_CONTROLLER.VREG_1V2.lv,
            self.PD_CONTROLLER.VREG_2V7.lv,
        )

        F.ElectricLogic.connect_all_module_references(self, gnd_only=True)

        # USB connector
        self.USB_CONNECTOR.POWER_VBUS.connect(self.VBUS)
        self.USB_CONNECTOR.CC1.connect(self.PD_CONTROLLER.CC1, self.PD_CONTROLLER.CC1DB)
        self.USB_CONNECTOR.CC2.connect(self.PD_CONTROLLER.CC2, self.PD_CONTROLLER.CC2DB)

        self.VBUS_VS_DISCH_R.resistance.merge(F.Range.from_center_rel(1 * P.kohm, 0.01))
        self.VBUS_VS_DISCH_R.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VBUS.hv.connect_via(self.VBUS_VS_DISCH_R, self.PD_CONTROLLER.VBUS_VS_DISCH)

        # Output connector
        self.XT30PW.power.connect(self.VSINK)

        # LEDs
        self.VSYNC_LED.power.connect(self.VSINK)
        self.PDO2_LED.power.connect(self.VSINK)
        self.PDO3_LED.power.connect(self.VSINK)

        for led in [self.VSYNC_LED, self.PDO2_LED, self.PDO3_LED]:
            led.led.color.merge(F.LED.Color.BLUE)
            led.add(F.has_footprint_requirement_defined([("0402", 2)]))
            led.led.brightness.merge(
                TypicalLuminousIntensity.APPLICATION_LED_INDICATOR_INSIDE.value.value
            )

        # I2C
        self.STEMMA.i2c.connect(self.I2C)
        self.PD_CONTROLLER
        self.STEMMA.power.connect(self.VMCU)

        # Internal rail decoupling
        self.Vreg_2V7_CAP.unnamed[0].connect(self.PD_CONTROLLER.VREG_2V7.lv)
        self.Vreg_2V7_CAP.unnamed[1].connect(self.PD_CONTROLLER.VREG_2V7.hv)
        self.Vreg_2V7_CAP.capacitance.merge(
            F.Range.from_center_rel(1 * P.uF, 0.2)
        )
        self.Vreg_2V7_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))

        self.Vreg_1V2_CAP.unnamed[0].connect(self.PD_CONTROLLER.VREG_1V2.lv)
        self.Vreg_1V2_CAP.unnamed[1].connect(self.PD_CONTROLLER.VREG_1V2.hv)
        self.Vreg_1V2_CAP.capacitance.merge(
            F.Range.from_center_rel(1 * P.uF, 0.2)
        )
        self.Vreg_1V2_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))

        # Regulator rail net naming
        vreg_2v7 = F.Net.with_name("VREG_2V7")
        vreg_1v2 = F.Net.with_name("VREG_1V2")
        vreg_2v7.part_of.connect(self.PD_CONTROLLER.VREG_2V7.hv)
        vreg_1v2.part_of.connect(self.PD_CONTROLLER.VREG_1V2.hv)

        self.VBUS_CAP.unnamed[0].connect(self.VBUS.lv)
        self.VBUS_CAP.unnamed[1].connect(self.VBUS.hv)
        self.VBUS_CAP.capacitance.merge(F.Range.from_center_rel(4.7 * P.uF, 0.3))
        self.VBUS_CAP.add(F.has_footprint_requirement_defined([("0603", 2)]))
        self.VBUS_CAP.rated_voltage.merge(F.Range(30 * P.V, float("inf") * P.V))

        self.VBUS.connect(self.PD_CONTROLLER.VDD)

        # VBUS net naming
        vbus = F.Net.with_name("VBUS") 
        vbus.part_of.connect(self.VBUS.hv)

        # ESD protection
        self.VBUS.hv.connect_via(self.VBUS_ESD_DIODE, self.VBUS.lv)
        self.VSINK.hv.connect_via(self.VSINK_ESD_DIODE, self.VSINK.lv)
        self.PD_CONTROLLER.CC1.signal.connect(self.ESD_CC.K1)
        self.PD_CONTROLLER.CC2.signal.connect(self.ESD_CC.K2)
        self.VBUS.lv.connect(self.ESD_CC.A)

        # CC line net naming
        cc1 = F.Net.with_name("CC1")
        cc2 = F.Net.with_name("CC2")
        cc1.part_of.connect(self.PD_CONTROLLER.CC1.signal)
        cc2.part_of.connect(self.PD_CONTROLLER.CC2.signal)

        # VSINK SWITCH
        self.VSINK_MOSFET.channel_type.merge(F.MOSFET.ChannelType.P_CHANNEL)
        self.VSINK_MOSFET.add(F.has_descriptive_properties_defined({"LCSC": "C471913"}))
        # VBUS to VSINK switching
        self.VBUS.hv.connect_via(self.VSINK_MOSFET, self.VSINK.hv)

        # VSINK voltage divider for VCC
        self.VSINK_VCC = F.Net.with_name("VSINK_VCC")
        self.VSINK_VCC.part_of.connect(self.VSINK.hv)

        # Gate pullup resistor divider
        self.VSINK_GATE_R.resistance.merge(F.Range.from_center_rel(22 * P.kohm, 0.03))
        self.VSINK_GATE_R.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VSINK_MOSFET.gate.connect_via(
            self.VSINK_GATE_R, self.PD_CONTROLLER.VBUS_EN_SNK
        )

        # Gate to drain pullup resistor
        self.VSINK_GATE_PULLUP.resistance.merge(
            F.Range.from_center_rel(100 * P.kohm, 0.02)
        )
        self.VSINK_GATE_PULLUP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VSINK_MOSFET.gate.connect_via(
            self.VSINK_GATE_PULLUP, self.VSINK_MOSFET.drain
        )

        # Gate to source RC snubber
        self.VSINK_GATE_SNUB_R.resistance.merge(
            F.Range.from_center_rel(100 * P.ohm, 0.01)
        )
        self.VSINK_GATE_SNUB_R.add(F.has_footprint_requirement_defined([("0201", 2)]))

        self.VSINK_GATE_SNUB_C.capacitance.merge(
            F.Range.from_center_rel(100 * P.nF, 0.2)
        )
        self.VSINK_GATE_SNUB_C.add(F.has_footprint_requirement_defined([("0201", 2)]))

        # Connect RC snubber between gate and source
        self.VSINK_MOSFET.gate.connect_via(
            [self.VSINK_GATE_SNUB_R, self.VSINK_GATE_SNUB_C], self.VSINK_MOSFET.source
        )

        # DISCH resistor
        self.DISCH_R.resistance.merge(F.Range.from_center_rel(1 * P.kohm, 0.01))
        self.DISCH_R.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VBUS.hv.connect_via(self.DISCH_R, self.PD_CONTROLLER.DISCH)

        # I2C nets
        self.I2C_SCL = F.Net.with_name("I2C_SCL")
        self.I2C_SDA = F.Net.with_name("I2C_SDA")
        self.I2C.scl.signal.connect(self.I2C_SCL.part_of)
        self.I2C.sda.signal.connect(self.I2C_SDA.part_of)

        self.I2C.connect(self.PD_CONTROLLER.I2C)

        self.I2C.terminate()
        for line in [self.I2C.sda, self.I2C.scl]:
            for r in line.get_trait(F.ElectricLogic.has_pulls).get_pulls():
                if r is None:
                    continue
                r.resistance.merge(F.Range.from_center_rel(4.7 * P.kohm, 0.03))
                r.add(F.has_footprint_requirement_defined([("0201", 2)]))


        F.ElectricLogic.connect_all_node_references(
            [self.VMCU]
            + [self.I2C]
        )
        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.VSINK.voltage.merge(F.Range(5 * P.V, 20 * P.V))
        self.VMCU.voltage.merge(F.Range(0 * P.V, 3.6 * P.V))
        self.VBUS.voltage.merge(F.Range(5 * P.V, 20 * P.V))
