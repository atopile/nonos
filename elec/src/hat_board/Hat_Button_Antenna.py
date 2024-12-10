# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import has_part_picked_remove


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
    no_pick: has_part_picked_remove

    designator_prefix = L.f_field(F.has_designator_prefix_defined)(
        F.has_designator_prefix.Prefix.P
    )



    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "2": self.play_button.signal,
                "3": self.next_button.signal,
                "1": self.prev_button.signal,
                "4": self.slider[0].signal,
                "5": self.slider[1].signal,
                "6": self.slider[2].signal,
                "7": self.slider[3].signal,
                "8": self.slider[4].signal,
                "10": self.antenna.p.signal,
                "9": self.antenna.n.signal,
            }
        )

    def __preinit__(self):
        self.get_trait(F.can_attach_to_footprint).attach(F.KicadFootprint("lcsc:hat-button-antenna", [str(i + 1) for i in range(10)]))
