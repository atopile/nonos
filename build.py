import logging
from pathlib import Path
from typing import Annotated

import faebryk.library._F as F  # noqa: F401
import typer
from faebryk.core.module import Module
from faebryk.libs.app.checks import run_checks
from faebryk.libs.app.parameters import replace_tbd_with_any
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.api.pickers import add_api_pickers
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.picker.picker import pick_part_recursively
from faebryk.libs.app.pcb import apply_design
from faebryk.libs.app.manufacturing import export_pcba_artifacts
from atopile.config import BuildContext, get_project_config_from_path
from faebryk.exporters.pcb.kicad.artifacts import export_svg
from faebryk.exporters.parameters.parameters_to_file import export_parameters_to_file

import importlib
import sys

logger = logging.getLogger(__name__)


def build_app(
    app: Module,
    build_context: BuildContext,
    pcb_path: Path,
    netlist_path: Path,
    export_manufacturing_artifacts: bool = False,
    export_visuals: bool = False,
    export_parameters: bool = False,
):
    # fill unspecified parameters ----------------------------
    logger.info("Filling unspecified parameters")
    replace_tbd_with_any(app, recursive=True, loglvl=logging.DEBUG)

    # pick parts ---------------------------------------------
    logger.info("Picking parts")
    modules = {
        n.get_most_special() for n in app.get_children(direct_only=False, types=Module)
    }
    for n in modules:
        # TODO: get enabled pickers from config
        add_api_pickers(n, base_prio=10)
        add_jlcpcb_pickers(n, base_prio=10)
    pick_part_recursively(app)

    # graph --------------------------------------------------
    logger.info("Make graph")
    G = app.get_graph()

    # checks -------------------------------------------------
    logger.info("Running checks")
    run_checks(app, G)

    # pcb ----------------------------------------------------
    logger.info("Make netlist & pcb")
    apply_design(pcb_path, netlist_path, G, app, transform=None)

    # generate pcba manufacturing and other artifacts ---------
    if export_manufacturing_artifacts:
        export_pcba_artifacts(build_context.output_base, pcb_path, app)

    # generate visuals ---------------------------------------
    if export_visuals:
        export_svg(pcb_path, build_context.output_base / f"{build_context.name}.svg")

    # export parameter report --------------------------------
    if export_parameters:
        export_parameters_to_file(
            app, build_context.output_base / f"{build_context.name}.csv"
        )


def build(
    name: Annotated[str, typer.Argument(help="Build name")],
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
    logger.info(f"Building {name}")

    project_config = get_project_config_from_path(Path("."))
    build_context = BuildContext.from_config_name(project_config, name)

    if name not in project_config.builds:
        raise ValueError(f"Build config {name} not found")

    build_entrypoint = project_config.builds[name].entry

    if build_entrypoint is None:
        raise ValueError(f"Build config {name} has no entry point")

    app_path, app_class_name = build_entrypoint.split(":")

    sys.path.insert(0, str(Path("elec/src").absolute()))

    app = getattr(importlib.import_module(app_path), app_class_name)()

    layout_path = build_context.layout_path

    if layout_path is None:
        # TODO: BuildContext should enforce this
        raise ValueError(f"Build config {name} has no layout path")

    build_dir = build_context.output_base

    build_app(
        app,
        build_context,
        pcb_path=layout_path,
        netlist_path=build_dir.joinpath(f"{name}.net"),
        export_manufacturing_artifacts=export_manufacturing_artifacts,
        export_visuals=export_visuals,
        export_parameters=export_parameters,
    )


if __name__ == "__main__":
    setup_basic_logging()
    typer.run(build)
