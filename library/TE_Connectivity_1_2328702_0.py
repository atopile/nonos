# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class TE_Connectivity_1_2328702_0(Module):
    """
    TODO: Docstring describing your module

    Flip type -40℃~+85℃ 10P Dual-sided contacts / top and bottom connection Horizontal attachment 0.5mm SMD,P=0.5mm,Surface Mount，Right Angle
    FFC, FPC (Flat Flexible) Connector Assemblies ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    unnamed = L.list_field(12, F.Electrical)

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C3167956"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("FPC")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "TE Connectivity",
            DescriptiveProperties.partno: "1-2328702-0",
        }
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.unnamed[0],
                "2": self.unnamed[1],
                "3": self.unnamed[2],
                "4": self.unnamed[3],
                "5": self.unnamed[4],
                "6": self.unnamed[5],
                "7": self.unnamed[6],
                "8": self.unnamed[7],
                "9": self.unnamed[8],
                "10": self.unnamed[9],
                "11": self.unnamed[10],
                "12": self.unnamed[11],
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
