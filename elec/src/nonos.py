

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
logger = logging.getLogger(__name__)

class NONOS(Module):
    """
    Open-source smart speaker
    """
    processor: CM4_MINIMAL
    rj45: HANRUNZhongshan_HanRun_Elec_HR911130A
    pd_controller: PDController


    def __preinit__(self):
        self.rj45.ethernet.connect(self.processor.ethernet)
        self.rj45.power_led.connect(self.processor.power_3v3)
