# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)

# TODO: What is NVCC_ENET? note on schematic says 'Supply from base board'


class _NXP_Semicon_MIMX8MM6CVTKZAA(Module):
    """
    TODO: Docstring describing your module

    256KB 1.6GHz FCPBGA-486
    Microcontrollers (MCU/MPU/SOC) ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    VDD_PCI_1P8: F.Electrical
    DRAM_AC08: F.Electrical
    SAI1_RXC: F.Electrical
    VDD_USB_0P8: F.Electrical
    DRAM_DQ20: F.Electrical
    DRAM_AC25: F.Electrical
    ENET_MDC: F.Electrical
    CLKOUT2: F.Electrical
    VDD_ANA_0P8: F.Electrical
    RTC_XTALI: F.Electrical
    DRAM_DQ06: F.Electrical
    DRAM_DQS2_N: F.Electrical
    DRAM_DM1: F.Electrical
    NAND_ALE: F.Electrical
    MIPI_DSI_D3_N: F.Electrical
    VDD_MIPI_0P9: F.Electrical
    NVCC_SAI5: F.Electrical
    DRAM_AC19: F.Electrical
    SD1_CLK: F.Electrical
    MIPI_DSI_D1_N: F.Electrical
    SAI1_TXD7: F.Electrical
    ENET_TD3: F.Electrical
    MIPI_CSI_D3_N: F.Electrical
    ENET_TD1: F.Electrical
    ENET_RX_CTL: F.Electrical
    UART3_RXD: F.Electrical
    DRAM_DQ08: F.Electrical
    NAND_WE_B: F.Electrical
    GPIO1_IO14: F.Electrical
    DRAM_DQ04: F.Electrical
    NVCC_GPIO1: F.Electrical
    DRAM_AC234: F.Electrical
    UART4_TXD: F.Electrical
    GPIO1_IO01: F.Electrical
    MIPI_CSI_CLK_P: F.Electrical
    PCIE_CLK_N: F.Electrical
    SD1_DATA6: F.Electrical
    DRAM_RESET_N: F.Electrical
    USB2_TXRTUNE: F.Electrical
    GPIO1_IO08: F.Electrical
    DRAM_AC07: F.Electrical
    SAI5_RXD1: F.Electrical
    DRAM_AC13: F.Electrical
    VDD_VPU: F.Electrical
    DRAM_AC05: F.Electrical
    UART1_RXD: F.Electrical
    SAI3_TXD: F.Electrical
    JTAG_TRST_B: F.Electrical
    PCIE_RXN_N: F.Electrical
    SAI5_MCLK: F.Electrical
    GPIO1_IO15: F.Electrical
    DRAM_AC38: F.Electrical
    ECSPI1_SCLK: F.Electrical
    NAND_RE_B: F.Electrical
    SAI2_RXFS: F.Electrical
    DRAM_DQ24: F.Electrical
    SPDIF_RX: F.Electrical
    JTAG_TCK: F.Electrical
    DRAM_AC16: F.Electrical
    ECSPI2_SCLK: F.Electrical
    NVCC_ESCPI: F.Electrical
    ECSPI2_SS0: F.Electrical
    SAI1_TXFS: F.Electrical
    DRAM_DQ28: F.Electrical
    DRAM_DQ23: F.Electrical
    SAI3_MCLK: F.Electrical
    MIPI_DSI_D1_P: F.Electrical
    MIPI_DSI_D3_P: F.Electrical
    DRAM_ALERT_N: F.Electrical
    NAND_CE2_B: F.Electrical
    MIPI_CSI_D3_P: F.Electrical
    DRAM_DQ25: F.Electrical
    I2C1_SDA: F.Electrical
    DRAM_DQ15: F.Electrical
    NVCC_NAND: F.Electrical
    DRAM_DQ13: F.Electrical
    MIPI_DSI_CLK_N: F.Electrical
    USB1_DP: F.Electrical
    DRAM_AC36: F.Electrical
    NAND_DATA01: F.Electrical
    PCIE_PXN_P: F.Electrical
    DRAM_DQ30: F.Electrical
    SAI1_RXD0: F.Electrical
    SAI2_RXC: F.Electrical
    DRAM_DQ12: F.Electrical
    ENET_RD0: F.Electrical
    NVCC_SAI2: F.Electrical
    VDD_USB_3P3: F.Electrical
    GPIO1_IO06: F.Electrical
    UART3_TXD: F.Electrical
    TESENSOR_RES_EXT: F.Electrical
    DRAM_DQS2_P: F.Electrical
    SAI2_RXD0: F.Electrical
    VDD_SNVS_0P8: F.Electrical
    VDD_MIPI_1P8: F.Electrical
    DRAM_ZN: F.Electrical
    MIPI_CSI_D0_P: F.Electrical
    DRAM_DQ02: F.Electrical
    SD2_CMD: F.Electrical
    VDD_ARM_PLL_1P8: F.Electrical
    JTAG_MOD: F.Electrical
    VDD_ARM_PLL_0P8: F.Electrical
    DRAM_AC04: F.Electrical
    DRAM_AC30: F.Electrical
    SAI1_TXD6: F.Electrical
    GPIO1_IO02: F.Electrical
    DRAM_DQ26: F.Electrical
    DRAM_DQS1_P: F.Electrical
    SAI3_RXFS: F.Electrical
    NC_J18: F.Electrical
    DRAM_AC32: F.Electrical
    SD1_DATA2: F.Electrical
    GPIO1_IO11: F.Electrical
    DRAM_AC17: F.Electrical
    PMIC_STBY_REQ: F.Electrical
    SAI1_TXD1: F.Electrical
    DRAM_AC09: F.Electrical
    I2C3_SCL: F.Electrical
    TSENSOR_TEST_OUT: F.Electrical
    SAI1_RXD1: F.Electrical
    MIPI_CSI_D2_P: F.Electrical
    MIPI_DSI_D0_N: F.Electrical
    DRAM_AC03: F.Electrical
    ENET_RD2: F.Electrical
    JTAG_TMS: F.Electrical
    SD1_DATA0: F.Electrical
    VDD_PCI_0P8: F.Electrical
    SD1_STROBE: F.Electrical
    USB1_VBUS: F.Electrical
    SD1_DATA4: F.Electrical
    SD2_DATA1: F.Electrical
    ENET_TX_CTL: F.Electrical
    CLKIN1: F.Electrical
    USB2_ID: F.Electrical
    DRAM_AC10: F.Electrical
    DRAM_DQ31: F.Electrical
    ENET_TD0: F.Electrical
    SAI5_RXC: F.Electrical
    SAI1_TXD3: F.Electrical
    NAND_WP_B: F.Electrical
    USB1_TXRTUNE: F.Electrical
    PVCC1_1P8: F.Electrical
    SAI1_RXD5: F.Electrical
    PMIC_ON_REQ: F.Electrical
    ENET_RD1: F.Electrical
    SD2_DATA3: F.Electrical
    DRAM_DQ29: F.Electrical
    DRAM_AC27: F.Electrical
    NAND_DATA07: F.Electrical
    GPIO1_IO04: F.Electrical
    DRAM_DQ17: F.Electrical
    PCIE_CLK_P: F.Electrical
    NAND_CE1_B: F.Electrical
    SD1_DATA1: F.Electrical
    UART1_TXD: F.Electrical
    MIPI_CSI_D1_N: F.Electrical
    NVCC_SNVS_1P8: F.Electrical
    NVCC_SD1: F.Electrical
    ENET_MDIO: F.Electrical
    VDD_DRAM_PLL_1P8: F.Electrical
    SAI2_TXFS: F.Electrical
    DRAM_DM0: F.Electrical
    VDD_GPU: F.Electrical
    DRAM_DQ01: F.Electrical
    SAI5_RXD2: F.Electrical
    MIPI_CSI_D2_N: F.Electrical
    JTAG_TDO: F.Electrical
    ENENT_RD3: F.Electrical
    NAND_CE0_B: F.Electrical
    DRAM_DQ27: F.Electrical
    NVCC_I2C: F.Electrical
    VDD_DRAM_PLL_0P8: F.Electrical
    DRAM_DQS3_N: F.Electrical
    SAI1_RXD7: F.Electrical
    GPIO1_IO00: F.Electrical
    DRAM_DQ19: F.Electrical
    NAND_DQS: F.Electrical
    CLKOUT1: F.Electrical
    NAND_DATA06: F.Electrical
    MIPI_DSI_D2_N: F.Electrical
    DRAM_DQS0_N: F.Electrical
    SD1_DATA5: F.Electrical
    UART4_RXD: F.Electrical
    SAI1_TXD2: F.Electrical
    DRAM_DQS1_N: F.Electrical
    SAI1_TXD0: F.Electrical
    DRAM_VREF: F.Electrical
    DRAM_DQ07: F.Electrical
    NAND_DATA02: F.Electrical
    MIPI_DSI_CLK_P: F.Electrical
    NAND_CE3_B: F.Electrical
    NAND_DATA04: F.Electrical
    ECSPI2_MISO: F.Electrical
    SD2_DATA0: F.Electrical
    VDD_MIPI_1P2: F.Electrical
    VDD_SOC: F.Electrical
    RTC_XTALO: F.Electrical
    SAI1_RXD4: F.Electrical
    I2C2_SCL: F.Electrical
    CLKIN2: F.Electrical
    DRAM_AC11: F.Electrical
    UART2_RXD: F.Electrical
    DRAM_DQ10: F.Electrical
    PCIE_TXN_P: F.Electrical
    SAI2_TXC: F.Electrical
    VDD_DRAM: F.Electrical
    NVCC_CLK: F.Electrical
    I2C3_SDA: F.Electrical
    ENET_TXC: F.Electrical
    DRAM_AC35: F.Electrical
    SD2_CD_B: F.Electrical
    ENET_TD2: F.Electrical
    MIPI_CSI_CLK_N: F.Electrical
    DRAM_DQ03: F.Electrical
    NVCC_JTAG: F.Electrical
    DRAM_AC23: F.Electrical
    DRAM_AC24: F.Electrical
    ECSPI1_SS0: F.Electrical
    UART2_TXD: F.Electrical
    NVCC_ENET: F.Electrical
    BOOT_MODE1: F.Electrical
    NVCC_SAI1: F.Electrical
    DRAM_DQ00: F.Electrical
    PCIE_RESREF: F.Electrical
    GPIO1_IO12: F.Electrical
    DRAM_AC00: F.Electrical
    SAI1_TXD4: F.Electrical
    GPIO1_IO09: F.Electrical
    DRAM_AC20: F.Electrical
    PVCC0_1P8: F.Electrical
    MIPI_DSI_D0_P: F.Electrical
    DRAM_AC14: F.Electrical
    DRAM_AC33: F.Electrical
    DRAM_DQ21: F.Electrical
    TEST_MODE: F.Electrical
    DRAM_DQ16: F.Electrical
    SAI5_RXFS: F.Electrical
    GPIO1_IO07: F.Electrical
    VDD_24M_XTAL_1P8: F.Electrical
    MIPI_DSI_D2_P: F.Electrical
    NVCC_DRAM: F.Electrical
    SAI1_RXD2: F.Electrical
    SAI3_RXC: F.Electrical
    SAI5_RXD3: F.Electrical
    VDD_ANA1_1P8: F.Electrical
    SD2_WP: F.Electrical
    GPIO1_IO05: F.Electrical
    NAND_DATA05: F.Electrical
    USB2_VBUS: F.Electrical
    VDD_USB_1P8: F.Electrical
    SAI2_TXD0: F.Electrical
    NAND_CLE: F.Electrical
    DRAM_AC31: F.Electrical
    MIPI_CSI_D0_N: F.Electrical
    SPDIF_TX: F.Electrical
    DRAM_AC15: F.Electrical
    I2C4_SCL: F.Electrical
    VSS: F.Electrical
    SAI3_RXD: F.Electrical
    SD2_DATA2: F.Electrical
    POR_B: F.Electrical
    P24M_XTALO: F.Electrical
    P24M_XTALI: F.Electrical
    SD2_CLK: F.Electrical
    DRAM_AC29: F.Electrical
    NAND_READY_B: F.Electrical
    DRAM_DQS0_P: F.Electrical
    ONOFF: F.Electrical
    DRAM_DQ22: F.Electrical
    RTC_RESET_B: F.Electrical
    NVCC_SAI3: F.Electrical
    VDD_ANA0_1P8: F.Electrical
    SAI1_TXD5: F.Electrical
    USB1_ID: F.Electrical
    DRAM_DQ09: F.Electrical
    SD1_CMD: F.Electrical
    SD1_DATA7: F.Electrical
    NAND_DATA00: F.Electrical
    PCIE_TXN_N: F.Electrical
    SAI1_RXD6: F.Electrical
    DRAM_DQS3_P: F.Electrical
    DRAM_AC28: F.Electrical
    ECSPI2_MOSI: F.Electrical
    GPIO1_IO03: F.Electrical
    MIPI_VREG_CAP: F.Electrical
    SAI1_TXC: F.Electrical
    DRAM_AC06: F.Electrical
    DRAM_AC12: F.Electrical
    PVCC2_1P8: F.Electrical
    SPDIF_EXT_CLK: F.Electrical
    DRAM_AC02: F.Electrical
    SAI1_RXFS: F.Electrical
    ENET_RXC: F.Electrical
    ECSPI1_MISO: F.Electrical
    DRAM_AC01: F.Electrical
    DRAM_AC21: F.Electrical
    NVCC_UART: F.Electrical
    USB2_DP: F.Electrical
    DRAM_DQ11: F.Electrical
    BOOT_MODE0: F.Electrical
    DRAM_AC22: F.Electrical
    SAI1_MCLK: F.Electrical
    USB1_DN: F.Electrical
    DRAM_DQ05: F.Electrical
    SAI2_MCLK: F.Electrical
    VDD_ARM: F.Electrical
    GPIO1_IO13: F.Electrical
    SAI3_TXC: F.Electrical
    SAI5_RXD0: F.Electrical
    SAI1_RXD3: F.Electrical
    DRAM_DQ18: F.Electrical
    DRAM_DM3: F.Electrical
    DRAM_DQ14: F.Electrical
    NVCC_SD2: F.Electrical
    ECSPI1_MOSI: F.Electrical
    SD2_RESET_B: F.Electrical
    DRAM_DM2: F.Electrical
    SAI3_TXFS: F.Electrical
    DRAM_AC37: F.Electrical
    I2C4_SDA: F.Electrical
    MIPI_CSI_D1_P: F.Electrical
    SD1_RESET_B: F.Electrical
    JTAG_TDI: F.Electrical
    GPIO1_IO10: F.Electrical
    SD1_DATA3: F.Electrical
    NAND_DATA03: F.Electrical
    DRAM_AC26: F.Electrical
    I2C1_SCL: F.Electrical
    I2C2_SDA: F.Electrical
    USB2_DN: F.Electrical

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C1522487"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "NXP Semicon",
            DescriptiveProperties.partno: "MIMX8MM6CVTKZAA",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2405281456_NXP-Semicon-MIMX8MM6CVTKZAA_C1522487.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "A1": self.VSS,
                "A10": self.MIPI_DSI_D1_N,
                "A11": self.MIPI_DSI_CLK_N,
                "A12": self.MIPI_DSI_D2_N,
                "A13": self.MIPI_DSI_D3_N,
                "A14": self.MIPI_CSI_D0_N,
                "A15": self.MIPI_CSI_D1_N,
                "A16": self.MIPI_CSI_CLK_N,
                "A17": self.MIPI_CSI_D2_N,
                "A18": self.MIPI_CSI_D3_N,
                "A19": self.PCIE_RXN_N,
                "A2": self.DRAM_DQS0_P,
                "A20": self.PCIE_TXN_N,
                "A21": self.PCIE_CLK_N,
                "A22": self.USB1_DN,
                "A23": self.USB2_DN,
                "A24": self.PMIC_ON_REQ,
                "A25": self.ONOFF,
                "A26": self.RTC_XTALI,
                "A27": self.VSS,
                "A3": self.DRAM_DQ06,
                "A4": self.DRAM_DM0,
                "A5": self.DRAM_DQ00,
                "A6": self.ECSPI2_SS0,
                "A7": self.ECSPI1_MISO,
                "A8": self.ECSPI2_MISO,
                "A9": self.MIPI_DSI_D0_N,
                "AA1": self.DRAM_DQS2_P,
                "AA10": self.VSS,
                "AA13": self.VSS,
                "AA14": self.VDD_ANA0_1P8,
                "AA15": self.VSS,
                "AA18": self.VSS,
                "AA19": self.VSS,
                "AA2": self.DRAM_DQ17,
                "AA21": self.VSS,
                "AA26": self.SD2_CD_B,
                "AA27": self.SD2_WP,
                "AA7": self.VSS,
                "AA9": self.VSS,
                "AB1": self.DRAM_DM2,
                "AB10": self.GPIO1_IO12,
                "AB13": self.PVCC0_1P8,
                "AB15": self.SAI5_RXFS,
                "AB18": self.SAI1_MCLK,
                "AB19": self.SAI1_TXFS,
                "AB2": self.DRAM_DQ16,
                "AB22": self.SAI2_RXC,
                "AB23": self.SD2_DATA0,
                "AB24": self.SD2_DATA1,
                "AB25": self.VSS,
                "AB26": self.SD2_RESET_B,
                "AB27": self.ENET_MDIO,
                "AB3": self.VSS,
                "AB4": self.DRAM_AC20,
                "AB5": self.DRAM_AC21,
                "AB6": self.DRAM_AC38,
                "AB9": self.GPIO1_IO15,
                "AC1": self.DRAM_DQ22,
                "AC10": self.GPIO1_IO11,
                "AC13": self.SAI5_RXD3,
                "AC14": self.SAI5_RXD1,
                "AC15": self.SAI5_RXC,
                "AC18": self.SAI1_TXC,
                "AC19": self.SAI2_RXFS,
                "AC2": self.DRAM_DQ23,
                "AC22": self.SAI2_TXD0,
                "AC24": self.SAI2_RXD0,
                "AC25": self.VSS,
                "AC26": self.ENENT_RD3,
                "AC27": self.ENET_MDC,
                "AC3": self.VSS,
                "AC4": self.DRAM_AC30,
                "AC6": self.SAI3_TXFS,
                "AC9": self.GPIO1_IO14,
                "AD1": self.DRAM_DQ27,
                "AD10": self.GPIO1_IO10,
                "AD13": self.SAI5_RXD2,
                "AD15": self.SAI5_MCLK,
                "AD18": self.SAI5_RXD0,
                "AD19": self.SAI2_MCLK,
                "AD2": self.DRAM_DQ26,
                "AD22": self.SAI2_TXC,
                "AD23": self.SAI2_TXFS,
                "AD26": self.ENET_RD2,
                "AD27": self.ENET_RD1,
                "AD5": self.DRAM_AC31,
                "AD6": self.SAI3_MCLK,
                "AD9": self.GPIO1_IO13,
                "AE1": self.DRAM_DQ28,
                "AE10": self.VSS,
                "AE13": self.VSS,
                "AE14": self.VSS,
                "AE15": self.VSS,
                "AE18": self.VSS,
                "AE19": self.VSS,
                "AE2": self.VSS,
                "AE22": self.VSS,
                "AE23": self.VSS,
                "AE26": self.ENET_RXC,
                "AE27": self.ENET_RD0,
                "AE5": self.VSS,
                "AE6": self.VSS,
                "AE9": self.VSS,
                "AF1": self.DRAM_DQ29,
                "AF10": self.GPIO1_IO09,
                "AF11": self.GPIO1_IO07,
                "AF12": self.GPIO1_IO05,
                "AF13": self.GPIO1_IO03,
                "AF14": self.GPIO1_IO01,
                "AF15": self.SAI1_RXD1,
                "AF16": self.SAI1_RXC,
                "AF17": self.SAI1_RXD3,
                "AF18": self.SAI1_RXD5,
                "AF19": self.SAI1_RXD7,
                "AF2": self.DRAM_DQS3_N,
                "AF20": self.SAI1_TXD1,
                "AF21": self.SAI1_TXD3,
                "AF22": self.SAI1_TXD5,
                "AF23": self.SAI1_TXD7,
                "AF24": self.ENET_TX_CTL,
                "AF25": self.ENET_TD3,
                "AF26": self.ENET_TD1,
                "AF27": self.ENET_RX_CTL,
                "AF3": self.VSS,
                "AF4": self.DRAM_DQ31,
                "AF5": self.DRAM_DQ25,
                "AF6": self.SAI3_TXD,
                "AF7": self.SAI3_RXD,
                "AF8": self.SPDIF_EXT_CLK,
                "AF9": self.SPDIF_TX,
                "AG1": self.VSS,
                "AG10": self.GPIO1_IO08,
                "AG11": self.GPIO1_IO06,
                "AG12": self.GPIO1_IO04,
                "AG13": self.GPIO1_IO02,
                "AG14": self.GPIO1_IO00,
                "AG15": self.SAI1_RXD0,
                "AG16": self.SAI1_RXFS,
                "AG17": self.SAI1_RXD2,
                "AG18": self.SAI1_RXD4,
                "AG19": self.SAI1_RXD6,
                "AG2": self.DRAM_DQS3_P,
                "AG20": self.SAI1_TXD0,
                "AG21": self.SAI1_TXD2,
                "AG22": self.SAI1_TXD4,
                "AG23": self.SAI1_TXD6,
                "AG24": self.ENET_TXC,
                "AG25": self.ENET_TD2,
                "AG26": self.ENET_TD0,
                "AG27": self.VSS,
                "AG3": self.DRAM_DQ30,
                "AG4": self.DRAM_DM3,
                "AG5": self.DRAM_DQ24,
                "AG6": self.SAI3_TXC,
                "AG7": self.SAI3_RXC,
                "AG8": self.SAI3_RXFS,
                "AG9": self.SPDIF_RX,
                "B1": self.DRAM_DQ05,
                "B10": self.MIPI_DSI_D1_P,
                "B11": self.MIPI_DSI_CLK_P,
                "B12": self.MIPI_DSI_D2_P,
                "B13": self.MIPI_DSI_D3_P,
                "B14": self.MIPI_CSI_D0_P,
                "B15": self.MIPI_CSI_D1_P,
                "B16": self.MIPI_CSI_CLK_P,
                "B17": self.MIPI_CSI_D2_P,
                "B18": self.MIPI_CSI_D3_P,
                "B19": self.PCIE_PXN_P,
                "B2": self.DRAM_DQS0_N,
                "B20": self.PCIE_TXN_P,
                "B21": self.PCIE_CLK_P,
                "B22": self.USB1_DP,
                "B23": self.USB2_DP,
                "B24": self.POR_B,
                "B25": self.RTC_XTALO,
                "B26": self.VSS,
                "B27": self.P24M_XTALI,
                "B3": self.VSS,
                "B4": self.DRAM_DQ07,
                "B5": self.DRAM_DQ01,
                "B6": self.ECSPI1_SS0,
                "B7": self.ECSPI1_MOSI,
                "B8": self.ECSPI2_MOSI,
                "B9": self.MIPI_DSI_D0_P,
                "C1": self.DRAM_DQ04,
                "C10": self.VSS,
                "C13": self.VSS,
                "C14": self.VSS,
                "C15": self.VSS,
                "C18": self.VSS,
                "C19": self.VSS,
                "C2": self.VSS,
                "C22": self.VSS,
                "C23": self.VSS,
                "C26": self.P24M_XTALO,
                "C27": self.JTAG_TRST_B,
                "C5": self.VSS,
                "C6": self.VSS,
                "C9": self.VSS,
                "D1": self.DRAM_DQ03,
                "D10": self.I2C2_SCL,
                "D13": self.I2C4_SCL,
                "D15": self.MIPI_VREG_CAP,
                "D18": self.UART3_TXD,
                "D19": self.PCIE_RESREF,
                "D2": self.DRAM_DQ02,
                "D22": self.USB1_ID,
                "D23": self.USB2_ID,
                "D26": self.TEST_MODE,
                "D27": self.JTAG_MOD,
                "D5": self.DRAM_AC11,
                "D6": self.ECSPI1_SCLK,
                "D9": self.I2C2_SDA,
                "E1": self.DRAM_DQ14,
                "E10": self.I2C3_SCL,
                "E13": self.I2C4_SDA,
                "E14": self.UART1_RXD,
                "E15": self.UART2_TXD,
                "E18": self.UART3_RXD,
                "E19": self.USB1_TXRTUNE,
                "E2": self.DRAM_DQ15,
                "E22": self.USB2_TXRTUNE,
                "E24": self.PMIC_STBY_REQ,
                "E25": self.VSS,
                "E26": self.JTAG_TDO,
                "E27": self.JTAG_TDI,
                "E3": self.VSS,
                "E4": self.DRAM_AC10,
                "E6": self.ECSPI2_SCLK,
                "E9": self.I2C1_SCL,
                "F1": self.DRAM_DM1,
                "F10": self.I2C3_SDA,
                "F13": self.UART1_TXD,
                "F15": self.UART2_RXD,
                "F18": self.UART4_TXD,
                "F19": self.UART4_RXD,
                "F2": self.DRAM_DQ08,
                "F22": self.USB1_VBUS,
                "F23": self.USB2_VBUS,
                "F24": self.RTC_RESET_B,
                "F25": self.VSS,
                "F26": self.JTAG_TCK,
                "F27": self.JTAG_TMS,
                "F3": self.VSS,
                "F4": self.DRAM_AC00,
                "F5": self.DRAM_AC01,
                "F6": self.DRAM_AC06,
                "F9": self.I2C1_SDA,
                "G1": self.DRAM_DQS1_P,
                "G10": self.VSS,
                "G13": self.VSS,
                "G14": self.VDD_PCI_1P8,
                "G15": self.VSS,
                "G18": self.VSS,
                "G19": self.VSS,
                "G2": self.DRAM_DQ09,
                "G21": self.VSS,
                "G26": self.BOOT_MODE0,
                "G27": self.BOOT_MODE1,
                "G7": self.VSS,
                "G9": self.VSS,
                "H1": self.DRAM_DQS1_N,
                "H10": self.NVCC_ESCPI,
                "H13": self.VDD_MIPI_1P8,
                "H15": self.VDD_USB_1P8,
                "H18": self.VSS,
                "H2": self.VSS,
                "H26": self.CLKOUT1,
                "H27": self.CLKIN1,
                "J1": self.DRAM_DQ10,
                "J10": self.VDD_DRAM,
                "J11": self.NVCC_I2C,
                "J12": self.NVCC_UART,
                "J13": self.PVCC2_1P8,
                "J14": self.VDD_MIPI_0P9,
                "J15": self.VDD_MIPI_1P2,
                "J16": self.VDD_PCI_0P8,
                "J17": self.VDD_USB_0P8,
                "J18": self.NC_J18,
                "J2": self.DRAM_DQ11,
                "J21": self.VSS,
                "J22": self.NVCC_SNVS_1P8,
                "J23": self.TSENSOR_TEST_OUT,
                "J24": self.TESENSOR_RES_EXT,
                "J25": self.VSS,
                "J26": self.CLKOUT2,
                "J27": self.CLKIN2,
                "J3": self.VSS,
                "J4": self.DRAM_AC03,
                "J5": self.DRAM_AC07,
                "J6": self.DRAM_AC08,
                "J7": self.VSS,
                "K1": self.DRAM_DQ13,
                "K12": self.VDD_VPU,
                "K13": self.VDD_VPU,
                "K15": self.VDD_SOC,
                "K16": self.VDD_SOC,
                "K19": self.VDD_USB_3P3,
                "K2": self.DRAM_DQ12,
                "K20": self.VSS,
                "K21": self.VSS,
                "K22": self.VDD_SNVS_0P8,
                "K23": self.NAND_DATA02,
                "K24": self.NAND_DATA01,
                "K25": self.VSS,
                "K26": self.NAND_DATA06,
                "K27": self.NAND_CLE,
                "K3": self.VSS,
                "K4": self.DRAM_AC02,
                "K5": self.DRAM_AC14,
                "K6": self.DRAM_AC09,
                "K7": self.VSS,
                "K8": self.NVCC_DRAM,
                "K9": self.NVCC_DRAM,
                "L1": self.DRAM_AC05,
                "L10": self.VDD_DRAM,
                "L11": self.VDD_VPU,
                "L12": self.VSS,
                "L13": self.VDD_VPU,
                "L15": self.VDD_SOC,
                "L16": self.VSS,
                "L17": self.VDD_ANA_0P8,
                "L18": self.VDD_SOC,
                "L19": self.NVCC_JTAG,
                "L2": self.DRAM_AC04,
                "L26": self.NAND_DATA05,
                "L27": self.NAND_CE3_B,
                "L9": self.NVCC_DRAM,
                "M1": self.DRAM_AC16,
                "M12": self.VSS,
                "M13": self.VDD_VPU,
                "M14": self.VDD_VPU,
                "M15": self.VDD_SOC,
                "M16": self.VSS,
                "M19": self.NVCC_CLK,
                "M2": self.DRAM_AC17,
                "M26": self.NAND_DATA04,
                "M27": self.NAND_CE2_B,
                "M9": self.NVCC_DRAM,
                "N1": self.DRAM_AC26,
                "N10": self.VDD_DRAM,
                "N11": self.VDD_VPU,
                "N12": self.VSS,
                "N13": self.VDD_SOC,
                "N15": self.VDD_SOC,
                "N16": self.VSS,
                "N17": self.VDD_ANA_0P8,
                "N18": self.VDD_SOC,
                "N19": self.VDD_24M_XTAL_1P8,
                "N2": self.DRAM_AC19,
                "N20": self.VDD_ANA1_1P8,
                "N21": self.VSS,
                "N22": self.NAND_ALE,
                "N23": self.NAND_DATA03,
                "N24": self.NAND_CE0_B,
                "N25": self.VSS,
                "N26": self.NAND_DATA07,
                "N27": self.NAND_RE_B,
                "N3": self.VSS,
                "N4": self.DRAM_AC12,
                "N5": self.DRAM_AC13,
                "N6": self.DRAM_AC15,
                "N7": self.VSS,
                "N8": self.NVCC_DRAM,
                "N9": self.NVCC_DRAM,
                "P1": self.DRAM_VREF,
                "P12": self.VDD_GPU,
                "P13": self.VSS,
                "P15": self.VSS,
                "P16": self.VDD_ARM_PLL_0P8,
                "P19": self.VDD_ANA1_1P8,
                "P2": self.DRAM_ZN,
                "P21": self.VSS,
                "P23": self.NAND_DATA00,
                "P25": self.VSS,
                "P26": self.NAND_READY_B,
                "P27": self.NAND_CE1_B,
                "P3": self.VSS,
                "P5": self.VDD_DRAM_PLL_1P8,
                "P7": self.NVCC_DRAM,
                "P9": self.VDD_DRAM_PLL_0P8,
                "R1": self.DRAM_RESET_N,
                "R10": self.VDD_DRAM,
                "R11": self.VDD_GPU,
                "R12": self.VSS,
                "R13": self.VDD_ARM,
                "R15": self.VDD_ARM,
                "R16": self.VSS,
                "R17": self.VDD_SOC,
                "R18": self.VDD_SOC,
                "R19": self.VDD_ARM_PLL_1P8,
                "R2": self.DRAM_ALERT_N,
                "R20": self.VSS,
                "R21": self.VSS,
                "R22": self.NAND_DQS,
                "R23": self.SD1_RESET_B,
                "R24": self.SD1_STROBE,
                "R25": self.VSS,
                "R26": self.NAND_WE_B,
                "R27": self.NAND_WP_B,
                "R3": self.VSS,
                "R4": self.DRAM_AC32,
                "R5": self.DRAM_AC33,
                "R6": self.DRAM_AC27,
                "R7": self.VSS,
                "R8": self.NVCC_DRAM,
                "R9": self.NVCC_DRAM,
                "T1": self.DRAM_AC234,
                "T12": self.VSS,
                "T13": self.VDD_ARM,
                "T14": self.VDD_ARM,
                "T15": self.VDD_ARM,
                "T16": self.VSS,
                "T19": self.PVCC1_1P8,
                "T2": self.DRAM_AC35,
                "T26": self.SD1_DATA3,
                "T27": self.SD1_DATA2,
                "T9": self.NVCC_DRAM,
                "U1": self.DRAM_AC25,
                "U10": self.VDD_DRAM,
                "U11": self.VDD_GPU,
                "U12": self.VSS,
                "U13": self.VDD_ARM,
                "U15": self.VDD_ARM,
                "U16": self.VSS,
                "U17": self.VDD_SOC,
                "U18": self.VDD_SOC,
                "U19": self.NVCC_NAND,
                "U2": self.DRAM_AC24,
                "U26": self.SD1_DATA5,
                "U27": self.SD1_DATA4,
                "U9": self.NVCC_DRAM,
                "V1": self.DRAM_DQ21,
                "V12": self.VDD_GPU,
                "V13": self.VDD_ARM,
                "V15": self.VDD_ARM,
                "V16": self.VDD_ARM,
                "V19": self.NVCC_SAI2,
                "V2": self.DRAM_DQ20,
                "V20": self.NVCC_SD1,
                "V21": self.VSS,
                "V22": self.NVCC_SD2,
                "V23": self.SD2_DATA3,
                "V24": self.SD2_DATA2,
                "V25": self.VSS,
                "V26": self.SD1_CLK,
                "V27": self.SD1_CMD,
                "V3": self.VSS,
                "V4": self.DRAM_AC23,
                "V5": self.DRAM_AC36,
                "V6": self.DRAM_AC29,
                "V7": self.VSS,
                "V8": self.NVCC_DRAM,
                "V9": self.NVCC_DRAM,
                "W1": self.DRAM_DQ18,
                "W10": self.VDD_DRAM,
                "W11": self.VDD_GPU,
                "W12": self.NVCC_GPIO1,
                "W13": self.VDD_ARM,
                "W14": self.VDD_ARM,
                "W15": self.VDD_ARM,
                "W16": self.VDD_ARM,
                "W17": self.NVCC_SAI5,
                "W18": self.NVCC_SAI1,
                "W2": self.DRAM_DQ19,
                "W21": self.VSS,
                "W22": self.NVCC_ENET,
                "W23": self.SD2_CLK,
                "W24": self.SD2_CMD,
                "W25": self.VSS,
                "W26": self.SD1_DATA7,
                "W27": self.SD1_DATA6,
                "W3": self.VSS,
                "W4": self.DRAM_AC22,
                "W5": self.DRAM_AC37,
                "W6": self.DRAM_AC28,
                "W7": self.VSS,
                "Y1": self.DRAM_DQS2_N,
                "Y10": self.NVCC_SAI3,
                "Y13": self.VSS,
                "Y15": self.VDD_ANA0_1P8,
                "Y18": self.VSS,
                "Y2": self.VSS,
                "Y26": self.SD1_DATA1,
                "Y27": self.SD1_DATA0,
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


class NXP_Semicon_MIMX8MM6CVTKZAA(Module):
    """
    Wrapper for the NXP i.MX8M Mini module
    """

    imx8: _NXP_Semicon_MIMX8MM6CVTKZAA

    # External interfaces

    # Power rails
    NVCC_SNVS_1V8: F.ElectricPower
    VDD_SNVS_0V8: F.ElectricPower
    VDD_SOC_0V8: F.ElectricPower
    VDD_DRAM_0V9: F.ElectricPower
    VDD_PHY_0V9: F.ElectricPower
    VDD_ARM_0V9: F.ElectricPower
    VDDA_1V8: F.ElectricPower
    VDD_1V8: F.ElectricPower
    NVCC_DRAM_1V1: F.ElectricPower
    VDD_3V3: F.ElectricPower
    VDD_PHY_1V2: F.ElectricPower
    NVCC_SD2: F.ElectricPower
    NVCC_ENET: F.ElectricPower
    GND: F.Net

    # Passive components
    MIPI_VREG_CAP: F.Capacitor

    def __preinit__(self):
        # ------------------------------------
        #
        #  ____
        # |  _ \ _____      _____ _ __
        # | |_) / _ \ \ /\ / / _ \ '__|
        # |  __/ (_) \ V  V /  __/ |
        # |_|   \___/ \_/\_/ \___|_|
        #
        # ------------------------------------
        # Set input voltages
        self.VDD_SNVS_0V8.voltage.merge(0.8 * P.V)
        self.VDD_SOC_0V8.voltage.merge(0.8 * P.V)
        self.VDD_DRAM_0V9.voltage.merge(0.9 * P.V)
        self.VDD_PHY_0V9.voltage.merge(0.9 * P.V)
        self.VDD_ARM_0V9.voltage.merge(0.9 * P.V)
        self.VDDA_1V8.voltage.merge(1.8 * P.V)
        self.VDD_1V8.voltage.merge(1.8 * P.V)
        self.NVCC_SNVS_1V8.voltage.merge(1.8 * P.V)
        self.NVCC_DRAM_1V1.voltage.merge(1.1 * P.V)
        self.VDD_3V3.voltage.merge(3.3 * P.V)
        self.VDD_PHY_1V2.voltage.merge(1.2 * P.V)
        self.NVCC_SD2.voltage.merge(3.3 * P.V)

        # Connections
        self.NVCC_SNVS_1V8.hv.connect(self.imx8.NVCC_SNVS_1P8)
        self.VDD_SNVS_0V8.hv.connect(self.imx8.VDD_SNVS_0P8)
        self.VDDA_1V8.hv.connect(self.imx8.VDD_24M_XTAL_1P8, self.imx8.VDD_ARM_PLL_1P8)
        self.VDD_ARM_0V9.hv.connect(self.imx8.VDD_ARM)
        self.VDD_SOC_0V8.hv.connect(self.imx8.VDD_SOC)
        self.VDD_DRAM_0V9.hv.connect(
            self.imx8.VDD_VPU,
            self.imx8.VDD_GPU,
            self.imx8.VDD_DRAM,
            self.imx8.VDD_DRAM_PLL_1P8,
        )
        self.NVCC_DRAM_1V1.hv.connect(self.imx8.NVCC_DRAM)
        self.VDD_1V8.hv.connect(
            self.imx8.NVCC_JTAG,
            self.imx8.NVCC_NAND,
            self.imx8.NVCC_SAI2,
            self.imx8.NVCC_GPIO1,
            self.imx8.NVCC_I2C,
            self.imx8.NVCC_UART,
            self.imx8.NVCC_SD1,
            self.imx8.NVCC_CLK,
            self.imx8.PVCC0_1P8,
            self.imx8.PVCC1_1P8,
            self.imx8.PVCC2_1P8,
            self.imx8.VDD_ARM_PLL_1P8,
            self.imx8.VDD_ANA0_1P8,
            self.imx8.VDD_ANA1_1P8,
            self.imx8.VDD_USB_1P8,
            self.imx8.VDD_PCI_1P8,
            self.imx8.VDD_MIPI_1P8,
        )
        self.VDD_3V3.hv.connect(
            self.imx8.NVCC_SAI1,
            self.imx8.NVCC_SAI3,
            self.imx8.NVCC_SAI5,
            self.imx8.NVCC_ESCPI,
            self.imx8.VDD_USB_3P3
        )
        self.NVCC_ENET.hv.connect(self.imx8.NVCC_ENET)
        self.NVCC_ENET.connect(self.VDD_1V8) #TODO: Confirm
        self.VDD_SOC_0V8.hv.connect(
            self.imx8.VDD_ARM_PLL_0P8,
            self.imx8.VDD_ANA_0P8,
            self.imx8.VDD_USB_0P8,
            self.imx8.VDD_PCI_0P8,
        )

        self.VDD_PHY_1V2.hv.connect(self.imx8.VDD_MIPI_1P2)
        self.VDD_PHY_0V9.hv.connect(self.imx8.VDD_MIPI_0P9)

        # GND
        # self.GND.with_name("GND")

        self.imx8.VSS.connect(
            self.imx8.VSS,
            self.VDD_SNVS_0V8.lv,
            self.VDD_SOC_0V8.lv,
            self.VDD_DRAM_0V9.lv,
            self.VDDA_1V8.lv,
            self.VDD_1V8.lv,
            self.NVCC_SNVS_1V8.lv,
            self.NVCC_DRAM_1V1.lv,
            self.VDD_3V3.lv,
            self.VDD_PHY_1V2.lv,
            self.VDD_PHY_0V9.lv,
            self.NVCC_SD2.lv,
            self.NVCC_ENET.lv,
            self.VDD_ARM_0V9.lv,
        )

        # Decoupling capacitors

        # NVCC_SNVS_1V8
        NVCC_SNVS_1V8_CAP = self.NVCC_SNVS_1V8.decoupled.decouple()
        NVCC_SNVS_1V8_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        NVCC_SNVS_1V8_CAP.capacitance.merge(F.Range.from_center_rel(1 * P.uF, 0.2))

        # # VDD_SNVS_0V8
        VDD_SNVS_0V8_CAP = self.VDD_SNVS_0V8.decoupled.decouple()
        VDD_SNVS_0V8_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        VDD_SNVS_0V8_CAP.capacitance.merge(F.Range.from_center_rel(220 * P.nF, 0.2))

        # VDDA_1V8
        VDDA_1V8_CAP_FOOTPRINTS = [
            ("0201", 2),
            ("0201", 2),
        ]
        VDDA_1V8_CAP_VALUES = [
            220 * P.nF,
            1 * P.uF,
        ]

        VDDA_1V8_CAPS = (
            self.VDDA_1V8.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDDA_1V8_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDDA_1V8_CAPS, VDDA_1V8_CAP_FOOTPRINTS, VDDA_1V8_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # VDD_ARM_0V9
        VDD_ARM_0V9_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
        ]
        VDD_ARM_0V9_CAP_VALUES = [
            10 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
        ]

        VDD_ARM_0V9_CAPS = (
            self.VDD_ARM_0V9.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDD_ARM_0V9_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDD_ARM_0V9_CAPS, VDD_ARM_0V9_CAP_FOOTPRINTS, VDD_ARM_0V9_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # VDD_SOC_0V8
        VDD_SOC_0V8_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0402", 2),
            ("0201", 2),
        ]
        VDD_SOC_0V8_CAP_VALUES = [
            10 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            4.7 * P.uF,
            220 * P.nF,
        ]

        VDD_SOC_0V8_CAPS = (
            self.VDD_SOC_0V8.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDD_SOC_0V8_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDD_SOC_0V8_CAPS, VDD_SOC_0V8_CAP_FOOTPRINTS, VDD_SOC_0V8_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # VDD_DRAM_0V9
        VDD_DRAM_0V9_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0402", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
        ]
        VDD_DRAM_0V9_CAP_VALUES = [
            10 * P.uF,
            10 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
        ]

        VDD_DRAM_0V9_CAPS = (
            self.VDD_DRAM_0V9.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDD_DRAM_0V9_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDD_DRAM_0V9_CAPS, VDD_DRAM_0V9_CAP_FOOTPRINTS, VDD_DRAM_0V9_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # NVCC_DRAM_1V1
        NVCC_DRAM_1V1_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0402", 2), 
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
        ]
        NVCC_DRAM_1V1_CAP_VALUES = [
            10 * P.uF,
            10 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
            1 * P.uF,
        ]

        NVCC_DRAM_1V1_CAPS = (
            self.NVCC_DRAM_1V1.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(NVCC_DRAM_1V1_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            NVCC_DRAM_1V1_CAPS, NVCC_DRAM_1V1_CAP_FOOTPRINTS, NVCC_DRAM_1V1_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # VDD_1V8
        VDD_1V8_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0302", 2),
            *([("0201", 1)] * 9) # Repeat 9 times
        ]
        VDD_1V8_CAP_VALUES = [
            10 * P.uF,
            10 * P.uF,
            *([220 * P.nF] * 9)  # Repeat 220 * P.nF nine times
        ]

        VDD_1V8_CAPS = (
            self.VDD_1V8.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDD_1V8_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDD_1V8_CAPS, VDD_1V8_CAP_FOOTPRINTS, VDD_1V8_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # VDD_3V3
        VDD_3V3_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
            ("0201", 2),
        ]
        VDD_3V3_CAP_VALUES = [
            4.7 * P.uF,
            220 * P.nF,
            220 * P.nF,
            220 * P.nF,
            220 * P.nF,
        ]

        VDD_3V3_CAPS = (
            self.VDD_3V3.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDD_3V3_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDD_3V3_CAPS, VDD_3V3_CAP_FOOTPRINTS, VDD_3V3_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # NVCC_ENET
        # NVCC_ENET_CAP = self.NVCC_ENET.decoupled.decouple()
        # NVCC_ENET_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        # NVCC_ENET_CAP.capacitance.merge(F.Range.from_center_rel(220 * P.nF, 0.2))

        # NVCC_SD2
        # NVCC_SD2_CAP = self.NVCC_SD2.decoupled.decouple()
        # NVCC_SD2_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        # NVCC_SD2_CAP.capacitance.merge(F.Range.from_center_rel(220 * P.nF, 0.2))

        # VDD_PHY_1V2
        VDD_PHY_1V2_CAP_FOOTPRINTS = [
            ("0402", 2),
            ("0201", 2),
        ]
        VDD_PHY_1V2_CAP_VALUES = [
            2.2 * P.uF,
            220 * P.nF,
        ]

        VDD_PHY_1V2_CAPS = (
            self.VDD_PHY_1V2.decoupled.decouple()
            .specialize(F.MultiCapacitor(len(VDD_PHY_1V2_CAP_FOOTPRINTS)))
            .capacitors
        )

        for cap, footprint, value in zip(
            VDD_PHY_1V2_CAPS, VDD_PHY_1V2_CAP_FOOTPRINTS, VDD_PHY_1V2_CAP_VALUES
        ):
            cap.add(F.has_footprint_requirement_defined([footprint]))
            cap.capacitance.merge(F.Range.from_center_rel(value, 0.2))

        # VDD_PHY_0V9
        VDD_PHY_0V9_CAP = self.VDD_PHY_0V9.decoupled.decouple()
        VDD_PHY_0V9_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        VDD_PHY_0V9_CAP.capacitance.merge(F.Range.from_center_rel(220 * P.nF, 0.2))

        # MIPI VREG CAP
        self.MIPI_VREG_CAP.add(F.has_footprint_requirement_defined([("0201", 2)]))
        self.MIPI_VREG_CAP.capacitance.merge(F.Range.from_center_rel(2.2 * P.uF, 0.2))
        self.imx8.MIPI_VREG_CAP.connect_via(self.MIPI_VREG_CAP, self.VDD_3V3.lv)


class App(Module):
    processor: NXP_Semicon_MIMX8MM6CVTKZAA
