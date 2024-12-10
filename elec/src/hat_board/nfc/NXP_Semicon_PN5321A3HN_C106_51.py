# This file is part of the faebryk project
# SPDX-License-Identifier: MIT

import logging

import faebryk.library._F as F  # noqa: F401
from faebryk.core.module import Module
from faebryk.libs.library import L  # noqa: F401
from faebryk.libs.picker.picker import DescriptiveProperties
from faebryk.libs.units import P  # noqa: F401

logger = logging.getLogger(__name__)


class _NXP_Semicon_PN5321A3HN_C106_51(Module):
    """
    TODO: Docstring describing your module

    QFN-40-EP(6x6) RFID ICs ROHS
    """

    # ----------------------------------------
    #     modules, interfaces, parameters
    # ----------------------------------------
    # TODO: Change auto-generated interface types to actual high level types
    DVSS: F.Electrical  # pin: 1
    LOADMOD: F.Electrical  # pin: 2
    TVSS1: F.Electrical  # pin: 3
    TX1: F.Electrical  # pin: 4
    TVDD: F.Electrical  # pin: 5
    TX2: F.Electrical  # pin: 6
    TVSS2: F.Electrical  # pin: 7
    AVDD: F.Electrical  # pin: 8
    VMID: F.Electrical  # pin: 9
    RX: F.Electrical  # pin: 10
    AVSS: F.Electrical  # pin: 11
    AUX1: F.Electrical  # pin: 12
    AUX2: F.Electrical  # pin: 13
    OSCIN: F.Electrical  # pin: 14
    OSCOUT: F.Electrical  # pin: 15
    I0: F.Electrical  # pin: 16
    I1: F.Electrical  # pin: 17
    TESTEN: F.Electrical  # pin: 18
    P35: F.Electrical  # pin: 19
    N_C_: F.Electrical  # pins: 20, 21, 22
    PVDD: F.Electrical  # pin: 23
    P30_UART_RX: F.Electrical  # pin: 24
    P70_IRQ: F.Electrical  # pin: 25
    RSTOUT_N: F.Electrical  # pin: 26
    NSS_P50_SCL_HSU_RX: F.Electrical  # pin: 27
    MOSI_SDA_HSU_TX: F.Electrical  # pin: 28
    MISO_P71: F.Electrical  # pin: 29
    SCK_P72: F.Electrical  # pin: 30
    P31_UART_TX: F.Electrical  # pin: 31
    P32_INT0: F.Electrical  # pin: 32
    P33_INT1: F.Electrical  # pin: 33
    P34_SIC_CLK: F.Electrical  # pin: 34
    SIGOUT: F.Electrical  # pin: 35
    SIGIN: F.Electrical  # pin: 36
    SVDD: F.Electrical  # pin: 37
    RSTPD_N: F.Electrical  # pin: 38
    DVDD: F.Electrical  # pin: 39
    VBAT: F.Electrical  # pin: 40
    EP: F.Electrical  # pin: 41

    # ----------------------------------------
    #                 traits
    # ----------------------------------------
    lcsc_id = L.f_field(F.has_descriptive_properties_defined)({"LCSC": "C880904"})
    designator_prefix = L.f_field(F.has_designator_prefix_defined)("U")
    descriptive_properties = L.f_field(F.has_descriptive_properties_defined)(
        {
            DescriptiveProperties.manufacturer: "NXP Semicon",
            DescriptiveProperties.partno: "PN5321A3HN/C106,51",
        }
    )
    datasheet = L.f_field(F.has_datasheet_defined)(
        "https://www.nxp.com/docs/en/nxp/data-sheets/PN532_C1.pdf"
    )

    @L.rt_field
    def attach_via_pinmap(self):
        return F.can_attach_to_footprint_via_pinmap(
            {
                "1": self.DVSS,
                "2": self.LOADMOD,
                "3": self.TVSS1,
                "4": self.TX1,
                "5": self.TVDD,
                "6": self.TX2,
                "7": self.TVSS2,
                "8": self.AVDD,
                "9": self.VMID,
                "10": self.RX,
                "11": self.AVSS,
                "12": self.AUX1,
                "13": self.AUX2,
                "14": self.OSCIN,
                "15": self.OSCOUT,
                "16": self.I0,
                "17": self.I1,
                "18": self.TESTEN,
                "19": self.P35,
                "20": None,
                "21": None,
                "22": None,
                "23": self.PVDD,
                "24": self.P30_UART_RX,
                "25": self.P70_IRQ,
                "26": self.RSTOUT_N,
                "27": self.NSS_P50_SCL_HSU_RX,
                "28": self.MOSI_SDA_HSU_TX,
                "29": self.MISO_P71,
                "30": self.SCK_P72,
                "31": self.P31_UART_TX,
                "32": self.P32_INT0,
                "33": self.P33_INT1,
                "34": self.P34_SIC_CLK,
                "35": self.SIGOUT,
                "36": self.SIGIN,
                "37": self.SVDD,
                "38": self.RSTPD_N,
                "39": self.DVDD,
                "40": self.VBAT,
                "41": self.EP,
            }
        )

    def __preinit__(self):
        self.DVSS.connect(self.EP, self.TESTEN)


