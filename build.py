import logging
from pathlib import Path
from typing import Callable

import faebryk.library._F as F  # noqa: F401
import faebryk.libs.picker.lcsc as lcsc
import typer
from faebryk.core.module import Module
from faebryk.exporters.pcb.kicad.transformer import PCB_Transformer
from faebryk.libs.app.checks import run_checks
from faebryk.libs.app.kicad_netlist import write_netlist
from faebryk.libs.app.parameters import replace_tbd_with_any
from faebryk.libs.app.pcb import include_footprints
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.api.api import ApiNotConfiguredError
from faebryk.libs.picker.api.pickers import add_api_pickers
from faebryk.libs.picker.common import DB_PICKER_BACKEND, CachePicker, PickerType
from faebryk.libs.picker.jlcpcb.jlcpcb import JLCPCB_DB
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.picker.picker import pick_part_recursively
from faebryk.libs.util import ConfigFlag

import yaml
import importlib
import sys
from pathlib import Path

BUILD_DIR = Path("./build")
GRAPH_OUT = BUILD_DIR / Path("faebryk/graph.png")
NETLIST_OUT = BUILD_DIR / Path("faebryk/faebryk.net")
KICAD_SRC = BUILD_DIR / Path("kicad/source")
PCB_FILE = KICAD_SRC / Path("example.kicad_pcb")
PROJECT_FILE = KICAD_SRC / Path("example.kicad_pro")

lcsc.BUILD_FOLDER = BUILD_DIR
lcsc.LIB_FOLDER = BUILD_DIR / Path("kicad/libs")
lcsc.MODEL_PATH = None

DEV_MODE = ConfigFlag("EXP_DEV_MODE", False)

logger = logging.getLogger(__name__)


def apply_design_to_pcb(
    m: Module, transform: Callable[[PCB_Transformer], None] | None = None
):
    """
    Picks parts for the module.
    Runs a simple ERC.
    Tags the graph with kicad info.
    Exports the graph to a netlist.
    Writes it to ./build
    Opens PCB and applies design (netlist, layout, route, ...)
    Saves PCB
    """

    logger.info("Filling unspecified parameters")

    replace_tbd_with_any(
        m, recursive=True, loglvl=logging.DEBUG if DEV_MODE else logging.INFO
    )

    G = m.get_graph()
    run_checks(m, G)

    # TODO this can be prettier
    # picking ----------------------------------------------------------------
    modules = m.get_children_modules(types=Module)
    CachePicker.add_to_modules(modules, prio=-20)

    match DB_PICKER_BACKEND:
        case PickerType.JLCPCB:
            try:
                JLCPCB_DB()
                for n in modules:
                    add_jlcpcb_pickers(n, base_prio=-10)
            except FileNotFoundError:
                logger.warning("JLCPCB database not found. Skipping JLCPCB pickers.")
        case PickerType.API:
            try:
                for n in modules:
                    add_api_pickers(n)
            except ApiNotConfiguredError:
                logger.warning("API not configured. Skipping API pickers.")

    pick_part_recursively(m)
    # -------------------------------------------------------------------------

    # apply_design(PCB_FILE, NETLIST_OUT, G, m, transform)
    logger.info(f"Writing netlist to {NETLIST_OUT}")
    changed = write_netlist(G, NETLIST_OUT, use_kicad_designators=True)
    # apply_design(PCB_FILE, NETLIST_OUT, G, m, transform)
    include_footprints(PCB_FILE)

    return G


# TODO: discover modules in elec/src
# TODO: build each


def build_module(name: str):
    logger.info(f"Building {name}")

    # TODO: validate config
    project_config = yaml.load(Path("ato.yaml").read_text(), Loader=yaml.Loader)

    if name not in project_config["builds"]:
        raise ValueError(f"Build config {name} not found")

    app_path, app_class_name = project_config["builds"][name].split(":")

    sys.path.insert(0, str(Path("elec/src").absolute()))

    App = getattr(importlib.import_module(app_path), app_class_name)

    # app = App()

    # logger.info("Export")
    # apply_design_to_pcb(app)


if __name__ == "__main__":
    setup_basic_logging()
    typer.run(build_module)
