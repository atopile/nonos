# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)


class _HCTL_HC_TYPE_C_24P_VS9_3_5A_F1_1_04(Module):
    """
    TODO: Docstring describing your module

    5A USB 3.1 1 260℃ Standing paste 24P Female -30℃~+80℃ Gold Copper Alloy Type-C SMD USB Connectors ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    EH: F.Electrical  # pins: 28, 27, 26, 25
    GND: F.Electrical  # pins: B12, B1, A12, A1
    SSTXP1: F.Electrical  # pin: A2
    SSTXN1: F.Electrical  # pin: A3
    VBUS: F.Electrical  # pins: B9, B4, A9, A4
    CC1: F.Electrical  # pin: A5
    DP1: F.Electrical  # pin: A6
    DN1: F.Electrical  # pin: A7
    SBU1: F.Electrical  # pin: A8
    SSRXN2: F.Electrical  # pin: A10
    SSRXP2: F.Electrical  # pin: A11
    SSTXP2: F.Electrical  # pin: B2
    SSTXN2: F.Electrical  # pin: B3
    CC2: F.Electrical  # pin: B5
    DP2: F.Electrical  # pin: B6
    DN2: F.Electrical  # pin: B7
    SBU2: F.Electrical  # pin: B8
    SSRXN1: F.Electrical  # pin: B10
    SSRXP1: F.Electrical  # pin: B11

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "HCTL",
            DescriptiveProperties.partno: "HC-TYPE-C-24P-VS9.3-5A-F1.1-04",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2301120930_HCTL-HC-TYPE-C-24P-VS9-3-5A-F1-1-04_C5342428.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "25": self.EH,
                "26": self.EH,
                "27": self.EH,
                "28": self.EH,
                "A1": self.GND,
                "A2": self.SSTXP1,
                "A3": self.SSTXN1,
                "A4": self.VBUS,
                "A5": self.CC1,
                "A6": self.DP1,
                "A7": self.DN1,
                "A8": self.SBU1,
                "A9": self.VBUS,
                "A10": self.SSRXN2,
                "A11": self.SSRXP2,
                "A12": self.GND,
                "B1": self.GND,
                "B2": self.SSTXP2,
                "B3": self.SSTXN2,
                "B4": self.VBUS,
                "B5": self.CC2,
                "B6": self.DP2,
                "B7": self.DN2,
                "B8": self.SBU2,
                "B9": self.VBUS,
                "B10": self.SSRXN1,
                "B11": self.SSRXP1,
                "B12": self.GND,
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


class HCTL_HC_TYPE_C_24P_VS9_3_5A_F1_1_04(Module):
    """

    5A USB 3.1 1 260℃ Standing paste 24P Female -30℃~+80℃ Gold Copper Alloy Type-C SMD USB Connectors ROHS
    """

    POWER_VBUS: F.ElectricPower
    USB2: F.USB2_0_IF.Data

    SBU2: F.ElectricLogic
    SBU1: F.ElectricLogic
    CC1: F.ElectricLogic
    CC2: F.ElectricLogic

    connector: _HCTL_HC_TYPE_C_24P_VS9_3_5A_F1_1_04

    def __preinit__(self):
        self.POWER_VBUS.hv.connect(self.connector.VBUS)
        self.USB2.p.signal.connect(self.connector.DP1, self.connector.DP2)
        self.USB2.n.signal.connect(self.connector.DN1, self.connector.DN2)
        self.SBU2.signal.connect(self.connector.SBU2)
        self.SBU1.signal.connect(self.connector.SBU1)
        self.CC1.signal.connect(self.connector.CC1)
        self.CC2.signal.connect(self.connector.CC2)
