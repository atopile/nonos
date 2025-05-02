# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401


logger = logging.getLogger(__name__)


class HatButtonAntenna(Module):
    """
    Hat Board
    """

    antenna: F.DifferentialPair
    play_button: F.ElectricLogic
    next_button: F.ElectricLogic
    prev_button: F.ElectricLogic
    slider = L.list_field(5, F.ElectricLogic)

    designator_prefix = L.f_field(F.has_designator_prefix)(
        F.has_designator_prefix.Prefix.P
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "2": self.play_button.line,
                "3": self.next_button.line,
                "1": self.prev_button.line,
                "4": self.slider[0].line,
                "5": self.slider[1].line,
                "6": self.slider[2].line,
                "7": self.slider[3].line,
                "8": self.slider[4].line,
                "10": self.antenna.p.line,
                "9": self.antenna.n.line,
            }
        )
