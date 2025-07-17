#!/bin/bash
set -e

DIR=$(dirname $0)/services
ENABLE="y"
RESTART="n"

for i in $DIR/*.service; do
    isuser=$(grep -q "WantedBy=default.target" $i && echo "y" || echo "n")
    if [ $isuser == "y" ]; then
        target=/home/atopile/.config/systemd/user/$(basename $i)
    else
        target=/etc/systemd/system/$(basename $i)
    fi

    if [ -e $target ]; then
        echo "Skipping $target, already exists"
    else
        echo "Creating symlink $target"
        sudo ln -s $(realpath $i) $target
    fi


    if [ $ENABLE == "y" ]; then
        echo "Enabling $isuser $target"
        if [ $isuser == "y" ]; then
            systemctl enable --user $(basename $i)
        else
            sudo systemctl enable $(basename $i)
        fi
    fi
done

sudo systemctl daemon-reload
systemctl daemon-reload --user

for i in $DIR/*.service; do
    isuser=$(grep -q "User=atopile" $i && echo "y" || echo "n")

    if [ $RESTART == "y" ]; then
        echo "Restarting $isuser $(basename $i)"
        if [ $isuser == "y" ]; then
            systemctl restart --user $(basename $i)
        else
            sudo systemctl restart $(basename $i)
        fi
    fi
done