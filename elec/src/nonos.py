

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

    # DRAM_DATA_A = times(16, F.ElectricLogic)  # Data
    # DRAM_DATA_B = times(16, F.ElectricLogic)  # Data
    # DRAM_DMI_A = times(2, F.ElectricLogic)  # Data mask (bit inversion)
    # DRAM_DMI_B = times(2, F.ElectricLogic)  # Data mask (bit inversion)
    # DRAM_SDQS_A = times(2, F.DifferentialPair)  # Data strobe (differential)
    # DRAM_SDQS_B = times(2, F.DifferentialPair)  # Data strobe (differential)
    # DRAM_CA_A = times(6, F.ElectricLogic)  # Command address
    # DRAM_CA_B = times(6, F.ElectricLogic)  # Command address
    # DRAM_CK_A: F.DifferentialPair  # Clock
    # DRAM_CK_B: F.DifferentialPair  # Clock
    # DRAM_CKE_A = times(2, F.ElectricLogic)  # Clock enable
    # DRAM_CKE_B = times(2, F.ElectricLogic)  # Clock enable
    # DRAM_nCS_A = times(2, F.ElectricLogic)  # Chip select
    # DRAM_nCS_B = times(2, F.ElectricLogic)  # Chip select
    # DRAM_nRESET: F.ElectricLogic  # Reset

        # ------------------------------------
        #          parametrization
        # ------------------------------------