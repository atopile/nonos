

# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

# Components
from .cm4.cm4 import CM4_MINIMAL
from .cm4.HANRUNZhongshan_HanRun_Elec_HR911130A import HANRUNZhongshan_HanRun_Elec_HR911130A
from .pd_controller.pd_controller import PDController
from .amplifier.Texas_Instruments_TAS5825MRHBR import Texas_Instruments_TAS5825MRHBR
from .power_supply.Texas_Instruments_TPS56637RPAR import Texas_Instruments_TPS56637RPAR


logger = logging.getLogger(__name__)

class NONOS(Module):
    """
    Open-source smart speaker
    """
    processor: CM4_MINIMAL
    rj45: HANRUNZhongshan_HanRun_Elec_HR911130A
    pd_controller: PDController
    regulator: Texas_Instruments_TPS56637RPAR
    amplifier: Texas_Instruments_TAS5825MRHBR
    # amplifier
    # DSP
    # 

    power_vbus: F.ElectricPower
    power_5v: F.ElectricPower


    def __preinit__(self):
    

        self.rj45.ethernet.connect(self.processor.ethernet)
        self.rj45.power_led.connect(self.processor.power_3v3)
