# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

from .nfc.NXP_Semicon_PN5321A3HN_C106_51 import NXP_Semicon_PN5321A3HN_C106_51
from .TE_Connectivity_1_2328702_0 import BoardToBoardConnector
from .OPSCO_Optoelectronics_SK6805SIDE_G_001 import OPSCO_Optoelectronics_SK6805SIDE_G_001
# from .capacative_sensor.

logger = logging.getLogger(__name__)

class HatBoard(Module):
    """
    HAT Board
    """
    power_3v3: F.ElectricPower
    power_5v: F.ElectricPower
    i2c: F.I2C

    nfc: NXP_Semicon_PN5321A3HN_C106_51
    board_to_board_connector: BoardToBoardConnector
    leds = L.list_field(23, OPSCO_Optoelectronics_SK6805SIDE_G_001)
    # capacitive_sensor: 


    def __preinit__(self):

        # Connector inverts pinmap, need to flip it back
        self.board_to_board_connector.invert_connector_pinmap()
        
        # Connect LEDs in series
        for i in range(len(self.leds)-1):
            self.leds[i].output.connect(self.leds[i+1].input)

        # Connect first LED
        self.power_3v3.connect(self.board_to_board_connector.power_3v3, self.nfc.power_3v3)
        self.power_5v.connect(self.leds[0].input.power, self.board_to_board_connector.power_5v)
        self.board_to_board_connector.hat_led_data.connect(self.leds[0].input.data)

        # Net naming
        F.Net.with_name("led_data").part_of.connect(self.board_to_board_connector.hat_led_data.signal)
        F.Net.with_name("power_3v3").part_of.connect(self.power_3v3.hv)
        F.Net.with_name("power_5v").part_of.connect(self.power_5v.hv)
        F.Net.with_name("gnd").part_of.connect(self.power_3v3.lv)
        F.Net.with_name("reset").part_of.connect(self.board_to_board_connector.hat_reset.signal)
        F.Net.with_name("i2c_scl").part_of.connect(self.board_to_board_connector.i2c.scl.signal)
        F.Net.with_name("i2c_sda").part_of.connect(self.board_to_board_connector.i2c.sda.signal)
        F.Net.with_name("nfc_irq").part_of.connect(self.board_to_board_connector.hat_nfc_irq.signal)
        F.Net.with_name("touch_irq").part_of.connect(self.board_to_board_connector.hat_touch_irq.signal)
