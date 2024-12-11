# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)


class HCTL_PZ254_2_04_S(Module):
    """
    TODO: Docstring describing your module

    250V 3A Standing paste Policy 2.5mm 260℃@5S 8P 6mm -40℃~+105℃ 2.54mm Double Row Black 2.54mm 2x4P SMD,P=2.54mm
    Pin Headers ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    unnamed = L.list_field(8, F.Electrical)

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("HDR")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "HCTL",
            DescriptiveProperties.partno: "PZ254-2-04-S",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2312170041_HCTL-PZ254-2-04-S_C3294462.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.unnamed[0],
                "2": self.unnamed[7],
                "3": self.unnamed[2],
                "4": self.unnamed[5],
                "5": self.unnamed[4],
                "6": self.unnamed[3],
                "7": self.unnamed[6],
                "8": self.unnamed[1],
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


class SaleaeHeader(Module):
    pins = L.list_field(4, F.ElectricLogic)
    connector: HCTL_PZ254_2_04_S
    reference: F.ElectricPower

    @L.rt_field
    def single_electric_reference(self):
        return F.has_single_electric_reference_defined(
            F.ElectricLogic.connect_all_module_references(self)
        )

    def __preinit__(self):
        self.pins[0].signal.connect(self.connector.unnamed[1])
        self.pins[1].signal.connect(self.connector.unnamed[3])
        self.pins[2].signal.connect(self.connector.unnamed[5])
        self.pins[3].signal.connect(self.connector.unnamed[7])
        self.reference.lv.connect(
            self.connector.unnamed[0],
            self.connector.unnamed[2],
            self.connector.unnamed[4],
            self.connector.unnamed[6]
        )


