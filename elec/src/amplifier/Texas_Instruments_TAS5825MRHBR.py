# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class _Texas_Instruments_TAS5825MRHBR(Module):
    """
    TODO: Docstring describing your module

    Dual Channel 38Wx1@8Ω VQFN-32(5x5) Audio Amplifiers ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    BST_Aplus: F.Electrical  # pin: 1
    OUT_Aplus: F.Electrical  # pin: 2
    DGND: F.Electrical  # pin: 5
    DVDD: F.Electrical  # pin: 6
    VR_DIG: F.Electrical  # pin: 7
    ADR: F.Electrical  # pin: 8
    GPIO0: F.Electrical  # pin: 9
    GPIO1: F.Electrical  # pin: 10
    GPIO2: F.Electrical  # pin: 11
    LRCLK: F.Electrical  # pin: 12
    SCLK: F.Electrical  # pin: 13
    SDIN: F.Electrical  # pin: 14
    SDA: F.Electrical  # pin: 15
    SCL: F.Electrical  # pin: 16
    PDNh: F.Electrical  # pin: 17
    GVDD: F.Electrical  # pin: 18
    AVDD: F.Electrical  # pin: 19
    AGND: F.Electrical  # pin: 20
    PVDD: F.Electrical  # pins: 3, 4, 21, 22
    OUT_Bplus: F.Electrical  # pin: 23
    BST_Bplus: F.Electrical  # pin: 24
    PGND: F.Electrical  # pins: 25, 26, 31, 32
    OUT_B_: F.Electrical  # pin: 27
    BST_B_: F.Electrical  # pin: 28
    BST_A_: F.Electrical  # pin: 29
    OUT_A_: F.Electrical  # pin: 30
    EP: F.Electrical  # pin: 33

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C471049"})
    designator_prefix = L.f_field(F.has_designator_prefix)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Texas Instruments",
            DescriptiveProperties.partno: "TAS5825MRHBR",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_1912202033_Texas-Instruments-TAS5825MRHBR_C471049.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.BST_Aplus,
                "2": self.OUT_Aplus,
                "3": self.PVDD,
                "4": self.PVDD,
                "5": self.DGND,
                "6": self.DVDD,
                "7": self.VR_DIG,
                "8": self.ADR,
                "9": self.GPIO0,
                "10": self.GPIO1,
                "11": self.GPIO2,
                "12": self.LRCLK,
                "13": self.SCLK,
                "14": self.SDIN,
                "15": self.SDA,
                "16": self.SCL,
                "17": self.PDNh,
                "18": self.GVDD,
                "19": self.AVDD,
                "20": self.AGND,
                "21": self.PVDD,
                "22": self.PVDD,
                "23": self.OUT_Bplus,
                "24": self.BST_Bplus,
                "25": self.PGND,
                "26": self.PGND,
                "27": self.OUT_B_,
                "28": self.BST_B_,
                "29": self.BST_A_,
                "30": self.OUT_A_,
                "31": self.PGND,
                "32": self.PGND,
                "33": self.EP,
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


class OutputStage(Module):
    """
    Output stage for the TAS5825MRHBR amplifier
    """

    output: F.DifferentialPair
    input: F.DifferentialPair
    bootstrap: F.DifferentialPair
    reference: F.ElectricPower

    # Components
    inductor_pos: F.Inductor
    inductor_neg: F.Inductor
    bootstrap_pos: F.Capacitor
    bootstrap_neg: F.Capacitor
    output_cap_pos: F.Capacitor
    output_cap_neg: F.Capacitor

    def __preinit__(self):
        # Connections
        self.input.p.line.connect_via(self.inductor_pos, self.output.p.line)
        self.input.n.line.connect_via(self.inductor_neg, self.output.n.line)

        self.bootstrap.p.line.connect_via(self.bootstrap_pos, self.input.p.line)
        self.bootstrap.n.line.connect_via(self.bootstrap_neg, self.input.n.line)

        self.output.p.line.connect_via(self.output_cap_pos, self.reference.lv)
        self.output.n.line.connect_via(self.output_cap_neg, self.reference.lv)

        # Parameterize
        # self.inductor_pos.inductance.constrain_subset(
        #   L.Range.from_center_rel(10 * P.uH, 0.3))
        # self.inductor_neg.inductance.constrain_subset(
        #   L.Range.from_center_rel(10 * P.uH, 0.3))
        # self.inductor_pos.max_current.constrain_subset(L.Range(4 * P.A, 6 * P.A))
        # self.inductor_neg.max_current.constrain_subset(L.Range(4 * P.A, 6 * P.A))
        self.inductor_pos.add(F.has_descriptive_properties_defined({"LCSC": "C167223"}))
        self.inductor_neg.add(F.has_descriptive_properties_defined({"LCSC": "C167223"}))

        self.bootstrap_pos.capacitance.constrain_subset(
            L.Range.from_center_rel(470 * P.nF, 0.1)
        )
        self.bootstrap_neg.capacitance.constrain_subset(
            L.Range.from_center_rel(470 * P.nF, 0.1)
        )
        self.bootstrap_pos.max_voltage.constrain_ge(30 * P.V)
        self.bootstrap_neg.max_voltage.constrain_ge(30 * P.V)
        self.bootstrap_pos.add(F.has_package(F.has_package.Package.C0603))
        self.bootstrap_neg.add(F.has_package(F.has_package.Package.C0603))

        self.output_cap_pos.capacitance.constrain_subset(
            L.Range.from_center_rel(680 * P.nF, 0.1)
        )
        self.output_cap_neg.capacitance.constrain_subset(
            L.Range.from_center_rel(680 * P.nF, 0.1)
        )
        self.output_cap_pos.max_voltage.constrain_ge(30 * P.V)
        self.output_cap_neg.max_voltage.constrain_ge(30 * P.V)
        self.output_cap_pos.add(F.has_package(F.has_package.Package.C0805))
        self.output_cap_neg.add(F.has_package(F.has_package.Package.C0805))


class Texas_Instruments_TAS5825MRHBR(Module):
    """
    Dual Channel 38Wx1@8Ω VQFN-32(5x5) Audio Amplifiers ROHS
    """

    # Power
    power_pvdd: F.ElectricPower
    power_dvdd: F.ElectricPower

    i2c: F.I2C
    i2s: F.I2S
    fault: F.ElectricLogic
    mute: F.ElectricLogic
    warn: F.ElectricLogic
    pdn: F.ElectricLogic
    output_a: F.DifferentialPair
    output_b: F.DifferentialPair

    # Components
    amplifier: _Texas_Instruments_TAS5825MRHBR
    output_stage_a: OutputStage
    output_stage_b: OutputStage
    address_resistor: F.Resistor
    vr_dig_cap: F.Capacitor
    gvdd_cap: F.Capacitor
    avdd_cap: F.Capacitor

    def __preinit__(self):
        # Connect all references

        # Connect output stages
        self.amplifier.OUT_Aplus.connect(self.output_stage_a.input.p.line)
        self.amplifier.OUT_A_.connect(self.output_stage_a.input.n.line)
        self.amplifier.OUT_Bplus.connect(self.output_stage_b.input.p.line)
        self.amplifier.OUT_B_.connect(self.output_stage_b.input.n.line)
        self.amplifier.BST_Aplus.connect(self.output_stage_a.bootstrap.p.line)
        self.amplifier.BST_A_.connect(self.output_stage_a.bootstrap.n.line)
        self.amplifier.BST_Bplus.connect(self.output_stage_b.bootstrap.p.line)
        self.amplifier.BST_B_.connect(self.output_stage_b.bootstrap.n.line)

        self.output_stage_a.output.connect(self.output_a)
        self.output_stage_b.output.connect(self.output_b)

        self.output_stage_a.reference.connect(self.power_dvdd)
        self.output_stage_b.reference.connect(self.power_dvdd)

        # Decoupling capacitors
        # PVDD decoupling
        pvdd_multicap = self.power_pvdd.decoupled.decouple(owner=self, count=6)
        for cap in pvdd_multicap.capacitors[:3]:
            cap.add(F.has_package(F.has_package.Package.C0805))
            cap.capacitance.constrain_subset(L.Range.from_center_rel(22 * P.uF, 0.2))

        for cap in pvdd_multicap.capacitors[3:]:
            cap.add(F.has_package(F.has_package.Package.C0402))
            cap.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))

        # DVDD decoupling
        dvdd_caps = self.power_dvdd.decoupled.decouple(owner=self, count=2)

        dvdd_caps.capacitors[0].add(F.has_package(F.has_package.Package.C0603))
        dvdd_caps.capacitors[0].capacitance.constrain_subset(
            L.Range.from_center_rel(4.7 * P.uF, 0.2)
        )

        dvdd_caps.capacitors[1].add(F.has_package(F.has_package.Package.C0402))
        dvdd_caps.capacitors[1].capacitance.constrain_subset(
            L.Range.from_center_rel(100 * P.nF, 0.2)
        )

        # Net naming
        # F.Net.with_name("PVDD").part_of.connect(self.power_pvdd.hv)
        # F.Net.with_name("DVDD").part_of.connect(self.power_dvdd.hv)
        # F.Net.with_name("GND").part_of.connect(self.power_pvdd.lv)

        # Power
        self.power_pvdd.hv.connect(self.amplifier.PVDD)
        self.power_dvdd.hv.connect(self.amplifier.DVDD)
        self.power_pvdd.lv.connect(
            self.amplifier.PGND,
            self.power_dvdd.lv,
            self.amplifier.AGND,
            self.amplifier.DGND,
            self.amplifier.EP,
        )

        # I2C
        self.i2c.scl.line.connect(self.amplifier.SCL)
        self.i2c.sda.line.connect(self.amplifier.SDA)

        # I2S
        self.i2s.sck.line.connect(self.amplifier.SCLK)
        self.i2s.ws.line.connect(self.amplifier.LRCLK)
        self.i2s.sd.line.connect(self.amplifier.SDIN)

        # Control signals
        self.fault.line.connect(self.amplifier.GPIO0)
        self.mute.line.connect(self.amplifier.GPIO1)
        self.warn.line.connect(self.amplifier.GPIO2)
        self.pdn.line.connect(self.amplifier.PDNh)

        # Pullups for control signals
        for signal in [self.fault, self.mute, self.warn, self.pdn]:
            signal.get_trait(F.ElectricLogic.can_be_pulled).pull(up=True, owner=self)
            pullup = signal.get_trait(F.ElectricLogic.has_pulls).get_pulls()[0]
            assert pullup is not None
            pullup.add(F.has_package(F.has_package.Package.R0402))
            pullup.resistance.constrain_subset(
                L.Range.from_center_rel(10 * P.kohm, 0.05)
            )

        # Decoupling for internal thing
        self.amplifier.VR_DIG.connect_via(self.vr_dig_cap, self.power_pvdd.lv)
        self.amplifier.GVDD.connect_via(self.gvdd_cap, self.power_dvdd.lv)
        self.amplifier.AVDD.connect_via(self.avdd_cap, self.power_dvdd.lv)

        self.vr_dig_cap.add(F.has_package(F.has_package.Package.C0402))
        self.gvdd_cap.add(F.has_package(F.has_package.Package.C0402))
        self.avdd_cap.add(F.has_package(F.has_package.Package.C0402))

        self.vr_dig_cap.capacitance.constrain_subset(
            L.Range.from_center_rel(1 * P.uF, 0.2)
        )
        self.gvdd_cap.capacitance.constrain_subset(
            L.Range.from_center_rel(1 * P.uF, 0.2)
        )
        self.avdd_cap.capacitance.constrain_subset(
            L.Range.from_center_rel(1 * P.uF, 0.2)
        )

        # Address resistor
        self.amplifier.ADR.connect_via(self.address_resistor, self.power_dvdd.lv)
        self.address_resistor.add(F.has_package(F.has_package.Package.R0402))
        self.address_resistor.resistance.constrain_subset(
            L.Range.from_center_rel(10 * P.ohm, 0.5)
        )
