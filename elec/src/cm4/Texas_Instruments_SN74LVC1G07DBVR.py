# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)

class _Texas_Instruments_SN74LVC1G07DBVR(Module):
    """
    TODO: Docstring describing your module

    1 32mA 1.65V~5.5V 1 SOT-23-5 Buffers, Drivers, Receivers, Transceivers ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    N_C_: F.Electrical  # pin: 1
    A: F.Electrical  # pin: 2
    GND: F.Electrical  # pin: 3
    Y: F.Electrical  # pin: 4
    VCC: F.Electrical  # pin: 5

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C7829"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Texas Instruments",
            DescriptiveProperties.partno: "SN74LVC1G07DBVR",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_1809251740_Texas-Instruments-SN74LVC1G07DBVR_C7829.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.N_C_,
                "2": self.A,
                "3": self.GND,
                "4": self.Y,
                "5": self.VCC,
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

class Texas_Instruments_SN74LVC1G07DBVR(Module):
    """
    Buffer
    """
    power: F.ElectricPower
    input: F.ElectricLogic
    output: F.ElectricLogic
    ic: _Texas_Instruments_SN74LVC1G07DBVR

    def __preinit__(self):
        self.power.hv.connect(self.ic.VCC)
        self.input.signal.connect(self.ic.A)
        self.output.signal.connect(self.ic.Y)
