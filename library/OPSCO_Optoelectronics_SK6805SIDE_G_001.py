# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class OPSCO_Optoelectronics_SK6805SIDE_G_001(Module):
    """
    TODO: Docstring describing your module

    SMD,1.3x3.5mm RGB LEDs(Built-in IC) ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    DOUT: F.Electrical  # pin: 1
    VSS: F.Electrical  # pin: 2
    VDD: F.Electrical  # pin: 3
    DIN: F.Electrical  # pin: 4

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C2909060"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "OPSCO Optoelectronics",
            DescriptiveProperties.partno: "SK6805SIDE-G-001",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2110250930_OPSCO-Optoelectronics-SK6805SIDE-G-001_C2909060.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.DOUT,
                "2": self.VSS,
                "3": self.VDD,
                "4": self.DIN,
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
