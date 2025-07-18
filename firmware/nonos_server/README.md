# Setup

```bash
# rsync nonos_server to nonos
rsync -a nonos_server/ nonos:
```

```bash
# update mirrors
sudo apt update
# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# install nonos_server
cd nonos_server
uv venv .venv_pi
source .venv_pi/bin/activate
uv pip install -e .
```

/boot/firmware/config.txt

```
dtoverlay=i2s-mmap
dtoverlay=googlevoicehat-soundcard
dtparam=i2s=on

#dtparam=audio=on
dtoverlay=vc4-kms-v3d,noaudio

# enable DSP
dtparam=i2s_vc=on
gpio=20=op,dh
```

## Bluetooth

Enable `FastConnectable=y` in `/etc/bluetooth/main.conf`
Make pairable and trust all devices:

Not sure about those:

```
[General]
AutoEnable=true
Class = 0x200414
DiscoverableTimeout = 0
PairableTimeout = 0
JustWorksRepairing = always
```

## Packages

TODO

- pipewire setup
- spotifyd
- shairplay
- ...

## Services

```bash
./nonos_server/make_symlinks.sh
```

# Test

```bash
speaker-test -Dasymed -c2 -t sine -f 1000 -F S32_LE
```

## Touch

- builtin driver (hat.dts) does not register key presses
- seems to be related to calibration not working
- multitouch does not work

# Broken

- bluetooth only works after login with ssh

# NOTES

- want usb bt dongle
- undervoltages
