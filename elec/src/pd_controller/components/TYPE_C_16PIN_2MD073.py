# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class TYPE_C_16PIN_2MD073(Module):
    """
    5A 1 Horizontal attachment 16P Female -25℃~+85℃ Type-C SMD
    USB Connectors ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    POWER_VBUS: F.ElectricPower
    USB2: F.USB2_0_IF.Data

    SBU2: F.ElectricLogic
    SBU1: F.ElectricLogic
    CC1: F.ElectricLogic
    CC2: F.ElectricLogic

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C2765186"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("USB")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "SHOU HAN",
            DescriptiveProperties.partno: "TYPE-C 16PIN 2MD(073)",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2111231930_SHOU-HAN-TYPE-C-16PIN-2MD-073_C2765186.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={
                self.CC1.signal: ["CC1"],
                self.CC2.signal: ["CC2"],
                self.USB2.n.signal: ["DN1", "DN2"],
                self.USB2.p.signal: ["DP1", "DP2"],
                self.SBU1.signal: ["SBU1"],
                self.SBU2.signal: ["SBU2"],
                self.POWER_VBUS.lv: ["SHELL", "GND"],
                self.POWER_VBUS.hv: ["VBUS"],
            },
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------
        # self.POWER_VBUS.connect(
        #     self.CC1.reference,
        #     self.CC2.reference,
        #     self.SBU1.reference,
        #     self.SBU2.reference,
        # ) # TODO: Fix reference
        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.CC1.reference.voltage.constrain_subset(L.Range(0 * P.V, 3.6 * P.V))
        self.CC2.reference.voltage.constrain_subset(L.Range(0 * P.V, 3.6 * P.V))
        self.SBU1.reference.voltage.constrain_subset(L.Range(0 * P.V, 3.6 * P.V))
        self.SBU2.reference.voltage.constrain_subset(L.Range(0 * P.V, 3.6 * P.V))
        self.POWER_VBUS.voltage.constrain_subset(L.Range(0 * P.V, 20 * P.V))
