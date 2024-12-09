# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

from .nfc.NXP_Semicon_PN5321A3HN_C106_51 import NXP_Semicon_PN5321A3HN_C106_51
from .TE_Connectivity_1_2328702_0 import TE_Connectivity_1_2328702_0
# from .capacative_sensor.

logger = logging.getLogger(__name__)

class HatBoard(Module):
    """
    HAT Board
    """
    nfc: NXP_Semicon_PN5321A3HN_C106_51
    board_to_board_connector: TE_Connectivity_1_2328702_0
    # capacitive_sensor: 


    def __preinit__(self):

        # Connector inverts pinmap, need to flip it back
        self.board_to_board_connector.invert_pinmap()
