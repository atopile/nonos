# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

"""
This is the entrypoint and boilerplate of the application.
It sets up several paths and calls the app to create the graph.
Afterwards it uses the graph to export to different artifacts (e.g netlist).
"""

import logging
from pathlib import Path

import faebryk.libs.picker.lcsc as lcsc
import typer
from faebryk.core.module import Module
from faebryk.exporters.parameters.parameters_to_file import export_parameters_to_file
from faebryk.exporters.pcb.kicad.artifacts import export_svg
from faebryk.libs.app.checks import run_checks
from faebryk.libs.app.manufacturing import export_pcba_artifacts
from faebryk.libs.app.parameters import replace_tbd_with_any
from faebryk.libs.app.pcb import apply_design
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.picker.picker import pick_part_recursively
from typing_extensions import Annotated

from elec.src.USBPD.pd_controller import App
from pcb import transform_pcb

# logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def main(
    export_manufacturing_artifacts: Annotated[
        bool, typer.Option(help="Export manufacturing artifacts (gerbers, BOM, etc.)")
    ] = False,
    export_visuals: Annotated[
        bool, typer.Option(help="Export project visuals (e.g. SVG)")
    ] = False,
    export_parameters: Annotated[
        bool, typer.Option(help="Export project parameters to a file")
    ] = False,
):
    # paths --------------------------------------------------
    root = Path(__file__).parent.parent.parent
    kicad_prj_path = root.joinpath("layout/pd-controller")
    pcbfile = kicad_prj_path.joinpath("pd-controller.kicad_pcb")
    build_dir = Path("./build")
    faebryk_build_dir = build_dir.joinpath("faebryk")
    faebryk_build_dir.mkdir(parents=True, exist_ok=True)
    netlist_path = faebryk_build_dir.joinpath("faebryk.net")
    manufacturing_artifacts_path = build_dir.joinpath("manufacturing")
    parameter_dir = build_dir.joinpath("parameters")
    parameters_path = parameter_dir.joinpath("parameters.md")  # .txt is also possible
    visuals_dir = build_dir.joinpath("visuals")

    lcsc.BUILD_FOLDER = build_dir
    lcsc.LIB_FOLDER = root.joinpath("libs")

    app = App()

    # fill unspecified parameters ----------------------------
    logger.info("Filling unspecified parameters")
    replace_tbd_with_any(app, recursive=True, loglvl=logging.DEBUG)

    # pick parts ---------------------------------------------
    logger.info("Picking parts")
    modules = {
        n.get_most_special() for n in app.get_children(direct_only=False, types=Module)
    }
    for n in modules:
        add_jlcpcb_pickers(n, base_prio=10)
        # add_app_pickers(n)
    pick_part_recursively(app)

    # graph --------------------------------------------------
    logger.info("Make graph")
    G = app.get_graph()

    # checks -------------------------------------------------
    logger.info("Running checks")
    run_checks(app, G)

    # pcb ----------------------------------------------------
    logger.info("Make netlist & pcb")
    apply_design(pcbfile, netlist_path, G, app, transform_pcb)

    # generate pcba manufacturing and other artifacts ---------
    if export_manufacturing_artifacts:
        export_pcba_artifacts(manufacturing_artifacts_path, pcbfile, app)

    # generate visuals ---------------------------------------
    if export_visuals:
        export_svg(pcbfile, visuals_dir.joinpath("pcba.svg"))

    # export parameter report --------------------------------
    if export_parameters:
        export_parameters_to_file(app, parameters_path)


if __name__ == "__main__":
    setup_basic_logging()
    typer.run(main)
