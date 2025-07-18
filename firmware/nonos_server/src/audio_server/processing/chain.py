import subprocess
import time
from pathlib import Path

from audio_server.processing.model import (
    Graph,
    Highpass,
    Limiter,
    Lowpass,
    MidSide,
    MultibandEQ,
    make_chain,
)

# -------------------------- Example ------------------------

CHAIN_CONF = (Path(__file__).parent / "chain.conf").resolve().absolute()

OUT_GAIN = -6.0


def setup_filter_chain():
    SOLO = [
        True,
        True,
    ]

    eqs = [
        MultibandEQ(
            name=f"masterEQ_{c}",
            gain____50hz=3.0,
            gain___100hz=9.0,
            gain___156hz=6.0,
            gain___220hz=1.0,
            gain___311hz=-5.0,
            gain___440hz=-10.0,
            gain___622hz=-7.0,
            gain___880hz=-10.0,
            gain__1250hz=-9.0,
            gain__1750hz=-10.0,
            gain__2500hz=-8.0,
            gain__3500hz=-6.0,
            gain__5000hz=-7.0,
            gain_10000hz=-2.0,
            gain_20000hz=-3.0,
        )
        for c in ["L", "R"]
    ]
    ms = MidSide(name="downmix")
    lp = Lowpass(name="lowpass", cutoff_frequency=2500, stages=4)
    hp = Highpass(name="highpass", cutoff_frequency=2500, stages=4)
    pre_hp_low = Highpass(name="pre_hp_low", cutoff_frequency=38, stages=4)
    pre_lp_high = Lowpass(name="pre_lp_high", cutoff_frequency=20000, stages=4)
    input_limiter = Limiter(
        name="inputLim", input_gain=-11.0, limit=-1.0, release_time=0.05
    )

    low_eq = MultibandEQ(
        name="lowEQ",
        gain____50hz=10.0,
        gain___880hz=12.0,
        gain__1250hz=15.0,
    )
    high_eq = MultibandEQ(
        name="highEQ",
        gain__2500hz=-7.0,
        gain__3500hz=-5.0,
        gain__5000hz=2.0,
        gain_10000hz=10.0,
        gain_20000hz=15.0,
    )
    lim_high = Limiter(
        name="highLim",
        input_gain=-7.0 + OUT_GAIN if SOLO[1] else -100.0,
        limit=0.0,
        release_time=5,
    )
    lim_low = Limiter(
        name="lowLim",
        input_gain=0.0 + OUT_GAIN if SOLO[0] else -100.0,
        limit=0.0,
        release_time=5,
    )

    # valve = Valve(name="valve", distortion_level=0.1, distortion_character=0.2)

    G = Graph()
    G.connect(
        input_limiter.input1,
        input_limiter.output1,
        eqs[0],
        ms.left,
        root_input=[0],
    )
    G.connect(
        input_limiter.input2,
        input_limiter.output2,
        eqs[1],
        ms.right,
        root_input=[1],
    )
    common_chain = ms.mid
    G.connect(
        common_chain,
        pre_hp_low,
        lp,
        low_eq,
        # valve,
        lim_low.input1,
        lim_low.output1,
        root_output=[0],
    )
    G.connect(
        common_chain,
        pre_lp_high,
        hp,
        high_eq,
        lim_high.input1,
        lim_high.output1,
        root_output=[1],
    )

    chain = make_chain(G, "Speaker-Master")
    CHAIN_CONF.write_text(chain, encoding="utf-8")


def enable_filter_chain():
    print("Setting up filter chain")
    setup_filter_chain()

    subprocess.check_output(
        ["sudo", "mkdir", "-p", "/etc/pipewire/filter-chain.conf.d"],
        stderr=subprocess.STDOUT,
    )

    target = "/etc/pipewire/filter-chain.conf.d/chain.conf"
    if not Path(target).exists():
        subprocess.check_output(
            [
                "sudo",
                "ln",
                "-s",
                CHAIN_CONF,
                target,
            ],
        )

    subprocess.check_output(["systemctl", "--user", "restart", "filter-chain.service"])
    time.sleep(2)

    try:
        print("Setting default audio chain")
        subprocess.check_output(
            Path(__file__).parent / "set_default.sh", stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"Failed to set default audio chain: <{e.output.decode('utf-8')}>"
        ) from e


if __name__ == "__main__":
    enable_filter_chain()
