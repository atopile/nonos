# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)


class _Texas_Instruments_TPS56637RPAR(Module):
    """
    TODO: Docstring describing your module

    Step-down type Adjustable 4.5V~28V 600mV~13V 6A VQFN-10-HR(3x3) DC-DC Converters ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    EN: F.Electrical  # pin: 1
    FB: F.Electrical  # pin: 2
    AGND: F.Electrical  # pin: 3
    PG: F.Electrical  # pin: 4
    SW: F.Electrical  # pin: 6
    BOOT: F.Electrical  # pin: 7
    VIN: F.Electrical  # pin: 8
    PGND: F.Electrical  # pin: 9
    MODE: F.Electrical  # pin: 10

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C841386"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Texas Instruments",
            DescriptiveProperties.partno: "TPS56637RPAR",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.ti.com/cn/lit/gpn/tps56637"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.EN,
                "2": self.FB,
                "3": self.AGND,
                "4": self.PG,
                "5": None,
                "6": self.SW,
                "7": self.BOOT,
                "8": self.VIN,
                "9": self.PGND,
                "10": self.MODE,
            }
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass


class Texas_Instruments_TPS56637RPAR(Module):
    """
    Step-down type Adjustable 4.5V~28V 600mV~13V 6A VQFN-10-HR(3x3) DC-DC Converters ROHS
    """

    # Interfaces
    power_in: F.ElectricPower
    power_out: F.ElectricPower

    # Components
    regulator: _Texas_Instruments_TPS56637RPAR
    inductor: F.Inductor
    feedback_rtop: F.Resistor
    feedback_rbottom: F.Resistor
    compensation_resistor: F.Resistor
    compensation_capacitor: F.Capacitor
    boot_capacitor: F.Capacitor
    power_good_resistor: F.Resistor

    def __preinit__(self):
        # Input caps
        INPUT_CAP_PROPERTIES = [
            {"value": 4.7 * P.uF, "footprint": "0805"},
            {"value": 4.7 * P.uF, "footprint": "0805"},
            {"value": 4.7 * P.uF, "footprint": "0805"},
            {"value": 100 * P.nF, "footprint": "0402"},
        ]

        INPUT_CAPS = []
        for props in INPUT_CAP_PROPERTIES:
            cap = self.power_in.decoupled.decouple(owner=self)
            cap.add(F.has_package_requirement(props["footprint"]))
            cap.capacitance.constrain_subset(
                L.Range.from_center_rel(props["value"], 0.2)
            )
            INPUT_CAPS.append(cap)

        output_cap = self.power_out.decoupled.decouple(owner=self)
        output_cap.add(F.has_package_requirement("0805"))
        output_cap.capacitance.constrain_subset(L.Range.from_center_rel(47 * P.uF, 0.2))

        # Connections to regulator ic
        self.power_in.hv.connect(self.regulator.VIN)
        self.power_out.hv.connect_via(self.inductor, self.regulator.SW)
        self.power_out.hv.connect_via(self.power_good_resistor, self.regulator.PG)
        self.power_out.hv.connect_via(
            [self.compensation_resistor, self.compensation_capacitor], self.regulator.FB
        )
        self.regulator.BOOT.connect_via(self.boot_capacitor, self.regulator.SW)
        self.power_out.hv.connect_via(self.feedback_rtop, self.regulator.FB)
        self.power_out.lv.connect_via(self.feedback_rbottom, self.regulator.FB)
        self.power_out.lv.connect(
            self.regulator.AGND,
            self.regulator.PGND,
            self.regulator.MODE,
            self.power_in.lv,
        )

        # Parameters
        # self.inductor.inductance.constrain_subset(L.Range.from_center_rel(3.3 * P.uH, 0.4))
        # self.inductor.max_current.constrain_subset(L.Range(4 * P.A, 6 * P.A))
        self.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C602030"}))
        self.power_good_resistor.resistance.constrain_subset(
            L.Range.from_center_rel(100 * P.kohm, 0.2)
        )
        self.feedback_rtop.resistance.constrain_subset(
            L.Range.from_center_rel(73.2 * P.kohm, 0.2)
        )
        self.feedback_rbottom.resistance.constrain_subset(
            L.Range.from_center_rel(10 * P.kohm, 0.2)
        )
        self.compensation_resistor.resistance.constrain_subset(
            L.Range.from_center_rel(20 * P.kohm, 0.2)
        )
        self.compensation_capacitor.capacitance.constrain_subset(
            L.Range.from_center_rel(100 * P.pF, 0.2)
        )
        self.boot_capacitor.capacitance.constrain_subset(
            L.Range.from_center_rel(100 * P.nF, 0.2)
        )

        # Packages
        for component in [
            self.power_good_resistor,
            self.feedback_rtop,
            self.feedback_rbottom,
            self.compensation_resistor,
            self.compensation_capacitor,
            self.boot_capacitor,
        ]:
            component.add(F.has_package_requirement("0402"))
