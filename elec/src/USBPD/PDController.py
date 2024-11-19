# SPDX-License-Identifier: MIT

import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

import faebryk.library._F as F  # noqa: F401
import faebryk.libs.picker.lcsc as lcsc
import psutil
import typer
from faebryk.core.graph import Graph
from faebryk.core.module import Module
from faebryk.core.node import Node
from faebryk.exporters.pcb.kicad.transformer import PCB_Transformer
from faebryk.exporters.pcb.routing.util import apply_route_in_pcb
from faebryk.libs.app.checks import run_checks
from faebryk.libs.app.kicad_netlist import write_netlist
from faebryk.libs.app.parameters import replace_tbd_with_any
from faebryk.libs.app.pcb import apply_design
from faebryk.libs.examples.pickers import add_example_pickers
from faebryk.libs.kicad.fileformats import (
    C_kicad_fp_lib_table_file,
    C_kicad_pcb_file,
    C_kicad_project_file,
)

from faebryk.libs.app.pcb import apply_layouts, apply_routing, apply_netlist, include_footprints

# from faebryk.libs.examples.buildutil import apply_design_to_pcb as fab_apply_design_to_pcb
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.api.api import ApiNotConfiguredError
from faebryk.libs.picker.api.pickers import add_api_pickers
from faebryk.libs.picker.common import DB_PICKER_BACKEND, CachePicker, PickerType
from faebryk.libs.picker.jlcpcb.jlcpcb import JLCPCB_DB
from faebryk.libs.picker.jlcpcb.pickers import add_jlcpcb_pickers
from faebryk.libs.picker.picker import DescriptiveProperties, pick_part_recursively
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.util import ConfigFlag

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

# Components
from TYPE_C_16PIN_2MD073 import TYPE_C_16PIN_2MD073

logger = logging.getLogger(__name__)



class STEMMA_RIGHT_ANGLE(Module):
    """
    TODO: Docstring describing your module

    1x4P 4P SH Tin 4 -25℃~+85℃ 1A 1 1mm Copper alloy Horizontal attachment SMD,P=1mm,Surface Mount，Right Angle Wire To Board Connector ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    power: F.ElectricPower
    i2c: F.I2C

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C160404"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("CN")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "JST Sales America",
            DescriptiveProperties.partno: "SM04B-SRSS-TB(LF)(SN)",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_JST-SM04B-SRSS-TB-LF-SN_C160404.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={
                self.power.lv: ["1","5","6"],
                self.power.hv: ["2"],
                self.i2c.sda.signal: ["3"],
                self.i2c.scl.signal: ["4"]
            },
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass

class XT30PW(Module):
    """
    XT30 Female Right Angle
    Typically used to provide power (Connected to the battery)
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    power: F.ElectricPower

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C2913282"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Changzhou Amass Electronics Co.,Ltd",
            DescriptiveProperties.partno: "XT30PW-F20.G.Y",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2312181139_Changzhou-Amass-Elec-XT30PW-F20-G-Y_C2913282.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={self.power.lv: ["1","3","4"], self.power.hv: ["2"]},
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass


class ESDA25P35_1U1M(F.Diode):
    """
    TODO: Docstring describing your module

    35A@(8/20us) 41V 1.4kW 23.3V 22V DFN1610-2
    ESD and Surge Protection (TVS/ESD) ROHS
    """

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C1974707"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("D")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "STMicroelectronics",
            DescriptiveProperties.partno: "ESDA25P35-1U1M",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2201300300_STMicroelectronics-ESDA25P35-1U1M_C1974707.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={self.anode: ["1"], self.cathode: ["2"]},
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass


