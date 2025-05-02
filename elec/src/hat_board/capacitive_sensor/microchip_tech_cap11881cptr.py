# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

logger = logging.getLogger(__name__)


class _Microchip_Tech_CAP1188_1_CP_TR(Module):
    """
    TODO: Docstring describing your module

    8 QFN-24-EP(4x4)
    Touch Sensors ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    SPI_CSh: F.Electrical  # pin: 1
    WAKE_SPI_MOSI: F.Electrical  # pin: 2
    SMDATA_BC_DATA_SPI_MSIO_SPI_MISO: F.Electrical  # pin: 3
    SMCLK_BC_CLK_SPI_CLK: F.Electrical  # pin: 4
    LED1: F.Electrical  # pin: 5
    LED2: F.Electrical  # pin: 6
    LED3: F.Electrical  # pin: 7
    LED4: F.Electrical  # pin: 8
    LED5: F.Electrical  # pin: 9
    LED6: F.Electrical  # pin: 10
    LED7: F.Electrical  # pin: 11
    LED8: F.Electrical  # pin: 12
    ALERTh_BC_IRQh: F.Electrical  # pin: 13
    ADDR_COMM: F.Electrical  # pin: 14
    CS8: F.Electrical  # pin: 15
    CS7: F.Electrical  # pin: 16
    CS6: F.Electrical  # pin: 17
    CS5: F.Electrical  # pin: 18
    CS4: F.Electrical  # pin: 19
    CS3: F.Electrical  # pin: 20
    CS2: F.Electrical  # pin: 21
    CS1: F.Electrical  # pin: 22
    VDD: F.Electrical  # pin: 23
    RESET: F.Electrical  # pin: 24
    GND: F.Electrical  # pin: 25

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    designator_prefix = L.f_field(F.has_designator_prefix)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "Microchip Tech",
            DescriptiveProperties.partno: "CAP1188-1-CP-TR",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2309071116_Microchip-Tech-CAP1188-1-CP-TR_C2652057.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.SPI_CSh,
                "2": self.WAKE_SPI_MOSI,
                "3": self.SMDATA_BC_DATA_SPI_MSIO_SPI_MISO,
                "4": self.SMCLK_BC_CLK_SPI_CLK,
                "5": self.LED1,
                "6": self.LED2,
                "7": self.LED3,
                "8": self.LED4,
                "9": self.LED5,
                "10": self.LED6,
                "11": self.LED7,
                "12": self.LED8,
                "13": self.ALERTh_BC_IRQh,
                "14": self.ADDR_COMM,
                "15": self.CS8,
                "16": self.CS7,
                "17": self.CS6,
                "18": self.CS5,
                "19": self.CS4,
                "20": self.CS3,
                "21": self.CS2,
                "22": self.CS1,
                "23": self.VDD,
                "24": self.RESET,
                "25": self.GND,
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


class Microchip_Tech_CAP1188_1_CP_TR(Module):
    """
    8 QFN-24-EP(4x4)
    Touch Sensors ROHS
    """

    power: F.ElectricPower
    i2c: F.I2C
    reset: F.ElectricLogic
    interrupt: F.ElectricLogic
    address: F.ElectricLogic
    pads = L.list_field(8, F.ElectricLogic)

    capacitive_sensor: _Microchip_Tech_CAP1188_1_CP_TR

    @L.rt_field
    def single_electric_reference(self):
        return F.has_single_electric_reference_defined(
            F.ElectricLogic.connect_all_module_references(self)
        )

    def __preinit__(self):
        # Power
        self.power.hv.connect(self.capacitive_sensor.VDD)
        self.power.lv.connect(self.capacitive_sensor.GND)

        decouple_cap = self.power.decoupled.decouple(owner=self).capacitors[0]
        decouple_cap.capacitance.constrain_subset(
            L.Range.from_center_rel(100 * P.nF, 0.3)
        )
        decouple_cap.add(F.has_package(F.has_package.Package.C0402))

        # Data
        self.i2c.sda.line.connect(
            self.capacitive_sensor.SMDATA_BC_DATA_SPI_MSIO_SPI_MISO
        )
        self.i2c.scl.line.connect(self.capacitive_sensor.SMCLK_BC_CLK_SPI_CLK)
        self.reset.line.connect(self.capacitive_sensor.RESET)
        self.interrupt.line.connect(self.capacitive_sensor.ALERTh_BC_IRQh)
        self.address.line.connect(self.capacitive_sensor.ADDR_COMM)

        self.i2c.terminate(owner=self)

        self.interrupt.get_trait(F.ElectricLogic.can_be_pulled).pull(
            up=True, owner=self
        )
        pullup = self.interrupt.get_trait(F.ElectricLogic.has_pulls).get_pulls()[0]
        assert pullup is not None
        pullup.add(F.has_package(F.has_package.Package.R0402))
        pullup.resistance.constrain_subset(L.Range.from_center_rel(10 * P.kohm, 0.05))

        self.reset.get_trait(F.ElectricLogic.can_be_pulled).pull(up=False, owner=self)
        reset_pulldown = self.reset.get_trait(F.ElectricLogic.has_pulls).get_pulls()[1]
        assert reset_pulldown is not None
        reset_pulldown.add(F.has_package(F.has_package.Package.R0402))
        reset_pulldown.resistance.constrain_subset(
            L.Range.from_center_rel(10 * P.kohm, 0.05)
        )

        self.address.get_trait(F.ElectricLogic.can_be_pulled).pull(up=False, owner=self)
        address_pulldown = self.address.get_trait(
            F.ElectricLogic.has_pulls
        ).get_pulls()[1]
        assert address_pulldown is not None
        address_pulldown.add(F.has_package(F.has_package.Package.R0402))
        address_pulldown.resistance.constrain_subset(
            L.Range.from_center_rel(10 * P.kohm, 0.05)
        )

        # Pads
        self.capacitive_sensor.CS1.connect(self.pads[0].line)
        self.capacitive_sensor.CS2.connect(self.pads[1].line)
        self.capacitive_sensor.CS3.connect(self.pads[2].line)
        self.capacitive_sensor.CS4.connect(self.pads[3].line)
        self.capacitive_sensor.CS5.connect(self.pads[4].line)
        self.capacitive_sensor.CS6.connect(self.pads[5].line)
        self.capacitive_sensor.CS7.connect(self.pads[6].line)
        self.capacitive_sensor.CS8.connect(self.pads[7].line)
