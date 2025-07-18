# Setup

```bash
# rsync nonos_server to nonos
rsync -a nonos_server nonos:
ssh nonos "cd nonos_server && ./setup.sh"
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
- vnc stuff, see setup.sh (needs manual vncpasswd set)

# NOTES

- want usb bt dongle
- undervoltages
