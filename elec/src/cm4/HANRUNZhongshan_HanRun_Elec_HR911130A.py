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

    link_led = L.f_field(F.LEDIndicator)(use_mosfet=False)
    speed_led = L.f_field(F.LEDIndicator)(use_mosfet=False)

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


class HANRUNZhongshan_HanRun_Elec_HR911130A(Module):
    """
    RJ45Receptacle 1 WithLED Plugin Ethernet Connectors / Modular Connectors (RJ45 RJ11) ROHS
    """

    ethernet: GigabitEthernet

    connector: _HANRUNZhongshan_HanRun_Elec_HR911130A
    link_led_current_limiting_resistor: F.Resistor
    speed_led_current_limiting_resistor: F.Resistor

    def __preinit__(self):
        self.ethernet.pair0.p.signal.connect(self.connector.MDI0plus)
        self.ethernet.pair0.n.signal.connect(self.connector.MDI0_)
        self.ethernet.pair1.p.signal.connect(self.connector.MDI1plus)
        self.ethernet.pair1.n.signal.connect(self.connector.MDI1_)
        self.ethernet.pair2.p.signal.connect(self.connector.MDI2plus)
        self.ethernet.pair2.n.signal.connect(self.connector.MDI2_)
        self.ethernet.pair3.p.signal.connect(self.connector.MDI3plus)
        self.ethernet.pair3.n.signal.connect(self.connector.MDI3_)

        # link and speed LEDs
        self.ethernet.led_link.connect(self.connector.link_led.logic_in)
        self.ethernet.led_speed.connect(self.connector.speed_led.logic_in)

        # shield
        self.ethernet.single_electric_reference.get_reference().lv.connect(
            self.connector.SHIELD0, self.connector.SHIELD1
        )