class NXP_Semicon_PN5321A3HN_C106_51(Module):
    """
    QFN-40-EP(6x6) RFID ICs ROHS
    """

    nfc_ic: _NXP_Semicon_PN5321A3HN_C106_51
    tx1_inductor: F.Inductor
    tx2_inductor: F.Inductor
    tx1_series_capacitor: F.Capacitor
    tx2_series_capacitor: F.Capacitor
    tx1_decouple_capacitor: F.Capacitor
    tx2_decouple_capacitor: F.Capacitor
    tx1_mid_decouple_capacitor: F.Capacitor
    tx2_mid_decouple_capacitor: F.Capacitor
    rx_capacitor: F.Capacitor
    rx_resistor: F.Resistor
    vmid_resistor: F.Resistor
    oscillator: F.Crystal_Oscillator

    reset: F.ElectricLogic
    interrupt: F.ElectricLogic
    antenna_output: F.DifferentialPair
    i2c: F.I2C
    power_3v3: F.ElectricPower
    power_tvdd: F.ElectricPower
    power_vbat: F.ElectricPower
    power_dvdd: F.ElectricPower
    power_pvdd: F.ElectricPower
    power_avdd: F.ElectricPower
    power_svdd: F.ElectricPower
    power_vmid: F.ElectricPower

    def __preinit__(self):

        # Power
        # All power rails connected to 3v3 (external power supply)
        self.power_3v3.connect(
            self.power_dvdd,
            self.power_tvdd,
            self.power_pvdd,
            self.power_vbat,
            self.power_avdd,
        )
        # Connect power rails to IC
        self.power_dvdd.hv.connect(self.nfc_ic.DVDD)
        self.power_dvdd.lv.connect(self.nfc_ic.DVSS, self.nfc_ic.EP)

        self.power_tvdd.hv.connect(self.nfc_ic.TVDD)
        self.power_tvdd.lv.connect(self.nfc_ic.TVSS1, self.nfc_ic.TVSS2)

        self.power_pvdd.hv.connect(self.nfc_ic.PVDD)
        self.power_pvdd.lv.connect(self.nfc_ic.VMID)

        self.power_vbat.hv.connect(self.nfc_ic.VBAT)
        # self.power_vbat.lv.connect(self.nfc_ic.DVSS)

        self.power_avdd.hv.connect(self.nfc_ic.AVDD)
        self.power_avdd.lv.connect(self.nfc_ic.AVSS)

        self.power_svdd.hv.connect(self.nfc_ic.SVDD)
        self.power_svdd.lv.connect(self.power_3v3.lv)

        self.power_vmid.hv.connect(self.nfc_ic.VMID)
        # self.power_vmid.lv.connect(self.nfc_ic.DVSS)

        # Decoupling caps for power railsx
        vbat_cap = self.power_vbat.decoupled.decouple()
        vbat_cap.add(F.has_package_requirement("0402"))
        vbat_cap.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))

        svdd_cap = self.power_svdd.decoupled.decouple()
        svdd_cap.add(F.has_package_requirement("0402"))
        svdd_cap.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))

        avdd_cap = self.power_avdd.decoupled.decouple()
        avdd_cap.add(F.has_package_requirement("0402"))
        avdd_cap.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))

        pvdd_cap = self.power_pvdd.decoupled.decouple()
        pvdd_cap.add(F.has_package_requirement("0402"))
        pvdd_cap.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))

        vmid_cap = self.power_vmid.decoupled.decouple()
        vmid_cap.add(F.has_package_requirement("0402"))
        vmid_cap.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))
        self.nfc_ic.VMID.connect_via(vmid_cap, self.power_vmid.lv)

        POWER_TVDD_CAP_PROPERTIES = [
            {"value": 10 * P.uF, "footprint": "0603"},
            {"value": 100 * P.nF, "footprint": "0402"},
        ]

        POWER_TVDD_CAPS = []
        for props in POWER_TVDD_CAP_PROPERTIES:
            cap = self.power_tvdd.decoupled.decouple()
            cap.add(F.has_package_requirement(props["footprint"]))
            cap.capacitance.constrain_subset(
                L.Range.from_center_rel(props["value"], 0.2)
            )
            POWER_TVDD_CAPS.append(cap)

        POWER_DVDD_CAP_PROPERTIES = [
            {"value": 10 * P.uF, "footprint": "0603"},
            {"value": 100 * P.nF, "footprint": "0402"},
        ]

        POWER_DVDD_CAPS = []
        for props in POWER_DVDD_CAP_PROPERTIES:
            cap = self.power_dvdd.decoupled.decouple()
            cap.add(F.has_package_requirement(props["footprint"]))
            cap.capacitance.constrain_subset(
                L.Range.from_center_rel(props["value"], 0.2)
            )
            POWER_DVDD_CAPS.append(cap)

        # Antenna
        tx1_mid = F.Net.with_name("tx_1_mid")
        tx1_mid.part_of.connect_via(self.tx1_series_capacitor, self.antenna_output.p.signal)
        tx1_mid.part_of.connect_via(self.tx1_inductor, self.nfc_ic.TX1)
        tx1_mid.part_of.connect_via(self.tx1_mid_decouple_capacitor, self.power_tvdd.lv)
        self.antenna_output.p.signal.connect_via(self.tx1_decouple_capacitor, self.power_tvdd.lv)

        tx2_mid = F.Net.with_name("tx_2_mid")
        tx2_mid.part_of.connect_via(self.tx2_series_capacitor, self.antenna_output.n.signal)
        tx2_mid.part_of.connect_via(self.tx2_inductor, self.nfc_ic.TX2)
        tx2_mid.part_of.connect_via(self.tx2_mid_decouple_capacitor, self.power_tvdd.lv)
        tx2_mid.part_of.connect_via([self.rx_capacitor, self.rx_resistor], self.nfc_ic.RX)
        self.antenna_output.n.signal.connect_via(self.tx2_decouple_capacitor, self.power_tvdd.lv)

        self.power_vmid.hv.connect_via(self.vmid_resistor, self.nfc_ic.RX)

        # Interrupt and reset
        self.interrupt.signal.connect(self.nfc_ic.P70_IRQ)
        self.reset.signal.connect(self.nfc_ic.RSTOUT_N)

        # I2C
        self.i2c.scl.signal.connect(self.nfc_ic.MOSI_SDA_HSU_TX)
        self.i2c.sda.signal.connect(self.nfc_ic.NSS_P50_SCL_HSU_RX)
        self.i2c.terminate()

        # Select communication mode
        # I2C = I0: 1, I1: 0
        # UART = I0: 0, I1: 0
        # SPI = I0: 0, I1: 1
        self.nfc_ic.I0.connect(self.power_3v3.hv)
        self.nfc_ic.I1.connect(self.power_3v3.lv)

        # Oscillator
        self.nfc_ic.OSCIN.connect(self.oscillator.xtal_if.xin)
        self.nfc_ic.OSCOUT.connect(self.oscillator.xtal_if.xout)
        self.oscillator.xtal_if.gnd.connect(self.power_3v3.lv)
        self.oscillator.crystal.add(F.has_descriptive_properties_defined({"LCSC": "C70591"}))
        self.oscillator.crystal.add(F.can_attach_to_footprint_via_pinmap({"1": self.oscillator.crystal.unnamed[0], "3": self.oscillator.crystal.unnamed[1], "2": self.oscillator.crystal.gnd, "4": self.oscillator.crystal.gnd}))
        self.oscillator.crystal.add(F.has_designator_prefix_defined("XTAL"))
        self.oscillator.del_trait(F.has_pcb_layout)

        # Antenna parameters
        self.tx1_inductor.add(F.has_descriptive_properties_defined({"LCSC": "C91630"}))
        self.tx2_inductor.add(F.has_descriptive_properties_defined({"LCSC": "C91630"}))
        self.tx1_series_capacitor.add(F.has_package_requirement("0402"))
        self.tx2_series_capacitor.add(F.has_package_requirement("0402"))
        self.tx1_series_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(22 * P.pF, 0.2))
        self.tx2_series_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(22 * P.pF, 0.2))
        self.tx1_mid_decouple_capacitor.add(F.has_package_requirement("0402"))
        self.tx2_mid_decouple_capacitor.add(F.has_package_requirement("0402"))
        self.tx1_mid_decouple_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(220 * P.pF, 0.2))
        self.tx2_mid_decouple_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(220 * P.pF, 0.2))
        self.tx1_decouple_capacitor.add(F.has_package_requirement("0402"))
        self.tx2_decouple_capacitor.add(F.has_package_requirement("0402"))
        self.tx1_decouple_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.pF, 0.2))
        self.tx2_decouple_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.pF, 0.2))
        self.rx_capacitor.add(F.has_package_requirement("0402"))
        self.rx_capacitor.capacitance.constrain_subset(L.Range.from_center_rel(100 * P.nF, 0.2))
        self.rx_resistor.add(F.has_package_requirement("0402"))
        self.rx_resistor.resistance.constrain_subset(L.Range.from_center_rel(1 * P.kohm, 0.2))
