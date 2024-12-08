import faebryk.library._F as F
from faebryk.libs.library import L
from faebryk.libs.units import P
from faebryk.core.module import Module
from faebryk.libs.picker.picker import DescriptiveProperties


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
    VDD: F.ElectricPower

    CC1: F.ElectricLogic
    CC2: F.ElectricLogic
    CC1DB: F.ElectricLogic
    CC2DB: F.ElectricLogic

    I2C: F.I2C

    ATTACH: F.Electrical
    GPIO: F.Electrical
    ADDR1: F.Electrical
    POWER_OK3: F.Electrical
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
    ADDR0: F.Electrical

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
                self.CC1DB.signal: ["CC1DB"],
                self.CC2.signal: ["CC2"],
                self.CC2DB.signal: ["CC2DB"],
                self.DISCH: ["DISCH"],
                self.EP: ["EP"],
                self.VDD.lv: ["GND"],
                self.GPIO: ["GPIO"],
                self.NC: ["NC"],
                self.POWER_OK2: ["POWER_OK2"],
                self.POWER_OK3: ["POWER_OK3"],
                self.RESET: ["RESET"],
                self.I2C.scl.signal: ["SCL"],
                self.I2C.sda.signal: ["SDA"],
                self.VBUS_EN_SNK: ["VBUS_EN_SNK"],
                self.VBUS_VS_DISCH: ["VBUS_VS_DISCH"],
                self.VDD.hv: ["VDD"],
                self.VREG_1V2.hv: ["VREG_1V2"],
                self.VREG_2V7.hv: ["VREG_2V7"],
                self.VSYS: ["VSYS"],
            },
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        self.VREG_1V2.voltage.constrain_subset(L.Range(1.1 * P.V, 1.3 * P.V))
        self.VREG_2V7.voltage.constrain_subset(L.Range(2.6 * P.V, 2.8 * P.V))

        self.VDD.lv.connect(
            self.VREG_2V7.lv, self.VREG_1V2.lv, self.EP, self.RESET, self.VSYS, self.NC
        )

        # Set address
        self.ADDR0.connect(self.VDD.lv)
        self.ADDR1.connect(self.VDD.lv)
