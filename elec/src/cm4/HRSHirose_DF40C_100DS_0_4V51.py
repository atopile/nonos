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
    pins = L.list_field(100, F.Electrical)

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
                "1": self.pins[0],
                "2": self.pins[1],
                "3": self.pins[2],
                "4": self.pins[3],
                "5": self.pins[4],
                "6": self.pins[5],
                "7": self.pins[6],
                "8": self.pins[7],
                "9": self.pins[8],
                "10": self.pins[9],
                "11": self.pins[10],
                "12": self.pins[11],
                "13": self.pins[12],
                "14": self.pins[13],
                "15": self.pins[14],
                "16": self.pins[15],
                "17": self.pins[16],
                "18": self.pins[17],
                "19": self.pins[18],
                "20": self.pins[19],
                "21": self.pins[20],
                "22": self.pins[21],
                "23": self.pins[22],
                "24": self.pins[23],
                "25": self.pins[24],
                "26": self.pins[25],
                "27": self.pins[26],
                "28": self.pins[27],
                "29": self.pins[28],
                "30": self.pins[29],
                "31": self.pins[30],
                "32": self.pins[31],
                "33": self.pins[32],
                "34": self.pins[33],
                "35": self.pins[34],
                "36": self.pins[35],
                "37": self.pins[36],
                "38": self.pins[37],
                "39": self.pins[38],
                "40": self.pins[39],
                "41": self.pins[40],
                "42": self.pins[41],
                "43": self.pins[42],
                "44": self.pins[43],
                "45": self.pins[44],
                "46": self.pins[45],
                "47": self.pins[46],
                "48": self.pins[47],
                "49": self.pins[48],
                "50": self.pins[49],
                "51": self.pins[50],
                "52": self.pins[51],
                "53": self.pins[52],
                "54": self.pins[53],
                "55": self.pins[54],
                "56": self.pins[55],
                "57": self.pins[56],
                "58": self.pins[57],
                "59": self.pins[58],
                "60": self.pins[59],
                "61": self.pins[60],
                "62": self.pins[61],
                "63": self.pins[62],
                "64": self.pins[63],
                "65": self.pins[64],
                "66": self.pins[65],
                "67": self.pins[66],
                "68": self.pins[67],
                "69": self.pins[68],
                "70": self.pins[69],
                "71": self.pins[70],
                "72": self.pins[71],
                "73": self.pins[72],
                "74": self.pins[73],
                "75": self.pins[74],
                "76": self.pins[75],
                "77": self.pins[76],
                "78": self.pins[77],
                "79": self.pins[78],
                "80": self.pins[79],
                "81": self.pins[80],
                "82": self.pins[81],
                "83": self.pins[82],
                "84": self.pins[83],
                "85": self.pins[84],
                "86": self.pins[85],
                "87": self.pins[86],
                "88": self.pins[87],
                "89": self.pins[88],
                "90": self.pins[89],
                "91": self.pins[90],
                "92": self.pins[91],
                "93": self.pins[92],
                "94": self.pins[93],
                "95": self.pins[94],
                "96": self.pins[95],
                "97": self.pins[96],
                "98": self.pins[97],
                "99": self.pins[98],
                "100": self.pins[99],
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
