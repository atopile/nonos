import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.units import P  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties

# Interfaces
from .HDMI import HDMI

# Components
from .HRSHirose_DF40C_100DS_0_4V51 import HRSHirose_DF40C_100DS_0_4V51


logger = logging.getLogger(__name__)

class CM4_MINIMAL(Module):
    """
    CM4 module with minimal components
    """

    # Interfaces
    HDMI0: HDMI
    HDMI1: HDMI

    # Components
    HDI_A: HRSHirose_DF40C_100DS_0_4V51
    HDI_B: HRSHirose_DF40C_100DS_0_4V51



    def __preinit__(self) -> None:
        # ------------------------------------
        #           connections
        # ------------------------------------
        #HDMI0
        self.HDMI0.data2.p.connect(self.HDI_A.unnamed[70])  # HDMI0_D2_P, pin 170
        self.HDMI0.data2.n.connect(self.HDI_A.unnamed[72])  # HDMI0_D2_N, pin 172
        self.HDMI0.data1.p.connect(self.HDI_A.unnamed[76])  # HDMI0_D1_P, pin 176
        self.HDMI0.data1.n.connect(self.HDI_A.unnamed[78])  # HDMI0_D1_N, pin 178
        self.HDMI0.data0.p.connect(self.HDI_A.unnamed[82])  # HDMI0_D0_P, pin 182
        self.HDMI0.data0.n.connect(self.HDI_A.unnamed[84])  # HDMI0_D0_N, pin 184

        # Clock pair
        self.HDMI0.clock.p.connect(self.HDI_A.unnamed[88])  # HDMI0_CK_P, pin 188
        self.HDMI0.clock.n.connect(self.HDI_A.unnamed[90])  # HDMI0_CK_N, pin 190

        # I2C and control signals
        self.HDMI0.i2c.scl.connect(self.HDI_A.unnamed[100]) # HDMI0_SCL, pin 200
        self.HDMI0.i2c.sda.connect(self.HDI_A.unnamed[99])  # HDMI0_SDA, pin 199
        self.HDMI0.cec.connect(self.HDI_A.unnamed[51])      # HDMI0_CEC, pin 151
        self.HDMI0.hotplug.connect(self.HDI_A.unnamed[53])  # HDMI0_HOTPLUG, pin 153
        
        # HDMI1
        self.HDMI1.data2.p.connect(self.HDI_A.unnamed[68])  # HDMI0_D2_P, pin 168
        self.HDMI1.data2.n.connect(self.HDI_A.unnamed[70])  # HDMI0_D2_N, pin 170
        self.HDMI1.data1.p.connect(self.HDI_A.unnamed[76])  # HDMI0_D1_P, pin 176
        self.HDMI1.data1.n.connect(self.HDI_A.unnamed[78])  # HDMI0_D1_N, pin 178
        self.HDMI1.data0.p.connect(self.HDI_A.unnamed[82])  # HDMI0_D0_P, pin 182
        self.HDMI1.data0.n.connect(self.HDI_A.unnamed[84])  # HDMI0_D0_N, pin 184

        # Clock pair
        self.HDMI1.clock.p.connect(self.HDI_A.unnamed[88])  # HDMI0_CK_P, pin 188
        self.HDMI1.clock.n.connect(self.HDI_A.unnamed[90])  # HDMI0_CK_N, pin 190

        # I2C and control signals
        self.HDMI1.i2c.scl.connect(self.HDI_A.unnamed[47])      # HDMI0_SCL, pin 147
        self.HDMI1.i2c.sda.connect(self.HDI_A.unnamed[45])      # HDMI0_SDA, pin 145
        self.HDMI1.cec.connect(self.HDI_A.unnamed[49])      # HDMI0_CEC, pin 149
        self.HDMI1.hotplug.connect(self.HDI_A.unnamed[51])  # HDMI0_HOTPLUG, pin 151
        

