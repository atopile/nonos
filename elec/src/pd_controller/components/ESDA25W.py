import faebryk.library._F as F
from faebryk.core.module import Module
from faebryk.libs.library import L
from faebryk.libs.picker.picker import DescriptiveProperties


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
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("D")
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
    def pin_association(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "3": self.A,
                "1": self.K1,
                "2": self.K2,
            }
        )

