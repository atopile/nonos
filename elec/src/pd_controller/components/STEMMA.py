import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties


class STEMMA_RIGHT_ANGLE(Module):
    """
    TODO: Docstring describing your module

    1x4P 4P SH Tin 4 -25℃~+85℃ 1A 1 1mm Copper alloy Horizontal attachment SMD,P=1mm,Surface Mount，Right Angle Wire To Board Connector ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    power: F.ElectricPower
    i2c: F.I2C

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C160404"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("CN")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "JST Sales America",
            DescriptiveProperties.partno: "SM04B-SRSS-TB(LF)(SN)",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_JST-SM04B-SRSS-TB-LF-SN_C160404.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={
                self.power.lv: ["1","5","6"],
                self.power.hv: ["2"],
                self.i2c.sda.signal: ["3"],
                self.i2c.scl.signal: ["4"]
            },
            accept_prefix=False,
            case_sensitive=False,
        )

    def __preinit__(self):
        # ------------------------------------
        #           connections
        # ------------------------------------

        # ------------------------------------
        #          parametrization
        # ------------------------------------
        pass