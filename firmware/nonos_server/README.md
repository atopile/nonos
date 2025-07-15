## Enable I2S

/boot/firmware/config.txt

```
dtoverlay=i2s-mmap
dtoverlay=googlevoicehat-soundcard
dtparam=i2s=on

#dtparam=audio=on
```

/etc/asound.conf

```
options snd_rpi_googlemihat_soundcard index=0

pcm.spkvol {
    type            softvol
    slave.pcm       "dmix"
    control.name    "PCM"
    control.card    0
}

pcm.micboost {
    type            softvol
    slave.pcm       "dsnoop"
    control.name    "MIC"
    control.card    0
    min_dB      -10.0
    max_dB      18.0
}

pcm.asymed {
    type asym
    playback.pcm "spkvol"
    capture.pcm "micboost"
}

pcm.!default {
    type plug
    slave.pcm "asymed"
}
```

Test

32bit

```bash
speaker-test -Dasymed -c2 -t sine -f 1000 -F S32_LE
```

## Enable DSP

/boot/firmware/config.txt

```
dtparam=i2s_vc=on
gpio=20=op,dh
```

```bash
# backup, dt might not work
sudo pinctrl set 20 op
sudo pinctrl set 20 dh
```

Start TCP-I2C server

```bash
cd sigma_tcp
source .venv_pi/bin/activate
python src/tcp_i2c_bridge/main.py i2c 0 0x3b
```

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

# setup service
sudo ln -s /home/atopile/nonos_server/i2c_bridge.service /etc/systemd/system/i2c_bridge.service
sudo systemctl daemon-reload
sudo systemctl enable i2c_bridge.service
sudo systemctl start i2c_bridge.service
```

```bash
# prepare PD
# uncomment `stusb.nvm_write(nvm_custom)` in stusb4500.py
# uncomment `stusb.reset()` in stusb4500.py
# write nvm and reboot (done by next line)
python nonos_server/src/audio_server/stusb4500.py
```