class ESDA25W(Module):
    """
    25V 400W 25V 24V SOT-323-3L
    ESD and Surge Protection (TVS/ESD) ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    A: F.Electrical
    K1: F.Electrical
    K2: F.Electrical
    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C2935152"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("D")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "STMicroelectronics",
            DescriptiveProperties.partno: "ESDA25W",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2201201600_STMicroelectronics-ESDA25W_C2935152.pdf"
    )

    @L.rt_field
    def pin_association(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "3": self.A,
                "1": self.K1,
                "2": self.K2,
            }
        )


class STUSB4500QTR(Module):
    """
    Controller I2C QFN-24-EP(4x4) USB Converters ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    VREG_2V7: F.ElectricPower
    VREG_1V2: F.ElectricPower
    VDD: F.ElectricPower

    CC1: F.ElectricLogic
    CC2: F.ElectricLogic
    CC1DB: F.ElectricLogic
    CC2DB: F.ElectricLogic

    ATTACH: F.Electrical
    GPIO: F.Electrical
    ADDR1: F.Electrical
    POWER_OK3: F.Electrical
    SDA: F.Electrical
    NC: F.Electrical
    POWER_OK2: F.Electrical
    ALERT: F.Electrical
    VBUS_EN_SNK: F.Electrical
    EP: F.Electrical
    A_B_SIDE: F.Electrical
    VSYS: F.Electrical
    DISCH: F.Electrical
    VBUS_VS_DISCH: F.Electrical
    RESET: F.Electrical
    SCL: F.Electrical
    ADDR0: F.Electrical

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C2678061"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "STMicroelectronics",
            DescriptiveProperties.partno: "STUSB4500QTR",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2106070703_STMicroelectronics-STUSB4500QTR_C2678061.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={
                self.ADDR0: ["ADDR0"],
                self.ADDR1: ["ADDR1"],
                self.ALERT: ["ALERT"],
                self.ATTACH: ["ATTACH"],
                self.A_B_SIDE: ["A_B_SIDE"],
                self.CC1.signal: ["CC1"],
                self.CC1DB.signal: ["CC1DB"],
                self.CC2.signal: ["CC2"],
                self.CC2DB.signal: ["CC2DB"],
                self.DISCH: ["DISCH"],
                self.EP: ["EP"],
                self.VDD.lv: ["GND"],
                self.GPIO: ["GPIO"],
                self.NC: ["NC"],
                self.POWER_OK2: ["POWER_OK2"],
                self.POWER_OK3: ["POWER_OK3"],
                self.RESET: ["RESET"],
                self.SCL: ["SCL"],
                self.SDA: ["SDA"],
                self.VBUS_EN_SNK: ["VBUS_EN_SNK"],
                self.VBUS_VS_DISCH: ["VBUS_VS_DISCH"],
                self.VDD.hv: ["VDD"],
                self.VREG_1V2.hv: ["VREG_1V2"],
                self.VREG_2V7.hv: ["VREG_2V7"],
                self.VSYS: ["VSYS"],
            },
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        self.VREG_1V2.voltage.merge(F.Range(1.1 * P.V, 1.3 * P.V))
        self.VREG_2V7.voltage.merge(F.Range(2.6 * P.V, 2.8 * P.V))

        self.VDD.lv.connect(
            self.VREG_2V7.lv, self.VREG_1V2.lv, self.EP, self.RESET, self.VSYS, self.NC
        )

        # Set address
        self.ADDR0.connect(self.VDD.lv)
        self.ADDR1.connect(self.VDD.lv)


