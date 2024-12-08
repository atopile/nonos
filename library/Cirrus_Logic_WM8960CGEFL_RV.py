# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class Cirrus_Logic_WM8960CGEFL_RV(Module):
    """
    TODO: Docstring describing your module

    QFN-32-EP(5x5) Audio Interface ICs ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    MICBIAS: F.Electrical  # pin: 1
    LINPUT3_JD2: F.Electrical  # pin: 2
    LINPUT2: F.Electrical  # pin: 3
    LINPUT1: F.Electrical  # pin: 4
    RINPUT1: F.Electrical  # pin: 5
    RINPUT2: F.Electrical  # pin: 6
    RINPUT3_JD3: F.Electrical  # pin: 7
    DCVDD: F.Electrical  # pin: 8
    DGND: F.Electrical  # pin: 9
    DBVDD: F.Electrical  # pin: 10
    MCLK: F.Electrical  # pin: 11
    BCLK: F.Electrical  # pin: 12
    DACLRC: F.Electrical  # pin: 13
    DACDAT: F.Electrical  # pin: 14
    ADCLRC: F.Electrical  # pin: 15
    ADCDAT: F.Electrical  # pin: 16
    SCLK: F.Electrical  # pin: 17
    SDIN: F.Electrical  # pin: 18
    SPK_RN: F.Electrical  # pin: 19
    SPKGND2: F.Electrical  # pin: 20
    SPKVDD2: F.Electrical  # pin: 21
    SPK_RP: F.Electrical  # pin: 22
    SPK_LN: F.Electrical  # pin: 23
    SPKGND1: F.Electrical  # pin: 24
    SPK_LP: F.Electrical  # pin: 25
    SPKVDD1: F.Electrical  # pin: 26
    VMID: F.Electrical  # pin: 27
    AGND: F.Electrical  # pin: 28
    HP_R: F.Electrical  # pin: 29
    OUT3: F.Electrical  # pin: 30
    HP_L: F.Electrical  # pin: 31
    AVDD: F.Electrical  # pin: 32
    EP: F.Electrical  # pin: 33

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C18752"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Cirrus Logic",
            DescriptiveProperties.partno: "WM8960CGEFL/RV",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_1809192324_Cirrus-Logic-WM8960CGEFL-RV_C18752.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.MICBIAS,
                "2": self.LINPUT3_JD2,
                "3": self.LINPUT2,
                "4": self.LINPUT1,
                "5": self.RINPUT1,
                "6": self.RINPUT2,
                "7": self.RINPUT3_JD3,
                "8": self.DCVDD,
                "9": self.DGND,
                "10": self.DBVDD,
                "11": self.MCLK,
                "12": self.BCLK,
                "13": self.DACLRC,
                "14": self.DACDAT,
                "15": self.ADCLRC,
                "16": self.ADCDAT,
                "17": self.SCLK,
                "18": self.SDIN,
                "19": self.SPK_RN,
                "20": self.SPKGND2,
                "21": self.SPKVDD2,
                "22": self.SPK_RP,
                "23": self.SPK_LN,
                "24": self.SPKGND1,
                "25": self.SPK_LP,
                "26": self.SPKVDD1,
                "27": self.VMID,
                "28": self.AGND,
                "29": self.HP_R,
                "30": self.OUT3,
                "31": self.HP_L,
                "32": self.AVDD,
                "33": self.EP,
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
