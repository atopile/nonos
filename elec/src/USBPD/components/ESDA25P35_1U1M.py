import faebryk.library._F as F
from faebryk.libs.library import L
from faebryk.libs.picker.picker import DescriptiveProperties


class ESDA25P35_1U1M(F.Diode):
    """
    TODO: Docstring describing your module

    35A@(8/20us) 41V 1.4kW 23.3V 22V DFN1610-2
    ESD and Surge Protection (TVS/ESD) ROHS
    """

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C1974707"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("D")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "STMicroelectronics",
            DescriptiveProperties.partno: "ESDA25P35-1U1M",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2201300300_STMicroelectronics-ESDA25P35-1U1M_C1974707.pdf"
    )

    @L.rt_field
    def pin_association_heuristic(self):
        return F.has_pin_association_heuristic_lookup_table(
            mapping={self.anode: ["1"], self.cathode: ["2"]},
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