class XINGLIGHT_XL_C3570P5S10_62C3C2(Module):
    """
    TODO: Docstring describing your module

    1.7A 6000K~6500K Yellow lens Positive Stick -30℃~+125℃ White 120° 18mW 8.5V~10V SMD,3.5x7mm
    LED Indication - Discrete ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    K: F.Electrical
    A: F.Electrical
    D: F.Electrical

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C3646957"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("LED")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "XINGLIGHT",
            DescriptiveProperties.partno: "XL-C3570P5S10-62C3C2",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2402181505_XINGLIGHT-XL-C3570P5S10-62C3C2_C3646957.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={self.A: ["A"], self.D: ["D"], self.K: ["K"]},
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass



class App(Module):
    PD_CONTROLLER: STUSB4500QTR
    USB_CONNECTOR: TYPE_C_16PIN_2MD073
    ESD_CC: ESDA25W
    VSINK_MOSFET: F.MOSFET
    XT30PW: XT30PW
    STEMMA: STEMMA_RIGHT_ANGLE

    # Passive components
    VBUS_VS_DISCH_R: F.Resistor
    Vreg_2V7_CAP: F.Capacitor
    Vreg_1V2_CAP: F.Capacitor
    VBUS_CAP: F.Capacitor
    VBUS_ESD_DIODE: ESDA25P35_1U1M
    VSINK_ESD_DIODE: ESDA25P35_1U1M
    VSINK_GATE_R: F.Resistor
    VSINK_GATE_PULLUP: F.Resistor
    VSINK_GATE_SNUB_R: F.Resistor
    VSINK_GATE_SNUB_C: F.Capacitor
    DISCH_R: F.Resistor
    I2C_SCL_PULLUP: F.Resistor
    I2C_SDA_PULLUP: F.Resistor


    VSINK: F.ElectricPower
    VMCU: F.ElectricPower
    VBUS: F.ElectricPower
    I2C: F.I2C

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ESD protection TODO: Fix pin association, footprint names both pins K
        # self.usb_connector.CC1.connect(self.esd_cc.K1)
        # self.usb_connector.CC2.connect(self.esd_cc.K2)
        # self.esd_cc.A.connect(self.usb_connector.POWER_VBUS.lv)

        # Tie gnd together
        gnd = F.Net.with_name("GND")
        gnd.part_of.connect(
            self.VSINK.lv,
            self.VBUS.lv,
            self.VMCU.lv,
            self.PD_CONTROLLER.VDD.lv,
            self.PD_CONTROLLER.VREG_1V2.lv,
            self.PD_CONTROLLER.VREG_2V7.lv,
        )

        F.ElectricLogic.connect_all_module_references(self, gnd_only=True)

        # USB connector
        self.USB_CONNECTOR.POWER_VBUS.connect(self.VBUS)
        self.USB_CONNECTOR.CC1.connect(self.PD_CONTROLLER.CC1, self.PD_CONTROLLER.CC1DB)
        self.USB_CONNECTOR.CC2.connect(self.PD_CONTROLLER.CC2, self.PD_CONTROLLER.CC2DB)

        self.VBUS_VS_DISCH_R.resistance.merge(F.Range.from_center_rel(1 * P.kohm, 0.01))
        self.VBUS_VS_DISCH_R.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VBUS.hv.connect_via(self.VBUS_VS_DISCH_R, self.PD_CONTROLLER.VBUS_VS_DISCH)

        # Output connector
        self.XT30PW.power.connect(self.VSINK)

        # I2C
        self.STEMMA.i2c.connect(self.I2C)
        self.STEMMA.power.connect(self.VMCU)

        # Internal rail decoupling
        self.Vreg_2V7_CAP.unnamed[0].connect(self.PD_CONTROLLER.VREG_2V7.lv)
        self.Vreg_2V7_CAP.unnamed[1].connect(self.PD_CONTROLLER.VREG_2V7.hv)
        self.Vreg_2V7_CAP.capacitance.merge(
            F.Range.from_center_rel(1 * P.uF, 0.2)
        )  # TODO: should be 1uF
        self.Vreg_2V7_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))

        self.Vreg_1V2_CAP.unnamed[0].connect(self.PD_CONTROLLER.VREG_1V2.lv)
        self.Vreg_1V2_CAP.unnamed[1].connect(self.PD_CONTROLLER.VREG_1V2.hv)
        self.Vreg_1V2_CAP.capacitance.merge(
            F.Range.from_center_rel(1 * P.uF, 0.2)
        )  # TODO: should be 1uF
        self.Vreg_1V2_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))

        # Regulator rail net naming
        vreg_2v7 = F.Net.with_name("VREG_2V7")
        vreg_1v2 = F.Net.with_name("VREG_1V2")
        vreg_2v7.part_of.connect(self.PD_CONTROLLER.VREG_2V7.hv)
        vreg_1v2.part_of.connect(self.PD_CONTROLLER.VREG_1V2.hv)

        self.VBUS_CAP.unnamed[0].connect(self.VBUS.lv)
        self.VBUS_CAP.unnamed[1].connect(self.VBUS.hv)
        self.VBUS_CAP.capacitance.merge(F.Range.from_center_rel(4.7 * P.uF, 0.3))
        self.VBUS_CAP.add(F.has_footprint_requirement_defined([("0402", 2)]))

        self.VBUS.connect(self.PD_CONTROLLER.VDD)

        # VBUS net naming
        vbus = F.Net.with_name("VBUS") 
        vbus.part_of.connect(self.VBUS.hv)

        # ESD protection
        self.VBUS.lv.connect_via(self.VBUS_ESD_DIODE, self.VBUS.hv)
        self.VSINK.lv.connect_via(self.VSINK_ESD_DIODE, self.VSINK.hv)
        self.PD_CONTROLLER.CC1.signal.connect(self.ESD_CC.K1)
        self.PD_CONTROLLER.CC2.signal.connect(self.ESD_CC.K2)
        self.VBUS.lv.connect(self.ESD_CC.A)

        # CC line net naming
        cc1 = F.Net.with_name("CC1")
        cc2 = F.Net.with_name("CC2")
        cc1.part_of.connect(self.PD_CONTROLLER.CC1.signal)
        cc2.part_of.connect(self.PD_CONTROLLER.CC2.signal)

        # VSINK SWITCH
        self.VSINK_MOSFET.channel_type.merge(F.MOSFET.ChannelType.P_CHANNEL)
        self.VSINK_MOSFET.add(F.has_descriptive_properties_defined({"LCSC": "C471913"}))
        # VBUS to VSINK switching
        self.VBUS.hv.connect_via(self.VSINK_MOSFET, self.VSINK.hv)

        # VSINK voltage divider for VCC
        self.VSINK_VCC = F.Net.with_name("VSINK_VCC")
        self.VSINK_VCC.part_of.connect(self.VSINK.hv)

        # Gate pullup resistor divider
        self.VSINK_GATE_R.resistance.merge(F.Range.from_center_rel(22 * P.kohm, 0.03))
        self.VSINK_GATE_R.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VSINK_MOSFET.gate.connect_via(
            self.VSINK_GATE_R, self.PD_CONTROLLER.VBUS_EN_SNK
        )

        # Gate to drain pullup resistor
        self.VSINK_GATE_PULLUP.resistance.merge(
            F.Range.from_center_rel(100 * P.kohm, 0.02)
        )
        self.VSINK_GATE_PULLUP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VSINK_MOSFET.gate.connect_via(
            self.VSINK_GATE_PULLUP, self.VSINK_MOSFET.drain
        )

        # Gate to source RC snubber
        self.VSINK_GATE_SNUB_R.resistance.merge(
            F.Range.from_center_rel(100 * P.ohm, 0.01)
        )
        self.VSINK_GATE_SNUB_R.add(F.has_footprint_requirement_defined([("0201", 2)]))

        self.VSINK_GATE_SNUB_C.capacitance.merge(
            F.Range.from_center_rel(100 * P.nF, 0.2)
        )
        self.VSINK_GATE_SNUB_C.add(F.has_footprint_requirement_defined([("0201", 2)]))

        # Connect RC snubber between gate and source
        self.VSINK_MOSFET.gate.connect_via(
            [self.VSINK_GATE_SNUB_R, self.VSINK_GATE_SNUB_C], self.VSINK_MOSFET.source
        )

        # DISCH resistor
        self.DISCH_R.resistance.merge(F.Range.from_center_rel(1 * P.kohm, 0.01))
        self.DISCH_R.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.VBUS.hv.connect_via(self.DISCH_R, self.PD_CONTROLLER.DISCH)

        # I2C nets
        self.I2C_SCL = F.Net.with_name("I2C_SCL")
        self.I2C_SDA = F.Net.with_name("I2C_SDA")
        self.I2C.scl.connect(self.I2C_SCL.part_of)
        self.I2C.sda.connect(self.I2C_SDA.part_of)

        # Connect PD controller I2C pins to I2C bus
        self.PD_CONTROLLER.SCL.connect(self.I2C_SCL.part_of)
        self.PD_CONTROLLER.SDA.connect(self.I2C_SDA.part_of)

        # for r in self.I2C.terminate():
        #     # self.add(r)
        #     r.add(F.has_footprint_requirement_defined([("0402", 2)]))
        #     r.resistance.merge(F.Range.from_center_rel(4.7 * P.kohm, 0.02))

        self.I2C_SCL_PULLUP.resistance.merge(F.Range.from_center_rel(4.7 * P.kohm, 0.03))
        self.I2C_SDA_PULLUP.resistance.merge(F.Range.from_center_rel(4.7 * P.kohm, 0.03))

        self.I2C_SCL_PULLUP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.I2C_SDA_PULLUP.add(F.has_footprint_requirement_defined([("0201", 2)]))

        # Connect I2C lines to VMCU via pullup resistors
        self.I2C_SCL.part_of.connect_via(self.I2C_SCL_PULLUP, self.VMCU.hv)
        self.I2C_SDA.part_of.connect_via(self.I2C_SDA_PULLUP, self.VMCU.hv)

        F.ElectricLogic.connect_all_node_references(
            [self.VMCU]
            + [self.I2C]
        )
        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.VSINK.voltage.merge(F.Range(5 * P.V, 20 * P.V))
        self.VMCU.voltage.merge(F.Range(0 * P.V, 3.6 * P.V))
        self.VBUS.voltage.merge(F.Range(5 * P.V, 20 * P.V))


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

def main():
    logger.info("Building app")
    app = App()

    logger.info("Export")
    apply_design_to_pcb(app)



if __name__ == "__main__":
    setup_basic_logging()
    logger.info("Running example")

    typer.run(main)
