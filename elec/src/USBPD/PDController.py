# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
import typer
from faebryk.core.module import Module
from faebryk.libs.examples.buildutil import apply_design_to_pcb
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.logging import setup_basic_logging
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

# Components
from TYPE_C_16PIN_2MD073 import TYPE_C_16PIN_2MD073

logger = logging.getLogger(__name__)

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
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
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
    def pin_association_heuristic(self):
        return {1: self.A, 2: self.K1, 3: self.K2}
        return F.has_pin_association_heuristic_lookup_table(
            mapping={self.A: ["A"], self.K1: ["1"], self.K2: ["2"]},
            accept_prefix=False,
            case_sensitive=False,
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

    CC1: F.ElectricLogic
    CC2: F.ElectricLogic
    CC1DB: F.ElectricLogic
    CC2DB: F.ElectricLogic

    ATTACH: F.Electrical
    GPIO: F.Electrical
    ADDR1: F.Electrical
    POWER_OK3: F.Electrical
    VDD: F.Electrical
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
    GND: F.Electrical

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
                self.CC1DB: ["CC1DB"],
                self.CC2.signal: ["CC2"],
                self.CC2DB.signal: ["CC2DB"],
                self.DISCH: ["DISCH"],
                self.EP: ["EP"],
                self.GND: ["GND"],
                self.GPIO: ["GPIO"],
                self.NC: ["NC"],
                self.POWER_OK2: ["POWER_OK2"],
                self.POWER_OK3: ["POWER_OK3"],
                self.RESET: ["RESET"],
                self.SCL: ["SCL"],
                self.SDA: ["SDA"],
                self.VBUS_EN_SNK: ["VBUS_EN_SNK"],
                self.VBUS_VS_DISCH: ["VBUS_VS_DISCH"],
                self.VDD: ["VDD"],
                self.VREG_1V2.lv: ["VREG_1V2"],
                self.VREG_2V7.lv: ["VREG_2V7"],
                self.VSYS: ["VSYS"],
            },
            accept_prefix=False,
            case_sensitive=False,
        )
    
    def __preinit__(self):
        self.VREG_1V2.voltage.merge(F.Range(1.1 * P.V, 1.3 * P.V))
        self.VREG_2V7.voltage.merge(F.Range(2.6 * P.V, 2.8 * P.V))



class App(Module):
    pd_controller: STUSB4500QTR
    usb_connector: TYPE_C_16PIN_2MD073
    # esd_cc: ESDA25W

    VSYNC: F.ElectricPower
    VMCU: F.ElectricPower
    VBUS: F.ElectricPower

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------
        self.usb_connector.CC1.connect(self.pd_controller.CC1, self.pd_controller.CC1DB)
        self.usb_connector.CC2.connect(self.pd_controller.CC2, self.pd_controller.CC2DB)

        # ESD protection TODO: Fix pin association, footprint names both pins K
        # self.usb_connector.CC1.connect(self.esd_cc.K1)
        # self.usb_connector.CC2.connect(self.esd_cc.K2)
        # self.esd_cc.A.connect(self.usb_connector.POWER_VBUS.lv)

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        self.VSYNC.voltage.merge(F.Range(5 * P.V, 20 * P.V))
        self.VMCU.voltage.merge(F.Range(0 * P.V, 3.6 * P.V))
        self.VBUS.voltage.merge(F.Range(5 * P.V, 20 * P.V))

def main():
    logger.info("Building app")
    app = App()

    logger.info("Export")
    apply_design_to_pcb(app)


if __name__ == "__main__":
    setup_basic_logging()
    logger.info("Running example")

    typer.run(main)