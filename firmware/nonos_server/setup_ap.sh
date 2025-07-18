#!/bin/bash
nmcli connection add type wifi ifname wlan0 con-name nonos-ap autoconnect yes ssid nonos \
    mode ap ipv4.method shared \
    wifi.band bg wifi.channel 6 \
    wifi-sec.key-mgmt wpa-psk wifi-sec.psk "code2pcb"

nmcli connection up nonos-ap