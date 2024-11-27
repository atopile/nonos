

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
from .processor.ram import SK_HYNIX_H9HCNNNBKUMLXR_NEE

logger = logging.getLogger(__name__)

class App(Module):
    """
    Open-source smart speaker
    """
    IMX8: NXP_Semicon_MIMX8MM6CVTKZAA
    PMIC: PCA9450AAHNY


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
        #          parametrization
        # ------------------------------------