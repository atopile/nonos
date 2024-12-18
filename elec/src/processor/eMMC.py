# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.util import times

logger = logging.getLogger(__name__)


class _Samsung_KLMBG2JETD_B041(Module):
    """
    Component

    FBGA-153
    eMMC ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    VDD_3V3: F.ElectricPower
    VDD_1V8: F.ElectricPower
    VDD_INTERNAL: F.ElectricPower

    DAT = times(8, F.ElectricLogic)

    DATA_STROBE: F.ElectricLogic
    CMD: F.ElectricLogic
    CLK: F.ElectricLogic
    RSTN: F.ElectricLogic
    VDDF: F.Electrical
    VDDI: F.Electrical
    VDD: F.Electrical
    VSS: F.Electrical

    NC: F.Electrical  # TODO: remove NC, replace with a not-connected flag

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C2803245"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Samsung",
            DescriptiveProperties.partno: "KLMBG2JETD-B041",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2202131900_Samsung-KLMBG2JETD-B041_C2803245.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "A1": None,
                "A10": None,
                "A11": None,
                "A12": None,
                "A13": None,
                "A14": None,
                "A2": None,
                "A3": self.DAT[0].signal,
                "A4": self.DAT[1].signal,
                "A5": self.DAT[2].signal,
                "A6": self.VSS,
                "A7": None,
                "A8": None,
                "A9": None,
                "B1": None,
                "B10": None,
                "B11": None,
                "B12": None,
                "B13": None,
                "B14": None,
                "B2": self.DAT[3].signal,
                "B3": self.DAT[4].signal,
                "B4": self.DAT[5].signal,
                "B5": self.DAT[6].signal,
                "B6": self.DAT[7].signal,
                "B7": None,
                "B8": None,
                "B9": None,
                "C1": None,
                "C10": None,
                "C11": None,
                "C12": None,
                "C13": None,
                "C14": None,
                "C2": self.VDDI,
                "C3": None,
                "C4": self.VSS,
                "C5": None,
                "C6": self.VDD,
                "C7": None,
                "C8": None,
                "C9": None,
                "D1": None,
                "D12": None,
                "D13": None,
                "D14": None,
                "D2": None,
                "D3": None,
                "D4": None,
                "E1": None,
                "E10": None,
                "E12": None,
                "E13": None,
                "E14": None,
                "E2": None,
                "E3": None,
                "E5": None,
                "E6": self.VDDF,
                "E7": self.VSS,
                "E8": None,
                "E9": None,
                "F1": None,
                "F10": None,
                "F12": None,
                "F13": None,
                "F14": None,
                "F2": None,
                "F3": None,
                "F5": self.VDDF,
                "G1": None,
                "G10": None,
                "G12": None,
                "G13": None,
                "G14": None,
                "G2": None,
                "G3": None,
                "G5": self.VSS,
                "H1": None,
                "H10": self.VSS,
                "H12": None,
                "H13": None,
                "H14": None,
                "H2": None,
                "H3": None,
                "H5": self.DATA_STROBE.signal,
                "J1": None,
                "J10": self.VDDF,
                "J12": None,
                "J13": None,
                "J14": None,
                "J2": None,
                "J3": None,
                "J5": self.VSS,
                "K1": None,
                "K10": None,
                "K12": None,
                "K13": None,
                "K14": None,
                "K2": None,
                "K3": None,
                "K5": self.RSTN.signal,
                "K6": None,
                "K7": None,
                "K8": self.VSS,
                "K9": self.VDDF,
                "L1": None,
                "L12": None,
                "L13": None,
                "L14": None,
                "L2": None,
                "L3": None,
                "M1": None,
                "M10": None,
                "M11": None,
                "M12": None,
                "M13": None,
                "M14": None,
                "M2": None,
                "M3": None,
                "M4": self.VDD,
                "M5": self.CMD.signal,
                "M6": self.CLK.signal,
                "M7": None,
                "M8": None,
                "M9": None,
                "N1": None,
                "N10": None,
                "N11": None,
                "N12": None,
                "N13": None,
                "N14": None,
                "N2": self.VSS,
                "N3": None,
                "N4": self.VDD,
                "N5": self.VSS,
                "N6": None,
                "N7": None,
                "N8": None,
                "N9": None,
                "P1": None,
                "P10": None,
                "P11": None,
                "P12": None,
                "P13": None,
                "P14": None,
                "P2": None,
                "P3": self.VDD,
                "P4": self.VSS,
                "P5": self.VDD,
                "P6": self.VSS,
                "P7": None,
                "P8": None,
                "P9": None,
            }
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------
        self.VDD_3V3.hv.connect(self.VDDF)
        self.VDD_1V8.hv.connect(self.VDD)
        self.VDD_INTERNAL.hv.connect(self.VDDI)
        self.VDD_3V3.lv.connect(self.VSS)

        # Connect references
        for dat in self.DAT:
            dat.reference.connect(self.VDD_1V8)
            dat.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.DATA_STROBE.reference.connect(self.VDD_1V8)
        self.DATA_STROBE.reference.voltage.merge(
            F.Range.from_center_rel(1.8 * P.V, 0.05)
        )
        self.CMD.reference.connect(self.VDD_1V8)
        self.CMD.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.CLK.reference.connect(self.VDD_1V8)
        self.CLK.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.RSTN.reference.connect(self.VDD_1V8)
        self.RSTN.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.VDD_INTERNAL.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.VDD_3V3.voltage.merge(F.Range.from_center_rel(3.3 * P.V, 0.05))
        self.VDD_1V8.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))


class Samsung_KLMBG2JETD_B041(Module):
    """
    Module, contains decoupling capacitors and pullups


    """

    # Interfaces
    VDD_3V3: F.ElectricPower
    VDD_1V8: F.ElectricPower
    DAT = times(8, F.ElectricLogic)
    DATA_STROBE: F.ElectricLogic
    CMD: F.ElectricLogic
    CLK: F.ElectricLogic
    RSTN: F.ElectricLogic

    # Components
    eMMC: _Samsung_KLMBG2JETD_B041

    def __preinit__(self):
        # Connections
        F.ElectricLogic.connect_all_module_references(self, gnd_only=True)

        self.VDD_3V3.hv.connect(self.eMMC.VDD_3V3.hv)
        self.VDD_1V8.hv.connect(self.eMMC.VDD_1V8.hv)
        self.VDD_3V3.lv.connect(self.eMMC.VDD_3V3.lv, self.eMMC.VDD_1V8.lv)

        # Net naming
        for net in self.eMMC.DAT:
            F.Net.with_name(f"eMMC_DAT_{self.eMMC.DAT.index(net)}").part_of.connect(
                self.DAT[self.eMMC.DAT.index(net)].signal
            )

        F.Net.with_name("eMMC_DATA_STROBE").part_of.connect(self.DATA_STROBE.signal)
        F.Net.with_name("eMMC_CMD").part_of.connect(self.CMD.signal)
        F.Net.with_name("eMMC_CLK").part_of.connect(self.CLK.signal)
        F.Net.with_name("eMMC_RSTN").part_of.connect(self.RSTN.signal)
        # F.Net.with_name("VDD_1V8").part_of.connect(self.VDD_1V8.hv)
        # F.Net.with_name("VDD_3V3").part_of.connect(self.VDD_3V3.hv)
        F.Net.with_name("VDD_INTERNAL").part_of.connect(self.eMMC.VDD_INTERNAL.hv)
        # F.Net.with_name("GND").part_of.connect(self.VDD_1V8.lv)

        # Pass through
        for dat in self.DAT:
            dat.connect(self.eMMC.DAT[self.DAT.index(dat)])
        self.DATA_STROBE.connect(self.eMMC.DATA_STROBE)
        self.CMD.connect(self.eMMC.CMD)
        self.CLK.connect(self.eMMC.CLK)
        self.RSTN.connect(self.eMMC.RSTN)

        # VDD_3V3
        VDD_3V3_CAP_PROPERTIES = [
            {"value": 4.7 * P.uF, "footprint": "0402"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
        ]

        VDD_3V3_CAPS = []

        for props in VDD_3V3_CAP_PROPERTIES:
            cap = self.VDD_3V3.decoupled.decouple(owner=self)
            cap.add(F.has_footprint_requirement_defined([(props["footprint"], 2)]))
            cap.capacitance.merge(F.Range.from_center_rel(props["value"], 0.2))
            VDD_3V3_CAPS.append(cap)

        # VDD_1V8
        VDD_1V8_CAP_PROPERTIES = [
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
        ]

        VDD_1V8_CAPS = []

        for props in VDD_1V8_CAP_PROPERTIES:
            cap = self.VDD_1V8.decoupled.decouple(owner=self)
            cap.add(F.has_footprint_requirement_defined([(props["footprint"], 2)]))
            cap.capacitance.merge(F.Range.from_center_rel(props["value"], 0.2))
            VDD_1V8_CAPS.append(cap)

        # VDD_INTERNAL
        VDD_INTERNAL_CAP_PROPERTIES = [
            {"value": 1 * P.uF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
        ]

        VDD_INTERNAL_CAPS = []

        for props in VDD_INTERNAL_CAP_PROPERTIES:
            cap = self.eMMC.VDD_INTERNAL.decoupled.decouple(owner=self)
            cap.add(F.has_footprint_requirement_defined([(props["footprint"], 2)]))
            cap.capacitance.merge(F.Range.from_center_rel(props["value"], 0.2))
            VDD_INTERNAL_CAPS.append(cap)

        # Connect references
        for dat in self.DAT:
            dat.reference.connect(self.VDD_1V8)
            dat.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))

        self.DATA_STROBE.reference.connect(self.VDD_1V8)
        self.DATA_STROBE.reference.voltage.merge(
            F.Range.from_center_rel(1.8 * P.V, 0.05)
        )
        self.CMD.reference.connect(self.VDD_1V8)
        self.CMD.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.CLK.reference.connect(self.VDD_1V8)
        self.CLK.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.RSTN.reference.connect(self.VDD_1V8)
        self.RSTN.reference.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))

        # Set voltages
        self.eMMC.VDD_INTERNAL.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
        self.VDD_3V3.voltage.merge(F.Range.from_center_rel(3.3 * P.V, 0.05))
        self.VDD_1V8.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))
