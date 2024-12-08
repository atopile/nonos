# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class NXP_Semicon_MPR121QR2(Module):
    """
    TODO: Docstring describing your module

    QFN-20(3x3) Touch Sensors ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    IRQh: F.Electrical  # pin: 1
    SCL: F.Electrical  # pin: 2
    SDA: F.Electrical  # pin: 3
    ADDR: F.Electrical  # pin: 4
    VREG: F.Electrical  # pin: 5
    VSS: F.Electrical  # pin: 6
    REXT: F.Electrical  # pin: 7
    ELE0: F.Electrical  # pin: 8
    ELE1: F.Electrical  # pin: 9
    ELE2: F.Electrical  # pin: 10
    ELE3: F.Electrical  # pin: 11
    ELE4: F.Electrical  # pin: 12
    ELE5: F.Electrical  # pin: 13
    ELE6: F.Electrical  # pin: 14
    ELE7: F.Electrical  # pin: 15
    ELE8: F.Electrical  # pin: 16
    ELE9: F.Electrical  # pin: 17
    ELE10: F.Electrical  # pin: 18
    ELE11: F.Electrical  # pin: 19
    VDD: F.Electrical  # pin: 20

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C91322"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "NXP Semicon",
            DescriptiveProperties.partno: "MPR121QR2",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2407101627_NXP-Semicon-MPR121QR2_C91322.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.IRQh,
                "2": self.SCL,
                "3": self.SDA,
                "4": self.ADDR,
                "5": self.VREG,
                "6": self.VSS,
                "7": self.REXT,
                "8": self.ELE0,
                "9": self.ELE1,
                "10": self.ELE2,
                "11": self.ELE3,
                "12": self.ELE4,
                "13": self.ELE5,
                "14": self.ELE6,
                "15": self.ELE7,
                "16": self.ELE8,
                "17": self.ELE9,
                "18": self.ELE10,
                "19": self.ELE11,
                "20": self.VDD,
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
