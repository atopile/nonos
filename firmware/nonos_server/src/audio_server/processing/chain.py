import subprocess
from pathlib import Path

from audio_server.processing.model import (
    EQ,
    Graph,
    Highpass,
    Limiter,
    Lowpass,
    MidSide,
    MultibandEQ,
    Valve,
    make_chain,
)

# -------------------------- Example ------------------------


def setup_filter_chain():
    CROSSOVER_FREQ = 1500

    SOLO = [
        True,
        True,
    ]

    eqs = [
        MultibandEQ(
            name=f"masterEQ_{c}",
            gain_50hz=10.0,
            gain_100hz=3.0,
            gain_156hz=-6.0,
            gain_220hz=-6.0,
            gain_311hz=-6.0,
            gain_440hz=-6.0,
            gain_622hz=-6.0,
            gain_880hz=-6.0,
            gain_1250hz=-6.0,
            gain_1750hz=-3.0,
            gain_2500hz=-3.0,
            gain_3500hz=0.0,
            gain_5000hz=0.0,
            gain_10000hz=1.0,
            gain_20000hz=2.0,
        )
        for c in ["L", "R"]
    ]
    ms = MidSide(name="downmix")
    lp = Lowpass(name="lowpass", cutoff_frequency=CROSSOVER_FREQ)
    hp = Highpass(name="highpass", cutoff_frequency=CROSSOVER_FREQ)
    low_eq = EQ(name="lowEQ")
    high_eq = EQ(name="highEQ")
    lim_high = Limiter(
        name="highLim",
        input_gain=0.0 if SOLO[1] else -100.0,
        limit=-1.0,
        release_time=0.05,
    )
    lim_low = Limiter(
        name="lowLim",
        input_gain=0.0 if SOLO[0] else -100.0,
        limit=-1.0,
        release_time=0.05,
    )

    valve = Valve(name="valve", distortion_level=0.5, distortion_character=0.5)

    G = Graph()
    G.connect(eqs[0], ms.left, root_input=[0])
    G.connect(eqs[1], ms.right, root_input=[1])
    G.connect(
        ms.mid,
        lp,
        low_eq,
        valve,
        lim_low.input1,
        lim_low.output1,
        root_output=[0],
    )
    G.connect(
        ms.mid,
        hp,
        high_eq,
        lim_high.input1,
        lim_high.output1,
        root_output=[1],
    )

    chain = make_chain(G, "Speaker-Master")
    (Path(__file__).parent / "chain.conf").write_text(chain, encoding="utf-8")


def enable_filter_chain():
    setup_filter_chain()

    try:
        subprocess.check_output(
            Path(__file__).parent / "set_default.sh", stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"Failed to set default audio chain: <{e.output.decode('utf-8')}>"
        ) from e


if __name__ == "__main__":
    enable_filter_chain()
