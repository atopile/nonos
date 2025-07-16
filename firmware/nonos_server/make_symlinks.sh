#!/bin/bash
set -e

DIR=$(dirname $0)
ENABLE="y"
RESTART="n"

for i in $DIR/*.service; do
    target=/etc/systemd/system/$(basename $i)
    if [ -f $target ]; then
        echo "Skipping $target, already exists"
    else
        echo "Creating symlink $target"
        sudo ln -s $(realpath $i) $target
    fi

    if [ $ENABLE == "y" ]; then
        echo "Enabling $target"
        sudo systemctl enable $(basename $i)
    fi
done

sudo systemctl daemon-reload

for i in $DIR/*.service; do
    if [ $RESTART == "y" ]; then
        echo "Restarting $(basename $i)"
        sudo systemctl restart $(basename $i)
    fi
done