#!/bin/bash

DIR=$(dirname $0)

dtc -I dts -O dtb -o /boot/overlays/hat.dtbo $DIR/hat.dts


# TODO
# add dtoverlay=hat to /boot/firmware/config.txt