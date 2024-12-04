# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)


class HRSHirose_DF40C_100DS_0_4V51(Module):
    """
    TODO: Docstring describing your module

    0.4mm 2 -35℃~+85℃ Standing paste 300mA SMD,P=0.4mm Board-to-Board and Backplane Connector ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    unnamed = L.list_field(100, F.Electrical)

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C597931"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("CN")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "HRS(Hirose)",
            DescriptiveProperties.partno: "DF40C-100DS-0.4V(51)",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_HRS-Hirose-DF40C-100DS-0-4V-51_C597931.pdf"
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
                "13": self.unnamed[12],
                "14": self.unnamed[13],
                "15": self.unnamed[14],
                "16": self.unnamed[15],
                "17": self.unnamed[16],
                "18": self.unnamed[17],
                "19": self.unnamed[18],
                "20": self.unnamed[19],
                "21": self.unnamed[20],
                "22": self.unnamed[21],
                "23": self.unnamed[22],
                "24": self.unnamed[23],
                "25": self.unnamed[24],
                "26": self.unnamed[25],
                "27": self.unnamed[26],
                "28": self.unnamed[27],
                "29": self.unnamed[28],
                "30": self.unnamed[29],
                "31": self.unnamed[30],
                "32": self.unnamed[31],
                "33": self.unnamed[32],
                "34": self.unnamed[33],
                "35": self.unnamed[34],
                "36": self.unnamed[35],
                "37": self.unnamed[36],
                "38": self.unnamed[37],
                "39": self.unnamed[38],
                "40": self.unnamed[39],
                "41": self.unnamed[40],
                "42": self.unnamed[41],
                "43": self.unnamed[42],
                "44": self.unnamed[43],
                "45": self.unnamed[44],
                "46": self.unnamed[45],
                "47": self.unnamed[46],
                "48": self.unnamed[47],
                "49": self.unnamed[48],
                "50": self.unnamed[49],
                "51": self.unnamed[50],
                "52": self.unnamed[51],
                "53": self.unnamed[52],
                "54": self.unnamed[53],
                "55": self.unnamed[54],
                "56": self.unnamed[55],
                "57": self.unnamed[56],
                "58": self.unnamed[57],
                "59": self.unnamed[58],
                "60": self.unnamed[59],
                "61": self.unnamed[60],
                "62": self.unnamed[61],
                "63": self.unnamed[62],
                "64": self.unnamed[63],
                "65": self.unnamed[64],
                "66": self.unnamed[65],
                "67": self.unnamed[66],
                "68": self.unnamed[67],
                "69": self.unnamed[68],
                "70": self.unnamed[69],
                "71": self.unnamed[70],
                "72": self.unnamed[71],
                "73": self.unnamed[72],
                "74": self.unnamed[73],
                "75": self.unnamed[74],
                "76": self.unnamed[75],
                "77": self.unnamed[76],
                "78": self.unnamed[77],
                "79": self.unnamed[78],
                "80": self.unnamed[79],
                "81": self.unnamed[80],
                "82": self.unnamed[81],
                "83": self.unnamed[82],
                "84": self.unnamed[83],
                "85": self.unnamed[84],
                "86": self.unnamed[85],
                "87": self.unnamed[86],
                "88": self.unnamed[87],
                "89": self.unnamed[88],
                "90": self.unnamed[89],
                "91": self.unnamed[90],
                "92": self.unnamed[91],
                "93": self.unnamed[92],
                "94": self.unnamed[93],
                "95": self.unnamed[94],
                "96": self.unnamed[95],
                "97": self.unnamed[96],
                "98": self.unnamed[97],
                "99": self.unnamed[98],
                "100": self.unnamed[99],
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
