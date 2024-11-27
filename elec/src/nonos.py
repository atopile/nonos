

# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

# Components
from .processor.imx8 import NXP_Semicon_MIMX8MM6CVTKZAA
from .processor.pmic import PCA9450AAHNY
from .processor.RAM import SK_HYNIX_H9HCNNNBKUMLXR_NEE
from .processor.eMMC import Samsung_KLMBG2JETD_B041

logger = logging.getLogger(__name__)

class App(Module):
    """
    Open-source smart speaker
    """
    IMX8: NXP_Semicon_MIMX8MM6CVTKZAA
    PMIC: PCA9450AAHNY
    RAM: SK_HYNIX_H9HCNNNBKUMLXR_NEE
    eMMC: Samsung_KLMBG2JETD_B041


    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------
        # ------------------------------------
        #
        #  ____  __  __ ___ ____ 
        # |  _ \|  \/  |_ _/ ___|
        # | |_) | |\/| || | |    
        # |  __/| |  | || | |___ 
        # |_|   |_|  |_|___\____|
        #
        # ------------------------------------
        # Power rails
        self.PMIC.NVCC_SNVS_1V8.connect(self.IMX8.NVCC_SNVS_1V8)
        self.PMIC.VDD_SNVS_0V8.connect(self.IMX8.VDD_SNVS_0V8)
        self.PMIC.VDD_SOC_0V8.connect(self.IMX8.VDD_SOC_0V8)
        self.PMIC.VDD_DRAM_0V9.connect(self.IMX8.VDD_DRAM_0V9)
        self.PMIC.VDDA_1V8.connect(self.IMX8.VDDA_1V8)
        self.PMIC.VDD_1V8.connect(self.IMX8.VDD_1V8)
        self.PMIC.NVCC_DRAM_1V1.connect(self.IMX8.NVCC_DRAM_1V1)
        self.PMIC.VCC_3V3.connect(self.IMX8.VDD_3V3)
        self.PMIC.VDD_PHY_1V2.connect(self.IMX8.VDD_PHY_1V2)
        self.PMIC.NVCC_SD2.connect(self.IMX8.NVCC_SD2)
        #TODO: Determine correct connection for NVCC_ENET

        # Reset / Boot
        # self.PMIC.ONOFF.connect(self.IMX8.ONOFF) #TODO: Power button
        self.PMIC.POR_B.connect(self.IMX8.POR_B)
        self.PMIC.RTC_RESET_B.connect(self.IMX8.RTC_RESET_B)
        self.PMIC.PMIC_ON_REQ.connect(self.IMX8.PMIC_ON_REQ)
        self.PMIC.PMIC_STBY_REQ.connect(self.IMX8.PMIC_STBY_REQ)
        self.PMIC.CLK_32K_OUT.connect(self.IMX8.XTALI_32K)

        # I2C
        self.PMIC.I2C.connect(self.IMX8.I2C1)

        # ------------------------------------
        #
        #  ____      _    __  __ 
        # |  _ \    / \  |  \/  |
        # | |_) |  / _ \ | |\/| |
        # |  _ <  / ___ \| |  | |
        # |_| \_\/_/   \_\_|  |_|
        #
        # ------------------------------------
        # Power rails
        self.RAM.VDD_1V8.connect(self.IMX8.VDD_1V8)
        self.RAM.NVCC_DRAM_1V1.connect(self.IMX8.NVCC_DRAM_1V1)
        self.RAM.DRAM_ODT_CA_A.connect(self.IMX8.NVCC_DRAM_1V1)
        self.RAM.DRAM_ODT_CA_B.connect(self.IMX8.NVCC_DRAM_1V1)

        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_DATA_A, self.IMX8.DRAM_DATA_A)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_DATA_A_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_DATA_B, self.IMX8.DRAM_DATA_B)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_DATA_B_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_DMI_A, self.IMX8.DRAM_DMI_A)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_DMI_A_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_DMI_B, self.IMX8.DRAM_DMI_B)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_DMI_B_{i}").part_of.connect(imx.signal)

        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_SDQS_A, self.IMX8.DRAM_SDQS_A)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_SDQS_A_{i}_N").part_of.connect(imx.n.signal)
            F.Net.with_name(f"DRAM_SDQS_A_{i}_P").part_of.connect(imx.p.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_SDQS_B, self.IMX8.DRAM_SDQS_B)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_SDQS_B_{i}_N").part_of.connect(imx.n.signal)
            F.Net.with_name(f"DRAM_SDQS_B_{i}_P").part_of.connect(imx.p.signal)


        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_CA_A, self.IMX8.DRAM_CA_A)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_CA_A_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_CA_B, self.IMX8.DRAM_CA_B)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_CA_B_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_CKE_A, self.IMX8.DRAM_CKE_A)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_CKE_A_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_CKE_B, self.IMX8.DRAM_CKE_B)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_CKE_B_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_nCS_A, self.IMX8.DRAM_nCS_A)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_nCS_A_{i}").part_of.connect(imx.signal)
        
        for i, (ram, imx) in enumerate(zip(self.RAM.DRAM_nCS_B, self.IMX8.DRAM_nCS_B)):
            ram.connect(imx)
            F.Net.with_name(f"DRAM_nCS_B_{i}").part_of.connect(imx.signal)

        self.RAM.DRAM_CK_A.connect(self.IMX8.DRAM_CK_A)
        self.RAM.DRAM_CK_B.connect(self.IMX8.DRAM_CK_B)

        F.Net.with_name("DRAM_CK_A_N").part_of.connect(self.IMX8.DRAM_CK_A.n.signal)
        F.Net.with_name("DRAM_CK_A_P").part_of.connect(self.IMX8.DRAM_CK_A.p.signal)
        F.Net.with_name("DRAM_CK_B_N").part_of.connect(self.IMX8.DRAM_CK_B.n.signal)
        F.Net.with_name("DRAM_CK_B_P").part_of.connect(self.IMX8.DRAM_CK_B.p.signal)
        
        self.RAM.DRAM_nRESET.connect(self.IMX8.DRAM_nRESET)
        F.Net.with_name("DRAM_nRESET").part_of.connect(self.IMX8.DRAM_nRESET.signal)



        # Net naming

        # ------------------------------------
        #          parametrization
        # ------------------------------------