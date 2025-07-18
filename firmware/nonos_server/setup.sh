#!/bin/bash
# exit on error
set -e

ROOT=$(realpath $(dirname $0))
CONFIGS=$ROOT/configs
cd /home/atopile

# APT SETUP ----------------------------------------------------------------

# update mirrors
sudo apt update
# install uv
which uv || {
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
}

# PYTHON -------------------------------------------------------------------
cd nonos_server
if [ ! -d .venv_pi ]; then
    uv venv .venv_pi
fi
source .venv_pi/bin/activate
uv pip install -e .
cd /home/atopile




# PACKAGES -----------------------------------------------------------------
sudo apt update
xargs -a $CONFIGS/packages.txt sudo apt install -y --no-upgrade

# spotifyd
if [ ! -f /home/atopile/spotifyd ]; then
    wget https://github.com/Spotifyd/spotifyd/releases/download/v0.4.1/spotifyd-linux-aarch64-full.tar.gz
    tar -xzf spotifyd-linux-aarch64-full.tar.gz
    rm spotifyd-linux-aarch64-full.tar.gz
    chmod +x spotifyd
fi

# shairplay
which shairplay || {
    git clone https://github.com/juhovh/shairplay.git
    cd shairplay
    ./autogen.sh
    ./configure
    make
    sudo make install
}

# CONFIG -------------------------------------------------------------------
sudo cp $CONFIGS/config.txt /boot/firmware/config.txt
sudo cp $CONFIGS/bluetooth_main.conf /etc/bluetooth/main.conf

mkdir -p /home/atopile/.vnc
cp $CONFIGS/vnc/passwd /home/atopile/.vnc/passwd


# setup autologin with linger
sudo loginctl enable-linger atopile

# SERVICES -----------------------------------------------------------------

DIR=$ROOT/services
ENABLE="y"
RESTART="n"

mkdir -p /home/atopile/.config/systemd/user
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