# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class NXP_Semicon_PN5321A3HN_C106_51(Module):
    """
    TODO: Docstring describing your module

    QFN-40-EP(6x6) RFID ICs ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    DVSS: F.Electrical  # pin: 1
    LOADMOD: F.Electrical  # pin: 2
    TVSS1: F.Electrical  # pin: 3
    TX1: F.Electrical  # pin: 4
    TVDD: F.Electrical  # pin: 5
    TX2: F.Electrical  # pin: 6
    TVSS2: F.Electrical  # pin: 7
    AVDD: F.Electrical  # pin: 8
    VMID: F.Electrical  # pin: 9
    RX: F.Electrical  # pin: 10
    AVSS: F.Electrical  # pin: 11
    AUX1: F.Electrical  # pin: 12
    AUX2: F.Electrical  # pin: 13
    OSCIN: F.Electrical  # pin: 14
    OSCOUT: F.Electrical  # pin: 15
    I0: F.Electrical  # pin: 16
    I1: F.Electrical  # pin: 17
    TESTEN: F.Electrical  # pin: 18
    P35: F.Electrical  # pin: 19
    N_C_: F.Electrical  # pins: 20, 21, 22
    PVDD: F.Electrical  # pin: 23
    P30_UART_RX: F.Electrical  # pin: 24
    P70_IRQ: F.Electrical  # pin: 25
    RSTOUT_N: F.Electrical  # pin: 26
    NSS_P50_SCL_HSU_RX: F.Electrical  # pin: 27
    MOSI_SDA_HSU_TX: F.Electrical  # pin: 28
    MISO_P71: F.Electrical  # pin: 29
    SCK_P72: F.Electrical  # pin: 30
    P31_UART_TX: F.Electrical  # pin: 31
    P32_INT0: F.Electrical  # pin: 32
    P33_INT1: F.Electrical  # pin: 33
    P34_SIC_CLK: F.Electrical  # pin: 34
    SIGOUT: F.Electrical  # pin: 35
    SIGIN: F.Electrical  # pin: 36
    SVDD: F.Electrical  # pin: 37
    RSTPD_N: F.Electrical  # pin: 38
    DVDD: F.Electrical  # pin: 39
    VBAT: F.Electrical  # pin: 40
    EP: F.Electrical  # pin: 41

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C880904"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "NXP Semicon",
            DescriptiveProperties.partno: "PN5321A3HN/C106,51",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.nxp.com/docs/en/nxp/data-sheets/PN532_C1.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.DVSS,
                "2": self.LOADMOD,
                "3": self.TVSS1,
                "4": self.TX1,
                "5": self.TVDD,
                "6": self.TX2,
                "7": self.TVSS2,
                "8": self.AVDD,
                "9": self.VMID,
                "10": self.RX,
                "11": self.AVSS,
                "12": self.AUX1,
                "13": self.AUX2,
                "14": self.OSCIN,
                "15": self.OSCOUT,
                "16": self.I0,
                "17": self.I1,
                "18": self.TESTEN,
                "19": self.P35,
                "20": self.N_C_,
                "21": self.N_C_,
                "22": self.N_C_,
                "23": self.PVDD,
                "24": self.P30_UART_RX,
                "25": self.P70_IRQ,
                "26": self.RSTOUT_N,
                "27": self.NSS_P50_SCL_HSU_RX,
                "28": self.MOSI_SDA_HSU_TX,
                "29": self.MISO_P71,
                "30": self.SCK_P72,
                "31": self.P31_UART_TX,
                "32": self.P32_INT0,
                "33": self.P33_INT1,
                "34": self.P34_SIC_CLK,
                "35": self.SIGOUT,
                "36": self.SIGIN,
                "37": self.SVDD,
                "38": self.RSTPD_N,
                "39": self.DVDD,
                "40": self.VBAT,
                "41": self.EP,
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
