# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)


class Microchip_Tech_CAP1188_1_CP_TR(Module):
    """
    TODO: Docstring describing your module

    8 QFN-24-EP(4x4)
    Touch Sensors ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    SPI_CSh: F.Electrical  # pin: 1
    WAKE_SPI_MOSI: F.Electrical  # pin: 2
    SMDATA_BC_DATA_SPI_MSIO_SPI_MISO: F.Electrical  # pin: 3
    SMCLK_BC_CLK_SPI_CLK: F.Electrical  # pin: 4
    LED1: F.Electrical  # pin: 5
    LED2: F.Electrical  # pin: 6
    LED3: F.Electrical  # pin: 7
    LED4: F.Electrical  # pin: 8
    LED5: F.Electrical  # pin: 9
    LED6: F.Electrical  # pin: 10
    LED7: F.Electrical  # pin: 11
    LED8: F.Electrical  # pin: 12
    ALERTh_BC_IRQh: F.Electrical  # pin: 13
    ADDR_COMM: F.Electrical  # pin: 14
    CS8: F.Electrical  # pin: 15
    CS7: F.Electrical  # pin: 16
    CS6: F.Electrical  # pin: 17
    CS5: F.Electrical  # pin: 18
    CS4: F.Electrical  # pin: 19
    CS3: F.Electrical  # pin: 20
    CS2: F.Electrical  # pin: 21
    CS1: F.Electrical  # pin: 22
    GND: F.Electrical  # pin: 23
    RESET: F.Electrical  # pin: 24

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Microchip Tech",
            DescriptiveProperties.partno: "CAP1188-1-CP-TR",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2309071116_Microchip-Tech-CAP1188-1-CP-TR_C2652057.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.SPI_CSh,
                "2": self.WAKE_SPI_MOSI,
                "3": self.SMDATA_BC_DATA_SPI_MSIO_SPI_MISO,
                "4": self.SMCLK_BC_CLK_SPI_CLK,
                "5": self.LED1,
                "6": self.LED2,
                "7": self.LED3,
                "8": self.LED4,
                "9": self.LED5,
                "10": self.LED6,
                "11": self.LED7,
                "12": self.LED8,
                "13": self.ALERTh_BC_IRQh,
                "14": self.ADDR_COMM,
                "15": self.CS8,
                "16": self.CS7,
                "17": self.CS6,
                "18": self.CS5,
                "19": self.CS4,
                "20": self.CS3,
                "21": self.CS2,
                "22": self.CS1,
                "23": self.GND,
                "24": self.RESET,
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
