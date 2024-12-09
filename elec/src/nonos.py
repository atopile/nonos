

# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

# Components
from .cm4.cm4 import CM4_MINIMAL
from .cm4.HANRUNZhongshan_HanRun_Elec_HR911130A import HANRUNZhongshan_HanRun_Elec_HR911130A
from .pd_controller.pd_controller import PDController
from .amplifier.Texas_Instruments_TAS5825MRHBR import Texas_Instruments_TAS5825MRHBR
from .power_supply.Texas_Instruments_TPS56637RPAR import Texas_Instruments_TPS56637RPAR
from .hat_board.TE_Connectivity_1_2328702_0 import BoardToBoardConnector

logger = logging.getLogger(__name__)

class NONOS(Module):
    """
    Open-source smart speaker
    """
    processor: CM4_MINIMAL
    rj45: HANRUNZhongshan_HanRun_Elec_HR911130A
    pd_controller: PDController
    regulator: Texas_Instruments_TPS56637RPAR
    amplifier: Texas_Instruments_TAS5825MRHBR
    board_to_board_connector: BoardToBoardConnector
    # DSP

    power_vbus: F.ElectricPower
    power_5v: F.ElectricPower
    power_3v3: F.ElectricPower

    def __preinit__(self):

        # Power
        self.pd_controller.power_vbus.connect(self.power_vbus)
        self.regulator.power_in.connect(self.power_vbus)
        self.regulator.power_out.connect(self.power_5v)
        self.processor.power_3v3.connect(self.power_3v3) # Onboard regulator can provide 3.3V

        # Ethernet
        self.rj45.ethernet.connect(self.processor.ethernet)
        self.rj45.power_led.connect(self.processor.power_3v3)

        # Amplifier
        self.processor.i2s.connect(self.amplifier.i2s)
        self.processor.i2c.connect(self.amplifier.i2c)
        self.processor.gpio[0].connect(self.amplifier.mute)
        self.processor.gpio[1].connect(self.amplifier.warn)
        self.processor.gpio[2].connect(self.amplifier.fault)
        self.processor.gpio[3].connect(self.amplifier.pdn)

        # Hat board
        self.board_to_board_connector.i2c.connect(self.processor.i2c)
        self.board_to_board_connector.power_3v3.connect(self.power_3v3)
        self.board_to_board_connector.power_5v.connect(self.power_5v)
        self.board_to_board_connector.hat_reset.connect(self.processor.gpio[4])
        self.board_to_board_connector.hat_nfc_irq.connect(self.processor.gpio[5])
        self.board_to_board_connector.hat_touch_irq.connect(self.processor.gpio[6])
        self.board_to_board_connector.hat_led_data.connect(self.processor.gpio[7])
