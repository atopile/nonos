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


class _SK_HYNIX_H9HCNNNBKUMLXR_NEE(Module):
    """
    TODO: Docstring describing your module

    16 Gbit FBGA-200(10x15) DDR SDRAM ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    ZQ0: F.Electrical
    DQ11a: F.Electrical
    CA4a: F.Electrical
    CA1b: F.Electrical
    CA5b: F.Electrical
    CA0b: F.Electrical
    DQ14a: F.Electrical
    CK_ca: F.Electrical
    DQS1_ta: F.Electrical
    CA0a: F.Electrical
    VSS: F.Electrical
    CS0b: F.Electrical
    DQ9b: F.Electrical
    CK_ta: F.Electrical
    DQ4b: F.Electrical
    DQ12a: F.Electrical
    DQ3b: F.Electrical
    CA3a: F.Electrical
    DQS0_tb: F.Electrical
    DQ7a: F.Electrical
    CK_cb: F.Electrical
    DQ9a: F.Electrical
    DMI1b: F.Electrical
    DQ0b: F.Electrical
    DQ0a: F.Electrical
    CA2a: F.Electrical
    DQS0_ca: F.Electrical
    CA3b: F.Electrical
    NC: F.Electrical
    DQ13a: F.Electrical
    VDD1: F.Electrical
    CA4b: F.Electrical
    DQ2b: F.Electrical
    DQ6b: F.Electrical
    DMI0b: F.Electrical
    DQ1a: F.Electrical
    DQ5a: F.Electrical
    DQ15a: F.Electrical
    DNU: F.Electrical
    VDDQ: F.Electrical
    CA5a: F.Electrical
    DQ11b: F.Electrical
    DQ14b: F.Electrical
    DMI0a: F.Electrical
    DQ5b: F.Electrical
    DQ13b: F.Electrical
    DQ2a: F.Electrical
    DQ8b: F.Electrical
    RESET: F.Electrical
    DQ4a: F.Electrical
    CKE0b: F.Electrical
    CA2b: F.Electrical
    DQS1_cb: F.Electrical
    ODTb: F.Electrical
    DQ7b: F.Electrical
    DMI1a: F.Electrical
    DQS1_tb: F.Electrical
    DQ8a: F.Electrical
    CK_tb: F.Electrical
    DQS0_cb: F.Electrical
    DQ15b: F.Electrical
    DQS1_ca: F.Electrical
    VDD2: F.Electrical
    DQS0_ta: F.Electrical
    CS0a: F.Electrical
    DQ10a: F.Electrical
    DQ3a: F.Electrical
    DQ12b: F.Electrical
    CKE0a: F.Electrical
    DQ1b: F.Electrical
    DQ10b: F.Electrical
    CA1a: F.Electrical
    ODTa: F.Electrical
    DQ6a: F.Electrical

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C21912322"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "SK HYNIX",
            DescriptiveProperties.partno: "H9HCNNNBKUMLXR-NEE",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2403081819_SK-HYNIX-H9HCNNNBKUMLXR-NEE_C21912322.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "A1": self.DNU,
                "A10": self.VSS,
                "A11": self.DNU,
                "A12": self.DNU,
                "A2": self.DNU,
                "A3": self.VSS,
                "A4": self.VDD2,
                "A5": self.ZQ0,
                "A8": self.NC,
                "A9": self.VDD2,
                "AA1": self.DNU,
                "AA10": self.VDDQ,
                "AA11": self.DQ8b,
                "AA12": self.DNU,
                "AA2": self.DQ0b,
                "AA3": self.VDDQ,
                "AA4": self.DQ7b,
                "AA5": self.VDDQ,
                "AA8": self.VDDQ,
                "AA9": self.DQ15b,
                "AB1": self.DNU,
                "AB10": self.VSS,
                "AB11": self.DNU,
                "AB12": self.DNU,
                "AB2": self.DNU,
                "AB3": self.VSS,
                "AB4": self.VDD2,
                "AB5": self.VSS,
                "AB8": self.VSS,
                "AB9": self.VDD2,
                "B1": self.DNU,
                "B10": self.VDDQ,
                "B11": self.DQ8a,
                "B12": self.DNU,
                "B2": self.DQ0a,
                "B3": self.VDDQ,
                "B4": self.DQ7a,
                "B5": self.VDDQ,
                "B8": self.VDDQ,
                "B9": self.DQ15a,
                "C1": self.VSS,
                "C10": self.DMI1a,
                "C11": self.DQ9a,
                "C12": self.VSS,
                "C2": self.DQ1a,
                "C3": self.DMI0a,
                "C4": self.DQ6a,
                "C5": self.VSS,
                "C8": self.VSS,
                "C9": self.DQ14a,
                "D1": self.VDDQ,
                "D10": self.DQS1_ta,
                "D11": self.VSS,
                "D12": self.VDDQ,
                "D2": self.VSS,
                "D3": self.DQS0_ta,
                "D4": self.VSS,
                "D5": self.VDDQ,
                "D8": self.VDDQ,
                "D9": self.VSS,
                "E1": self.VSS,
                "E10": self.DQS1_ca,
                "E11": self.DQ10a,
                "E12": self.VSS,
                "E2": self.DQ2a,
                "E3": self.DQS0_ca,
                "E4": self.DQ5a,
                "E5": self.VSS,
                "E8": self.VSS,
                "E9": self.DQ13a,
                "F1": self.VDD1,
                "F10": self.VDDQ,
                "F11": self.DQ11a,
                "F12": self.VDD1,
                "F2": self.DQ3a,
                "F3": self.VDDQ,
                "F4": self.DQ4a,
                "F5": self.VDD2,
                "F8": self.VDD2,
                "F9": self.DQ12a,
                "G1": self.VSS,
                "G10": self.VSS,
                "G11": self.NC,
                "G12": self.VSS,
                "G2": self.ODTa,
                "G3": self.VSS,
                "G4": self.VDD1,
                "G5": self.VSS,
                "G8": self.VSS,
                "G9": self.VDD1,
                "H1": self.VDD2,
                "H10": self.CA3a,
                "H11": self.CA4a,
                "H12": self.VDD2,
                "H2": self.CA0a,
                "H3": self.NC,
                "H4": self.CS0a,
                "H5": self.VDD2,
                "H8": self.VDD2,
                "H9": self.CA2a,
                "J1": self.VSS,
                "J10": self.VSS,
                "J11": self.CA5a,
                "J12": self.VSS,
                "J2": self.CA1a,
                "J3": self.VSS,
                "J4": self.CKE0a,
                "J5": self.NC,
                "J8": self.CK_ta,
                "J9": self.CK_ca,
                "K1": self.VDD2,
                "K10": self.VDD2,
                "K11": self.VSS,
                "K12": self.VDD2,
                "K2": self.VSS,
                "K3": self.VDD2,
                "K4": self.VSS,
                "K5": self.NC,
                "K8": self.NC,
                "K9": self.VSS,
                "N1": self.VDD2,
                "N10": self.VDD2,
                "N11": self.VSS,
                "N12": self.VDD2,
                "N2": self.VSS,
                "N3": self.VDD2,
                "N4": self.VSS,
                "N5": self.NC,
                "N8": self.NC,
                "N9": self.VSS,
                "P1": self.VSS,
                "P10": self.VSS,
                "P11": self.CA5b,
                "P12": self.VSS,
                "P2": self.CA1b,
                "P3": self.VSS,
                "P4": self.CKE0b,
                "P5": self.NC,
                "P8": self.CK_tb,
                "P9": self.CK_cb,
                "R1": self.VDD2,
                "R10": self.CA3b,
                "R11": self.CA4b,
                "R12": self.VDD2,
                "R2": self.CA0b,
                "R3": self.NC,
                "R4": self.CS0b,
                "R5": self.VDD2,
                "R8": self.VDD2,
                "R9": self.CA2b,
                "T1": self.VSS,
                "T10": self.VSS,
                "T11": self.RESET,
                "T12": self.VSS,
                "T2": self.ODTb,
                "T3": self.VSS,
                "T4": self.VDD1,
                "T5": self.VSS,
                "T8": self.VSS,
                "T9": self.VDD1,
                "U1": self.VDD1,
                "U10": self.VDDQ,
                "U11": self.DQ11b,
                "U12": self.VDD1,
                "U2": self.DQ3b,
                "U3": self.VDDQ,
                "U4": self.DQ4b,
                "U5": self.VDD2,
                "U8": self.VDD2,
                "U9": self.DQ12b,
                "V1": self.VSS,
                "V10": self.DQS1_cb,
                "V11": self.DQ10b,
                "V12": self.VSS,
                "V2": self.DQ2b,
                "V3": self.DQS0_cb,
                "V4": self.DQ5b,
                "V5": self.VSS,
                "V8": self.VSS,
                "V9": self.DQ13b,
                "W1": self.VDDQ,
                "W10": self.DQS1_tb,
                "W11": self.VSS,
                "W12": self.VDDQ,
                "W2": self.VSS,
                "W3": self.DQS0_tb,
                "W4": self.VSS,
                "W5": self.VDDQ,
                "W8": self.VDDQ,
                "W9": self.VSS,
                "Y1": self.VSS,
                "Y10": self.DMI1b,
                "Y11": self.DQ9b,
                "Y12": self.VSS,
                "Y2": self.DQ1b,
                "Y3": self.DMI0b,
                "Y4": self.DQ6b,
                "Y5": self.VSS,
                "Y8": self.VSS,
                "Y9": self.DQ14b,
            }
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass


class SK_HYNIX_H9HCNNNBKUMLXR_NEE(Module):
    RAM: _SK_HYNIX_H9HCNNNBKUMLXR_NEE

    # Interfaces - Power
    VDD_1V8: F.ElectricPower
    NVCC_DRAM_1V1: F.ElectricPower
    DRAM_ODT_CA_A: F.ElectricPower  # On-die termination - Connect to NVCC_DRAM_1V1
    DRAM_ODT_CA_B: F.ElectricPower  # On-die termination - Connect to NVCC_DRAM_1V1

    # Interfaces - Data
    DRAM_DATA_A = times(16, F.ElectricLogic)  # Data
    DRAM_DATA_B = times(16, F.ElectricLogic)  # Data
    DRAM_DMI_A = times(2, F.ElectricLogic)  # Data mask (bit inversion)
    DRAM_DMI_B = times(2, F.ElectricLogic)  # Data mask (bit inversion)
    DRAM_SDQS_A = times(2, F.DifferentialPair)  # Data strobe (differential)
    DRAM_SDQS_B = times(2, F.DifferentialPair)  # Data strobe (differential)
    DRAM_CA_A = times(6, F.ElectricLogic)  # Command address
    DRAM_CA_B = times(6, F.ElectricLogic)  # Command address
    DRAM_CK_A: F.DifferentialPair  # Clock
    DRAM_CK_B: F.DifferentialPair  # Clock
    DRAM_CKE_A = times(2, F.ElectricLogic)  # Clock enable
    DRAM_CKE_B = times(2, F.ElectricLogic)  # Clock enable
    DRAM_nCS_A = times(2, F.ElectricLogic)  # Chip select
    DRAM_nCS_B = times(2, F.ElectricLogic)  # Chip select
    DRAM_nRESET: F.ElectricLogic  # Reset
    DRAM_ZQ0: F.ElectricLogic  # On-die termination calibration

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # Power Connections
        self.VDD_1V8.hv.connect(self.RAM.VDD1)
        self.NVCC_DRAM_1V1.hv.connect(
            self.RAM.VDD2,
            self.RAM.VDDQ,
            self.DRAM_ODT_CA_A.hv,
            self.DRAM_ODT_CA_B.hv,
        )

        self.VDD_1V8.lv.connect(
            self.RAM.VSS,
            self.NVCC_DRAM_1V1.lv,
            self.DRAM_ODT_CA_A.lv,
            self.DRAM_ODT_CA_B.lv,
        )

        # F.Net.with_name("VDD_1V8").part_of.connect(self.VDD_1V8.hv)
        # F.Net.with_name("NVCC_DRAM_1V1").part_of.connect(self.NVCC_DRAM_1V1.hv)
        # F.Net.with_name("GND").part_of.connect(self.RAM.VSS)

        # Decoupling capacitors
        VDD_1V8_CAP_PROPERTIES = [
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
        ]

        VDD_1V8_CAPS = []

        for props in VDD_1V8_CAP_PROPERTIES:
            cap = self.VDD_1V8.decoupled.decouple()
            cap.add(F.has_footprint_requirement_defined([(props["footprint"], 2)]))
            cap.capacitance.merge(F.Range.from_center_rel(props["value"], 0.2))
            VDD_1V8_CAPS.append(cap)

        # NVCC_DRAM_1V1
        NVCC_DRAM_1V1_CAP_PROPERTIES = [
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 10 * P.uF, "footprint": "0402"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
            {"value": 220 * P.nF, "footprint": "0201"},
        ]

        NVCC_DRAM_1V1_CAPS = []

        for props in NVCC_DRAM_1V1_CAP_PROPERTIES:
            cap = self.NVCC_DRAM_1V1.decoupled.decouple()
            cap.add(F.has_footprint_requirement_defined([(props["footprint"], 2)]))
            cap.capacitance.merge(F.Range.from_center_rel(props["value"], 0.2))
            NVCC_DRAM_1V1_CAPS.append(cap)

        # Connect data lines A
        self.RAM.DQ0a.connect(self.DRAM_DATA_A[0].signal)
        self.RAM.DQ1a.connect(self.DRAM_DATA_A[1].signal)
        self.RAM.DQ2a.connect(self.DRAM_DATA_A[2].signal)
        self.RAM.DQ3a.connect(self.DRAM_DATA_A[3].signal)
        self.RAM.DQ4a.connect(self.DRAM_DATA_A[4].signal)
        self.RAM.DQ5a.connect(self.DRAM_DATA_A[5].signal)
        self.RAM.DQ6a.connect(self.DRAM_DATA_A[6].signal)
        self.RAM.DQ7a.connect(self.DRAM_DATA_A[7].signal)
        self.RAM.DQ8a.connect(self.DRAM_DATA_A[8].signal)
        self.RAM.DQ9a.connect(self.DRAM_DATA_A[9].signal)
        self.RAM.DQ10a.connect(self.DRAM_DATA_A[10].signal)
        self.RAM.DQ11a.connect(self.DRAM_DATA_A[11].signal)
        self.RAM.DQ12a.connect(self.DRAM_DATA_A[12].signal)
        self.RAM.DQ13a.connect(self.DRAM_DATA_A[13].signal)
        self.RAM.DQ14a.connect(self.DRAM_DATA_A[14].signal)
        self.RAM.DQ15a.connect(self.DRAM_DATA_A[15].signal)

        # Connect data lines B
        self.RAM.DQ0b.connect(self.DRAM_DATA_B[0].signal)
        self.RAM.DQ1b.connect(self.DRAM_DATA_B[1].signal)
        self.RAM.DQ2b.connect(self.DRAM_DATA_B[2].signal)
        self.RAM.DQ3b.connect(self.DRAM_DATA_B[3].signal)
        self.RAM.DQ4b.connect(self.DRAM_DATA_B[4].signal)
        self.RAM.DQ5b.connect(self.DRAM_DATA_B[5].signal)
        self.RAM.DQ6b.connect(self.DRAM_DATA_B[6].signal)
        self.RAM.DQ7b.connect(self.DRAM_DATA_B[7].signal)
        self.RAM.DQ8b.connect(self.DRAM_DATA_B[8].signal)
        self.RAM.DQ9b.connect(self.DRAM_DATA_B[9].signal)
        self.RAM.DQ10b.connect(self.DRAM_DATA_B[10].signal)
        self.RAM.DQ11b.connect(self.DRAM_DATA_B[11].signal)
        self.RAM.DQ12b.connect(self.DRAM_DATA_B[12].signal)
        self.RAM.DQ13b.connect(self.DRAM_DATA_B[13].signal)
        self.RAM.DQ14b.connect(self.DRAM_DATA_B[14].signal)
        self.RAM.DQ15b.connect(self.DRAM_DATA_B[15].signal)

        # Connect DMI lines A
        self.RAM.DMI0a.connect(self.DRAM_DMI_A[0].signal)
        self.RAM.DMI1a.connect(self.DRAM_DMI_A[1].signal)

        # Connect DMI lines B
        self.RAM.DMI0b.connect(self.DRAM_DMI_B[0].signal)
        self.RAM.DMI1b.connect(self.DRAM_DMI_B[1].signal)

        # Connect data strobe lines A
        self.RAM.DQS0_ta.connect(self.DRAM_SDQS_A[0].p.signal)
        self.RAM.DQS0_ca.connect(self.DRAM_SDQS_A[0].n.signal)
        self.RAM.DQS1_ta.connect(self.DRAM_SDQS_A[1].p.signal)
        self.RAM.DQS1_ca.connect(self.DRAM_SDQS_A[1].n.signal)

        # Connect data strobe lines B
        self.RAM.DQS0_tb.connect(self.DRAM_SDQS_B[0].p.signal)
        self.RAM.DQS0_cb.connect(self.DRAM_SDQS_B[0].n.signal)
        self.RAM.DQS1_tb.connect(self.DRAM_SDQS_B[1].p.signal)
        self.RAM.DQS1_cb.connect(self.DRAM_SDQS_B[1].n.signal)

        # Connect command address lines A
        self.RAM.CA0a.connect(self.DRAM_CA_A[0].signal)
        self.RAM.CA1a.connect(self.DRAM_CA_A[1].signal)
        self.RAM.CA2a.connect(self.DRAM_CA_A[2].signal)
        self.RAM.CA3a.connect(self.DRAM_CA_A[3].signal)
        self.RAM.CA4a.connect(self.DRAM_CA_A[4].signal)
        self.RAM.CA5a.connect(self.DRAM_CA_A[5].signal)

        # Connect command address lines B
        self.RAM.CA0b.connect(self.DRAM_CA_B[0].signal)
        self.RAM.CA1b.connect(self.DRAM_CA_B[1].signal)
        self.RAM.CA2b.connect(self.DRAM_CA_B[2].signal)
        self.RAM.CA3b.connect(self.DRAM_CA_B[3].signal)
        self.RAM.CA4b.connect(self.DRAM_CA_B[4].signal)
        self.RAM.CA5b.connect(self.DRAM_CA_B[5].signal)

        # Connect clock lines A
        self.RAM.CK_ta.connect(self.DRAM_CK_A.p.signal)
        self.RAM.CK_ca.connect(self.DRAM_CK_A.n.signal)

        # Connect clock lines B
        self.RAM.CK_tb.connect(self.DRAM_CK_B.p.signal)
        self.RAM.CK_cb.connect(self.DRAM_CK_B.n.signal)

        # Connect clock enable lines A
        self.RAM.CKE0a.connect(self.DRAM_CKE_A[0].signal)
        # self.RAM.CKE1a.connect(self.DRAM_CKE_A[1].signal) # chip only has one CKE line

        # Connect clock enable lines B
        self.RAM.CKE0b.connect(self.DRAM_CKE_B[0].signal)
        # self.RAM.CKE1b.connect(self.DRAM_CKE_B[1].signal) # chip only has one CKE line

        # Connect chip select lines A
        self.RAM.CS0a.connect(self.DRAM_nCS_A[0].signal)
        # self.RAM.CS1a.connect(self.DRAM_nCS_A[1].signal) # chip only has one CS line

        # Connect chip select lines B
        self.RAM.CS0b.connect(self.DRAM_nCS_B[0].signal)
        # self.RAM.CS1b.connect(self.DRAM_nCS_B[1].signal) # chip only has one CS line

        # Connect ODT lines A
        self.RAM.ODTa.connect(self.DRAM_ODT_CA_A.hv)
        # self.RAM.ODT1a.connect(self.DRAM_ODT_CA_A.signal) # chip only has one ODT line

        # Connect ODT lines B
        self.RAM.ODTb.connect(self.DRAM_ODT_CA_B.hv)
        # self.RAM.ODT1b.connect(self.DRAM_ODT_CA_B.signal) # chip only has one ODT line

        # Connect reset line
        self.DRAM_nRESET.signal.connect(self.RAM.RESET)

        # Connect ZQ0 line
        zq0_r = F.Resistor()
        zq0_r.add(F.has_footprint_requirement_defined([("0201", 2)]))
        zq0_r.resistance.merge(F.Range.from_center_rel(240 * P.ohm, 0.01))
        self.RAM.ZQ0.connect_via(zq0_r, self.DRAM_ZQ0.signal)

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        # TODO: voltage currently not passed around by connections, once parameters are merged alot of this can be removed
        # Set voltage of power rails
        self.VDD_1V8.voltage.merge(F.Range.from_center_rel(1.8 * P.volt, 0.05))
        self.NVCC_DRAM_1V1.voltage.merge(F.Range.from_center_rel(1.1 * P.volt, 0.05))
        self.DRAM_ODT_CA_A.voltage.merge(F.Range.from_center_rel(1.1 * P.volt, 0.05))
        self.DRAM_ODT_CA_B.voltage.merge(F.Range.from_center_rel(1.1 * P.volt, 0.05))

        for signal in [
            self.DRAM_CK_A,
            self.DRAM_CK_B,
            *self.DRAM_SDQS_A,
            *self.DRAM_SDQS_B,
        ]:
            signal.p.reference.connect(self.NVCC_DRAM_1V1)
            signal.p.reference.voltage.merge(
                F.Range.from_center_rel(1.1 * P.volt, 0.05)
            )
            signal.n.reference.connect(self.NVCC_DRAM_1V1)
            signal.n.reference.voltage.merge(
                F.Range.from_center_rel(1.1 * P.volt, 0.05)
            )

        # Set voltage of all data, control and address lines
        for signal in (
            self.DRAM_DATA_A
            + self.DRAM_DATA_B
            + self.DRAM_DMI_A
            + self.DRAM_DMI_B
            + self.DRAM_CA_A
            + self.DRAM_CA_B
            + self.DRAM_CKE_A
            + self.DRAM_CKE_B
            + self.DRAM_nCS_A
            + self.DRAM_nCS_B
        ):
            signal.reference.connect(self.NVCC_DRAM_1V1)
            signal.reference.voltage.merge(F.Range.from_center_rel(1.1 * P.volt, 0.05))

        # Set voltage of reset and ZQ lines
        self.DRAM_nRESET.reference.connect(self.NVCC_DRAM_1V1)
        self.DRAM_ZQ0.reference.connect(self.NVCC_DRAM_1V1)

        self.DRAM_nRESET.reference.voltage.merge(
            F.Range.from_center_rel(1.1 * P.volt, 0.05)
        )
        self.DRAM_ZQ0.reference.voltage.merge(
            F.Range.from_center_rel(1.1 * P.volt, 0.05)
        )


class App(Module):
    RAM: SK_HYNIX_H9HCNNNBKUMLXR_NEE
