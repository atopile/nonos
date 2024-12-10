# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

from .Ethernet import GigabitEthernet

logger = logging.getLogger(__name__)


class _HANRUNZhongshan_HanRun_Elec_HR911130A(Module):
    """
    RJ45Receptacle 1 WithLED Plugin Ethernet Connectors / Modular Connectors (RJ45 RJ11) ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    MDI0plus: F.Electrical  # pin: MDI0+
    MDI0_: F.Electrical  # pin: MDI0-
    MDI1plus: F.Electrical  # pin: MDI1+
    MDI1_: F.Electrical  # pin: MDI1-
    MDI2plus: F.Electrical  # pin: MDI2+
    MDI2_: F.Electrical  # pin: MDI2-
    MDI3plus: F.Electrical  # pin: MDI3+
    MDI3_: F.Electrical  # pin: MDI3-
    P1: F.Electrical  # pin: P1
    P10: F.Electrical  # pin: P10
    SHIELD0: F.Electrical  # pin: SHIELD0
    SHIELD1: F.Electrical  # pin: SHIELD1
    unnamed = L.list_field(4, F.Electrical)

    link_led: F.LED
    speed_led: F.LED

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C54408"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("RJ")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "HANRUN(Zhongshan HanRun Elec)",
            DescriptiveProperties.partno: "HR911130A",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_1811141815_HANRUN-Zhongshan-HanRun-Elec-HR911130A_C54408.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "11": self.unnamed[2],
                "12": self.unnamed[3],
                "13": self.unnamed[1],
                "14": self.unnamed[0],
                "P2": self.MDI0plus,
                "P3": self.MDI0_,
                "P4": self.MDI1plus,
                "P7": self.MDI1_,
                "P5": self.MDI2plus,
                "P6": self.MDI2_,
                "P8": self.MDI3plus,
                "P9": self.MDI3_,
                "P1": self.P1,
                "P10": self.P10,
                "SHIELD0": self.SHIELD0,
                "SHIELD1": self.SHIELD1,
            }
        )

    def __preinit__(self):
        # Connections
        self.link_led.cathode.connect(self.unnamed[2])
        self.link_led.anode.connect(self.unnamed[3])
        self.speed_led.cathode.connect(self.unnamed[0])
        self.speed_led.anode.connect(self.unnamed[1])
        
        # Parameters
        self.link_led.color.alias_is(F.LED.Color.GREEN)
        self.link_led.forward_voltage.alias_is(2.1 * P.V)
        self.link_led.max_current.alias_is(10 * P.mA)
        self.speed_led.color.alias_is(F.LED.Color.YELLOW)
        self.speed_led.forward_voltage.alias_is(2.1 * P.V)
        self.speed_led.max_current.alias_is(10 * P.mA)

class HANRUNZhongshan_HanRun_Elec_HR911130A(Module):
    """
    RJ45Receptacle 1 WithLED Plugin Ethernet Connectors / Modular Connectors (RJ45 RJ11) ROHS
    """

    ethernet: F.Ethernet
    power_led: F.ElectricPower
    connector: _HANRUNZhongshan_HanRun_Elec_HR911130A
    # link_led = L.f_field(F.LEDIndicator)(use_mosfet=False)
    # speed_led = L.f_field(F.LEDIndicator)(use_mosfet=False)

    link_led_resistor: F.Resistor
    speed_led_resistor: F.Resistor

    def __preinit__(self):
        self.ethernet.pairs[0].p.signal.connect(self.connector.MDI0plus)
        self.ethernet.pairs[0].n.signal.connect(self.connector.MDI0_)
        self.ethernet.pairs[1].p.signal.connect(self.connector.MDI1plus)
        self.ethernet.pairs[1].n.signal.connect(self.connector.MDI1_)
        self.ethernet.pairs[2].p.signal.connect(self.connector.MDI2plus)
        self.ethernet.pairs[2].n.signal.connect(self.connector.MDI2_)
        self.ethernet.pairs[3].p.signal.connect(self.connector.MDI3plus)
        self.ethernet.pairs[3].n.signal.connect(self.connector.MDI3_)

        # link and speed LEDs
        # self.ethernet.led_link.connect(self.link_led.logic_in)
        # self.ethernet.led_speed.connect(self.speed_led.logic_in)

        # self.link_led.led.led.specialize(self.connector.link_led)
        # self.speed_led.led.led.specialize(self.connector.speed_led)

        self.power_led.hv.connect_via([self.link_led_resistor, self.connector.link_led], self.ethernet.led_link.signal)
        self.power_led.hv.connect_via([self.speed_led_resistor, self.connector.speed_led], self.ethernet.led_speed.signal)

        self.link_led_resistor.resistance.constrain_subset(L.Range.from_center_rel(470 * P.ohm, 0.05))
        self.speed_led_resistor.resistance.constrain_subset(L.Range.from_center_rel(470 * P.ohm, 0.05))

        # shield
        self.ethernet.single_electric_reference.get_reference().lv.connect(
            self.connector.SHIELD0, self.connector.SHIELD1
        )
