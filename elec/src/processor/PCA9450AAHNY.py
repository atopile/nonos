# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import itertools
import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)

class BuckOutput(Module):
    """
    Buck output stage containing buck and capacitor
    """
    input: F.ElectricPower
    output: F.ElectricPower
    inductor: F.Inductor

    def __preinit__(self):
        # Connect input HV to output HV through inductor
        self.input.hv.connect_via(self.inductor, self.output.hv)

        # Connect capacitor across output
        self.capacitor = self.output.decoupled.decouple()
        self.capacitor.add(F.has_footprint_requirement_defined([("0603", 2)])) #TODO: can different instances have different number of caps?


class PCA9450AAHNY_IC(Module):
    """
    HVQFN-56 Power Management - Specialized ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # Signals
    SDAL: F.Electrical
    IRQ_B: F.Electrical
    POR_B: F.Electrical
    LX3: F.Electrical
    SDAH: F.Electrical
    BUCK5FB: F.Electrical
    INB26: F.Electrical
    SWOUT: F.Electrical
    SCLH: F.Electrical
    IMB26: F.Electrical
    LX5: F.Electrical
    SD_VSEL: F.Electrical
    LX2: F.Electrical
    SWIN: F.Electrical
    AGND: F.Electrical
    INB13: F.Electrical
    RTC_RESET_B: F.Electrical
    SCLL: F.Electrical
    CLK_32K_OUT: F.Electrical
    BUCK_AGND: F.Electrical
    PMIC_STBY_REQ: F.Electrical
    R_SNSP2: F.Electrical
    LX1: F.Electrical
    R_SNSP1: F.Electrical
    LDO1: F.Electrical
    LDO2: F.Electrical
    SCL: F.Electrical
    LX6: F.Electrical
    INB45: F.Electrical
    XTAL_IN: F.Electrical
    SDA: F.Electrical
    XTAL_OUT: F.Electrical
    LDO4: F.Electrical
    BUCK4FB: F.Electrical
    VSYS: F.Electrical
    BUCK6FB: F.Electrical
    VINT: F.Electrical
    EP: F.Electrical
    INL1: F.Electrical
    R_SNSP3_CFG: F.Electrical
    WDOG_B: F.Electrical
    LDO5: F.Electrical
    LDO3: F.Electrical
    SW_EN: F.Electrical
    PMIC_ON_REQ: F.Electrical
    LX4: F.Electrical
    PMIC_RST_B: F.Electrical

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C5191349"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "NXP Semicon",
            DescriptiveProperties.partno: "PCA9450AAHNY",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2401301159_NXP-Semicon-PCA9450AAHNY_C5191349.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={
                self.AGND: ["AGND"],
                self.BUCK4FB: ["BUCK4FB"],
                self.BUCK5FB: ["BUCK5FB"],
                self.BUCK6FB: ["BUCK6FB"],
                self.BUCK_AGND: ["BUCK_AGND"],
                self.CLK_32K_OUT: ["CLK_32K_OUT"],
                self.EP: ["EP"],
                self.IMB26: ["IMB26"],
                self.INB13: ["INB13"],
                self.INB26: ["INB26"],
                self.INB45: ["INB45"],
                self.INL1: ["INL1"],
                self.IRQ_B: ["IRQ_B"],
                self.LDO1: ["LDO1"],
                self.LDO2: ["LDO2"],
                self.LDO3: ["LDO3"],
                self.LDO4: ["LDO4"],
                self.LDO5: ["LDO5"],
                self.LX1: ["LX1"],
                self.LX2: ["LX2"],
                self.LX3: ["LX3"],
                self.LX4: ["LX4"],
                self.LX5: ["LX5"],
                self.LX6: ["LX6"],
                self.PMIC_ON_REQ: ["PMIC_ON_REQ"],
                self.PMIC_RST_B: ["PMIC_RST_B"],
                self.PMIC_STBY_REQ: ["PMIC_STBY_REQ"],
                self.POR_B: ["POR_B"],
                self.RTC_RESET_B: ["RTC_RESET_B"],
                self.R_SNSP1: ["R_SNSP1"],
                self.R_SNSP2: ["R_SNSP2"],
                self.R_SNSP3_CFG: ["R_SNSP3_CFG"],
                self.SCL: ["SCL"],
                self.SCLH: ["SCLH"],
                self.SCLL: ["SCLL"],
                self.SDA: ["SDA"],
                self.SDAH: ["SDAH"],
                self.SDAL: ["SDAL"],
                self.SD_VSEL: ["SD_VSEL"],
                self.SWIN: ["SWIN"],
                self.SWOUT: ["SWOUT"],
                self.SW_EN: ["SW_EN"],
                self.VINT: ["VINT"],
                self.VSYS: ["VSYS"],
                self.WDOG_B: ["WDOG_B"],
                self.XTAL_IN: ["XTAL_IN"],
                self.XTAL_OUT: ["XTAL_OUT"],
            },
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # Connect buck outputs to power rails
        pass

        # ------------------------------------
        #          parametrization
        # ------------------------------------


class PCA9450AAHNY(Module):
    """
    HVQFN-56 Power Management - Specialized ROHS
    """
    pmic: PCA9450AAHNY_IC

    # Input power
    VSYS_5V: F.ElectricPower
    
    # Output power rails
    NVCC_SNVS_1V8: F.ElectricPower
    VDD_SNVS_0V8: F.ElectricPower
    VDD_SOC_0V8: F.ElectricPower
    VDD_DRAM_0V9: F.ElectricPower
    VDD_PHY_0V9: F.ElectricPower
    VDD_ARM_0V9: F.ElectricPower
    VDDA_1V8: F.ElectricPower
    VDD_1V8: F.ElectricPower
    NVCC_DRAM_1V1: F.ElectricPower
    VCC_3V3: F.ElectricPower
    VDD_PHY_1V2: F.ElectricPower
    NVCC_SD2: F.ElectricPower

    SWOUT: F.ElectricPower

    # Sense inputs
    R_SNSP2: F.ElectricLogic
    R_SNSP1: F.ElectricLogic
    R_SNSP3_CFG: F.ElectricLogic

    # Reset signals
    SYS_nRST: F.ElectricLogic
    PMIC_ON_REQ: F.ElectricLogic
    PMIC_STBY_REQ: F.ElectricLogic
    WDOG_B: F.ElectricLogic

    # Buck outputs
    BUCK1: BuckOutput
    BUCK2: BuckOutput
    BUCK3: BuckOutput
    BUCK4: BuckOutput
    BUCK5: BuckOutput
    BUCK6: BuckOutput

    def __preinit__(self):
        # Set input voltages
        self.VSYS_5V.voltage.merge(5 * P.V)
        self.VDD_SNVS_0V8.voltage.merge(0.8 * P.V)
        self.VDD_SOC_0V8.voltage.merge(0.8 * P.V)
        self.VDD_DRAM_0V9.voltage.merge(0.9 * P.V)
        self.VDD_PHY_0V9.voltage.merge(0.9 * P.V)
        self.VDD_ARM_0V9.voltage.merge(0.9 * P.V)
        self.VDDA_1V8.voltage.merge(1.8 * P.V)
        self.VDD_1V8.voltage.merge(1.8 * P.V)
        self.NVCC_SNVS_1V8.voltage.merge(1.8 * P.V)
        self.NVCC_DRAM_1V1.voltage.merge(1.1 * P.V)
        self.VCC_3V3.voltage.merge(3.3 * P.V)
        self.VDD_PHY_1V2.voltage.merge(1.2 * P.V)
        self.NVCC_SD2.voltage.merge(3.3 * P.V)

        # VSYS_5V
        self.VSYS_5V.hv.connect(self.pmic.INB13, self.pmic.INB26, self.pmic.INB45, self.pmic.INL1)
        self.VSYS_5V.lv.connect(self.pmic.AGND, self.pmic.BUCK_AGND, self.pmic.EP)
        VSYS_5V_CAPS = (
            self.VSYS_5V.decoupled.decouple()
            .specialize(F.MultiCapacitor(10))
            .capacitors
        )
        capacitance_values = [10] * 7 + [2.2] * 3  # in uF
    
        for cap, value in zip(
            VSYS_5V_CAPS, itertools.cycle(capacitance_values)
        ):
            cap.capacitance.merge(F.Range.from_center_rel(value * P.nF, 0.2)) #TODO: update value once API is updated to uF
            cap.add(F.has_footprint_requirement_defined([("0603", 2)]))

        # Set buck input voltages to VSYS_5V        
        self.BUCK1.input.voltage.merge(self.VSYS_5V.voltage)
        self.BUCK2.input.voltage.merge(self.VSYS_5V.voltage)
        self.BUCK3.input.voltage.merge(self.VSYS_5V.voltage)
        self.BUCK4.input.voltage.merge(self.VSYS_5V.voltage)
        self.BUCK5.input.voltage.merge(self.VSYS_5V.voltage)
        self.BUCK6.input.voltage.merge(self.VSYS_5V.voltage)

        # VDD_ARM_09V - Buck 2
        self.BUCK2.inductor.inductance.merge(F.Range.from_center_rel(0.470 * P.uH, 0.3))
        self.BUCK2.inductor.rated_current.merge(F.Range.lower_bound(3 * P.A))
        self.BUCK2.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C97014"}))
        self.BUCK2.capacitor.capacitance.merge(F.Range.from_center_rel(2 * P.nF, 0.2)) #TODO: update value once API is updated 22uF
        self.BUCK2.input.hv.connect(self.pmic.LX2)
        self.BUCK2.input.lv.connect(self.VSYS_5V.lv)
        self.VDD_ARM_0V9.connect(self.BUCK2.output)

        # VDD_SOC_08V - Buck 1
        self.BUCK1.inductor.inductance.merge(F.Range.from_center_rel(0.470 * P.uH, 0.3))
        self.BUCK1.inductor.rated_current.merge(F.Range.lower_bound(3 * P.A))
        self.BUCK1.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C97014"}))
        self.BUCK1.capacitor.capacitance.merge(F.Range.from_center_rel(2 * P.nF, 0.3)) #TODO: update value once API is updated 22uF
        self.BUCK1.input.hv.connect(self.pmic.LX1)
        self.BUCK1.input.lv.connect(self.VSYS_5V.lv)
        self.VDD_SOC_0V8.connect(self.BUCK1.output)

        # VDD_DRAM_09V - Buck 3
        self.BUCK3.inductor.inductance.merge(F.Range.from_center_rel(0.470 * P.uH, 0.3))
        self.BUCK3.inductor.rated_current.merge(F.Range.lower_bound(3 * P.A))
        self.BUCK3.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C97014"}))
        self.BUCK3.capacitor.capacitance.merge(F.Range.from_center_rel(2 * P.nF, 0.3)) #TODO: update value once API is updated 22uF
        self.BUCK3.input.hv.connect(self.pmic.LX3)
        self.BUCK3.input.lv.connect(self.VSYS_5V.lv)
        self.VDD_DRAM_0V9.connect(self.BUCK3.output)

        # VDD_3V3
        self.BUCK4.inductor.inductance.merge(F.Range.from_center_rel(1 * P.uH, 0.3))
        self.BUCK4.inductor.rated_current.merge(F.Range.lower_bound(3 * P.A))
        self.BUCK4.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C88211"}))
        self.BUCK4.capacitor.capacitance.merge(F.Range.from_center_rel(2 * P.nF, 0.3)) #TODO: update value once API is updated 22uF
        self.BUCK4.input.hv.connect(self.pmic.LX4)
        self.BUCK4.input.lv.connect(self.VSYS_5V.lv)
        self.VCC_3V3.connect(self.BUCK4.output)
        self.BUCK4.input.voltage.merge(self.VSYS_5V.voltage)

        # VDD_1V8
        self.BUCK5.inductor.inductance.merge(F.Range.from_center_rel(0.470 * P.uH, 0.3))
        self.BUCK5.inductor.rated_current.merge(F.Range.lower_bound(3 * P.A))
        self.BUCK5.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C97014"}))
        self.BUCK5.capacitor.capacitance.merge(F.Range.from_center_rel(2 * P.nF, 0.3)) #TODO: update value once API is updated 22uF
        self.BUCK5.input.hv.connect(self.pmic.LX5)
        self.BUCK5.input.lv.connect(self.VSYS_5V.lv)
        self.VDD_1V8.connect(self.BUCK5.output)
        self.BUCK5.input.voltage.merge(self.VSYS_5V.voltage)
        self.pmic.BUCK4FB.connect(self.BUCK5.output)

        # NVCC_DRAM_1V1
        self.BUCK6.inductor.inductance.merge(F.Range.from_center_rel(0.470 * P.uH, 0.3))
        self.BUCK6.inductor.rated_current.merge(F.Range.lower_bound(3 * P.A))
        self.BUCK6.inductor.add(F.has_descriptive_properties_defined({"LCSC": "C97014"}))
        self.BUCK6.capacitor.capacitance.merge(F.Range.from_center_rel(2 * P.nF, 0.3)) #TODO: update value once API is updated 22uF
        self.BUCK6.input.hv.connect(self.pmic.LX6)
        self.BUCK6.input.lv.connect(self.VSYS_5V.lv)
        self.NVCC_DRAM_1V1.connect(self.BUCK6.output)
        self.BUCK6.input.voltage.merge(self.VSYS_5V.voltage)
        self.pmic.BUCK6FB.connect(self.BUCK6.output)

        # Connect SWIN and SWOUT
        self.VCC_3V3.hv.connect(self.pmic.SWIN)
        SW_IN_RES = F.Resistor()
        SW_IN_RES.resistance.merge(F.Range.upper_bound(1 * P.ohm))
        self.VCC_3V3.hv.connect_via(SW_IN_RES, self.pmic.SWOUT)

        # Decouple PMIC SWIN
        SWIN_CAP = F.Capacitor()
        SWIN_CAP.capacitance.merge(F.Range.from_center_rel(1 * P.nF, 0.1)) #TODO: update value once API is updated 4.7uF
        SWIN_CAP.add(F.has_footprint_requirement_defined([("0402", 1)]))
        self.pmic.SWIN.connect_via(SWIN_CAP, self.VSYS_5V.lv)

        # Decouple PMIC SWOUT
        SWOUT_CAP = F.Capacitor()
        SWOUT_CAP.capacitance.merge(F.Range.from_center_rel(1 * P.nF, 0.1)) #TODO: update value once API is updated 4.7uF
        SWOUT_CAP.add(F.has_footprint_requirement_defined([("0402", 1)]))
        self.pmic.SWOUT.connect_via(SWOUT_CAP, self.SWOUT.lv)
        self.SWOUT.hv.connect(self.pmic.SWOUT)
        self.SWOUT.lv.connect(self.VSYS_5V.lv)


        # Reset signals





