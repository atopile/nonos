import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from atopile.buildutil import pick_part_recursively
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.logging import setup_basic_logging
from faebryk.core.solver.defaultsolver import DefaultSolver

logger = logging.getLogger(__name__)


class Test(Module):
    inductor: F.Inductor

    def __preinit__(self):
        #self.inductor.inductance.constrain_subset(L.Range.from_center_rel(3.3 * P.uH, 0.4))
        # self.inductor.max_current.constrain_subset(L.Range(4 * P.A, 6 * P.A))
        self.inductor.add_trait(F.has_descriptive_properties_defined({"LCSC": "C602030"}))


if __name__ == "__main__":
    test = Test()
    setup_basic_logging()

    solver = DefaultSolver()
    add_jlcpcb_pickers(test.inductor)
    pick_part_recursively(test.inductor, solver)
