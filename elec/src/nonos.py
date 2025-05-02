# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401

# Components
from .amplifier.Texas_Instruments_TAS5825MRHBR import Texas_Instruments_TAS5825MRHBR
from .components.hctl_hc_type_c24p_vs935a_f1104 import (
    HCTL_HC_TYPE_C_24P_VS9_3_5A_F1_1_04,
)
from .components.js_tsales_america_b02b_xa_sk1al_fsn import (
    JST_Sales_America_B02B_XASK_1_ALFSN,
)
from .components.saleae_header import SaleaeHeader
from .hat_board.TE_Connectivity_1_2328702_0 import BoardToBoardConnector

logger = logging.getLogger(__name__)


# FIXME replace with ato module
class NONOS(Module):
    """
    Open-source smart speaker
    """

    # FIXME
    # processor: CM4_MINIMAL
    # rj45: HANRUNZhongshan_HanRun_Elec_HR911130A
    # pd_controller: PDController
    # regulator: Texas_Instruments_TPS56637RPAR
    amplifier: Texas_Instruments_TAS5825MRHBR
    board_to_board_connector: BoardToBoardConnector
    full_range_speaker_connector: JST_Sales_America_B02B_XASK_1_ALFSN
    tweeter_speaker_connector: JST_Sales_America_B02B_XASK_1_ALFSN
    usb_connector: HCTL_HC_TYPE_C_24P_VS9_3_5A_F1_1_04

    power_20v: F.ElectricPower
    power_5v: F.ElectricPower
    power_3v3: F.ElectricPower

    debug_header_1: SaleaeHeader
    debug_header_2: SaleaeHeader

    debug_header_2: SaleaeHeader

    def __preinit__(self):
        # Power
        self.usb_connector.power_vbus.connect(self.pd_controller.power_vbus)
        self.pd_controller.power_vsink.connect(self.power_20v)
        for i, cc in enumerate(self.usb_connector.cc):
            cc.connect(self.pd_controller.cc[i])
        self.pd_controller.i2c.connect(self.processor.i2c)
        self.regulator.power_in.connect(self.power_20v)
        self.regulator.power_out.connect(self.power_5v)
        self.power_5v.connect(self.processor.power_5v)
        self.power_3v3.connect(self.pd_controller.power_mcu)
        self.processor.power_3v3.connect(
            self.power_3v3
        )  # Onboard regulator can provide 3.3V

        # Ethernet
        self.rj45.ethernet.connect(self.processor.ethernet)
        self.rj45.power_led.connect(self.processor.power_3v3)

        # Amplifier
        self.amplifier.power_pvdd.connect(self.power_20v)
        self.amplifier.power_dvdd.connect(self.power_3v3)
        self.processor.i2s.connect(self.amplifier.i2s)
        self.processor.i2c.connect(self.amplifier.i2c)
        self.processor.gpio[0].connect(self.amplifier.mute)
        self.processor.gpio[1].connect(self.amplifier.warn)
        self.processor.gpio[2].connect(self.amplifier.fault)
        self.processor.gpio[3].connect(self.amplifier.pdn)
        self.amplifier.output_a.p.signal.connect(
            self.full_range_speaker_connector.unnamed[0]
        )
        self.amplifier.output_a.n.signal.connect(
            self.full_range_speaker_connector.unnamed[1]
        )
        self.amplifier.output_b.p.signal.connect(
            self.tweeter_speaker_connector.unnamed[1]
        )
        self.amplifier.output_b.n.signal.connect(
            self.tweeter_speaker_connector.unnamed[0]
        )

        # Hat board
        self.board_to_board_connector.i2c.connect(self.processor.i2c)
        self.board_to_board_connector.power_3v3.connect(self.power_3v3)
        self.board_to_board_connector.power_5v.connect(self.power_5v)
        self.board_to_board_connector.hat_reset.connect(self.processor.gpio[4])
        self.board_to_board_connector.hat_nfc_irq.connect(self.processor.gpio[5])
        self.board_to_board_connector.hat_touch_irq.connect(self.processor.gpio[6])
        self.board_to_board_connector.hat_led_data.connect(self.processor.gpio[7])

        # self.power_5v.voltage.constrain_subset(L.Range.from_center_rel(5 * P.V, 0.1))
        # self.power_3v3.voltage.constrain_subset(L.Range.from_center_rel(
        #   3.3 * P.V, 0.1))

        # Debug headers
        self.processor.uart_tx.connect(self.debug_header_1.pins[0])
        self.processor.uart_rx.connect(self.debug_header_1.pins[1])
        self.processor.i2c.scl.connect(self.debug_header_1.pins[2])
        self.processor.i2c.sda.connect(self.debug_header_1.pins[3])

        self.processor.i2s.sck.connect(self.debug_header_2.pins[0])
        self.processor.i2s.ws.connect(self.debug_header_2.pins[1])
        self.processor.i2s.sd.connect(self.debug_header_2.pins[2])
        self.power_5v.hv.connect(self.debug_header_2.pins[3].signal)
