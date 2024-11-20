# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging
from os import times

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

    NC: F.Electrical

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
                "A1": self.NC,
                "A10": self.NC,
                "A11": self.NC,
                "A12": self.NC,
                "A13": self.NC,
                "A14": self.NC,
                "A2": self.NC,
                "A3": self.DAT[0].signal,
                "A4": self.DAT[1].signal,
                "A5": self.DAT[2].signal,
                "A6": self.VSS,
                "A7": self.NC,
                "A8": self.NC,
                "A9": self.NC,
                "B1": self.NC,
                "B10": self.NC,
                "B11": self.NC,
                "B12": self.NC,
                "B13": self.NC,
                "B14": self.NC,
                "B2": self.DAT[3].signal,
                "B3": self.DAT[4].signal,
                "B4": self.DAT[5].signal,
                "B5": self.DAT[6].signal,
                "B6": self.DAT[7].signal,
                "B7": self.NC,
                "B8": self.NC,
                "B9": self.NC,
                "C1": self.NC,
                "C10": self.NC,
                "C11": self.NC,
                "C12": self.NC,
                "C13": self.NC,
                "C14": self.NC,
                "C2": self.VDDI,
                "C3": self.NC,
                "C4": self.VSS,
                "C5": self.NC,
                "C6": self.VDD,
                "C7": self.NC,
                "C8": self.NC,
                "C9": self.NC,
                "D1": self.NC,
                "D12": self.NC,
                "D13": self.NC,
                "D14": self.NC,
                "D2": self.NC,
                "D3": self.NC,
                "D4": self.NC,
                "E1": self.NC,
                "E10": self.NC,
                "E12": self.NC,
                "E13": self.NC,
                "E14": self.NC,
                "E2": self.NC,
                "E3": self.NC,
                "E5": self.NC,
                "E6": self.VDDF,
                "E7": self.VSS,
                "E8": self.NC,
                "E9": self.NC,
                "F1": self.NC,
                "F10": self.NC,
                "F12": self.NC,
                "F13": self.NC,
                "F14": self.NC,
                "F2": self.NC,
                "F3": self.NC,
                "F5": self.VDDF,
                "G1": self.NC,
                "G10": self.NC,
                "G12": self.NC,
                "G13": self.NC,
                "G14": self.NC,
                "G2": self.NC,
                "G3": self.NC,
                "G5": self.VSS,
                "H1": self.NC,
                "H10": self.VSS,
                "H12": self.NC,
                "H13": self.NC,
                "H14": self.NC,
                "H2": self.NC,
                "H3": self.NC,
                "H5": self.DATA_STROBE.signal,
                "J1": self.NC,
                "J10": self.VDDF,
                "J12": self.NC,
                "J13": self.NC,
                "J14": self.NC,
                "J2": self.NC,
                "J3": self.NC,
                "J5": self.VSS,
                "K1": self.NC,
                "K10": self.NC,
                "K12": self.NC,
                "K13": self.NC,
                "K14": self.NC,
                "K2": self.NC,
                "K3": self.NC,
                "K5": self.RSTN.signal,
                "K6": self.NC,
                "K7": self.NC,
                "K8": self.VSS,
                "K9": self.VDDF,
                "L1": self.NC,
                "L12": self.NC,
                "L13": self.NC,
                "L14": self.NC,
                "L2": self.NC,
                "L3": self.NC,
                "M1": self.NC,
                "M10": self.NC,
                "M11": self.NC,
                "M12": self.NC,
                "M13": self.NC,
                "M14": self.NC,
                "M2": self.NC,
                "M3": self.NC,
                "M4": self.VDD,
                "M5": self.CMD.signal,
                "M6": self.CLK.signal,
                "M7": self.NC,
                "M8": self.NC,
                "M9": self.NC,
                "N1": self.NC,
                "N10": self.NC,
                "N11": self.NC,
                "N12": self.NC,
                "N13": self.NC,
                "N14": self.NC,
                "N2": self.VSS,
                "N3": self.NC,
                "N4": self.VDD,
                "N5": self.VSS,
                "N6": self.NC,
                "N7": self.NC,
                "N8": self.NC,
                "N9": self.NC,
                "P1": self.NC,
                "P10": self.NC,
                "P11": self.NC,
                "P12": self.NC,
                "P13": self.NC,
                "P14": self.NC,
                "P2": self.NC,
                "P3": self.VDD,
                "P4": self.VSS,
                "P5": self.VDD,
                "P6": self.VSS,
                "P7": self.NC,
                "P8": self.NC,
                "P9": self.NC,
            }
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------
        self.VDD_3V3.hv.connect(self.VDDF)
        self.VDD_1V8.hv.connect(self.VDD)
        self.VDD_INTERNAL.hv.connect(self.VDDI)
        F.ElectricLogic.connect_all_module_references(self, gnd_only=True)

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.VDD_3V3.voltage.merge(F.Range.from_center_rel(3.3 * P.V, 0.05))
        self.VDD_1V8.voltage.merge(F.Range.from_center_rel(1.8 * P.V, 0.05))


class Samsung_KLMBG2JETD_B041(Module):
    """
    Module, contains decoupling capacitors and pullups


    """
    #Interfaces
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

        # Pass through
        for dat in self.DAT:
            dat.connect(self.eMMC.DAT[self.DAT.index(dat)])
        self.DATA_STROBE.connect(self.eMMC.DATA_STROBE)
        self.CMD.connect(self.eMMC.CMD)
        self.CLK.connect(self.eMMC.CLK)
        self.RSTN.connect(self.eMMC.RSTN)

        # Decoupling capacitors
        VDD_3V3_CAPS = (
            self.VDD_3V3.decoupled.decouple()
            .specialize(F.MultiCapacitor(3))
            .capacitors
        )
        VDD_3V3_CAP_FOOTPRINTS = [("0402", 2), ("0201", 2), ("0201", 2)]
        VDD_3V3_CAP_VALUES = [4.7 * P.uF, 220 * P.nF, 220 * P.nF]

        for cap, footprint, value in zip(VDD_3V3_CAPS, VDD_3V3_CAP_FOOTPRINTS, VDD_3V3_CAP_VALUES):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        VDD_1V8_CAPS = (
            self.VDD_1V8.decoupled.decouple()
            .specialize(F.MultiCapacitor(4))
            .capacitors
        )
        VDD_1V8_CAP_FOOTPRINTS = [("0402", 2), ("0201", 2), ("0201", 2), ("0201", 2)]
        VDD_1V8_CAP_VALUES = [10 * P.uF, 220 * P.nF, 220 * P.nF, 220 * P.nF]

        for cap, footprint, value in zip(VDD_1V8_CAPS, VDD_1V8_CAP_FOOTPRINTS, VDD_1V8_CAP_VALUES):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        VDD_INTERNAL_CAPS = (
            self.eMMC.VDD_INTERNAL.decoupled.decouple()
            .specialize(F.MultiCapacitor(2))
            .capacitors 
        )
        VDD_INTERNAL_CAP_FOOTPRINTS = [("0201", 2), ("0201", 2)]
        VDD_INTERNAL_CAP_VALUES = [1 * P.uF, 220 * P.nF]

        for cap, footprint, value in zip(VDD_INTERNAL_CAPS, VDD_INTERNAL_CAP_FOOTPRINTS, VDD_INTERNAL_CAP_VALUES):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

class App(Module):
    eMMC: Samsung_KLMBG2JETD_B041