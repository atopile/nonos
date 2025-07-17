from dataclasses import dataclass, field, fields
from textwrap import indent
from typing import Literal, TypeVar


@dataclass(kw_only=True)
class Channel:
    name: str
    direction: str
    _parent: "Node | None" = None

    def __post_init__(self):
        assert self.direction in ("in", "out")

    @property
    def parent(self):
        assert self._parent is not None
        return self._parent

    @property
    def full_name(self):
        return f"{self.parent.name}:{self.name}"


def lit(val: str | float | int):
    return f'"{val}"' if isinstance(val, str) else repr(val)


@dataclass(kw_only=True)
class Node:
    name: str
    type: str = "ladspa"
    plugin: str | None = None
    label: str | None = None
    control: dict[str, float | int] | None = None

    _channels: list[Channel] = field(default_factory=list)

    def __post_init__(self):
        assert self.plugin is not None
        assert self.label is not None
        self.plugin = f"/usr/lib/ladspa/{self.plugin}.so"

        node_fields = {f.name for f in fields(Node)}
        control_fields = {f for f in fields(self) if f.name not in node_fields}

        self.control = {}
        for f in control_fields:
            val = getattr(self, f.name)
            if isinstance(val, Channel):
                val._parent = self
                self._channels.append(val)
            else:
                self.control[f.metadata["label"]] = val

    def to_config(self) -> str:
        node_fields = fields(Node)

        out = ""
        for k in node_fields:
            if k.name.startswith("_"):
                continue
            val = getattr(self, k.name)
            if isinstance(val, dict):
                val = (
                    "{\n  "
                    + "\n  ".join(f'"{k}" = {lit(v)}' for k, v in val.items())
                    + "\n}"
                )
            else:
                val = lit(val)
            out += f"\n{k.name} = {val} "
        out = "{" + indent(out, "  ") + "\n}"

        return out

    def get_input(self) -> Channel:
        inputs = [c for c in self._channels if c.direction == "in"]
        assert len(inputs) == 1
        return inputs[0]

    def get_output(self) -> Channel:
        outputs = [c for c in self._channels if c.direction == "out"]
        assert len(outputs) == 1
        return outputs[0]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: "Node"):
        return self.name == other.name


@dataclass(kw_only=True)
class Link:
    output: Channel
    input: Channel

    def to_config(self) -> str:
        return (
            "{ "
            + f'output = "{self.output.full_name}" input = "{self.input.full_name}"'
            + " }"
        )


class Graph:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.links: list[Link] = []
        self.inputs: list[Channel | None] = [None, None]
        self.outputs: list[Channel | None] = [None, None]

    def connect(
        self,
        *channels: Channel | Node,
        root_input: list[Literal[0, 1]] | None = None,
        root_output: list[Literal[0, 1]] | None = None,
    ):
        real_channels: list[Channel] = []
        for c in channels:
            if isinstance(c, Channel):
                real_channels.append(c)
            else:
                real_channels.append(c.get_input())
                real_channels.append(c.get_output())

        for c in real_channels:
            self.nodes[c.parent.name] = c.parent

        if not real_channels:
            return

        last = real_channels[0]
        if root_input is not None:
            for i in root_input:
                self.inputs[i] = real_channels[0]

        for c in real_channels[1:]:
            assert last.direction != c.direction
            if c.parent != last.parent:
                self.links.append(Link(output=last, input=c))
            last = c

        if root_output is not None:
            for i in root_output:
                self.outputs[i] = last

    def to_config(self) -> str:
        out = ""

        out += "nodes = [\n"
        for n in self.nodes.values():
            out += indent(n.to_config(), "  ") + "\n"
        out += "]"

        assert all(i is not None for i in self.inputs)
        assert all(i is not None for i in self.outputs)
        out += "\ninputs = [" + ", ".join(lit(i.full_name) for i in self.inputs) + "]"  # type: ignore
        out += (
            "\noutputs = [" + ", ".join(lit(i.full_name) for i in self.outputs) + "]"  # type: ignore
        )

        out += "\nlinks = [\n"
        for link in self.links:
            out += indent(link.to_config(), "  ") + "\n"
        out += "]"

        out = "{\n" + indent(out, "  ") + "\n}"
        return out


T = TypeVar("T")


def f(label: str, default: T = 0) -> T:
    return field(default=default, metadata={"label": label})


def c_in(name: str):
    return field(default_factory=lambda: Channel(name=name, direction="in"))


def c_out(name: str):
    return field(default_factory=lambda: Channel(name=name, direction="out"))


# -------------------------- Nodes --------------------------


@dataclass(kw_only=True)
class EQ(Node):
    plugin: str = "triple_para_1204"
    label: str = "triplePara"

    low_shelving_gain: float = f("Low-shelving gain (dB)")
    low_shelving_frequency: float = f("Low-shelving frequency (Hz)")
    low_shelving_slope: float = f("Low-shelving slope")
    band_1_gain: float = f("Band 1 gain (dB)")
    band_1_frequency: float = f("Band 1 frequency (Hz)")
    band_1_bandwidth: float = f("Band 1 bandwidth (octaves)")
    band_2_gain: float = f("Band 2 gain (dB)")
    band_2_frequency: float = f("Band 2 frequency (Hz)")
    band_2_bandwidth: float = f("Band 2 bandwidth (octaves)")
    band_3_gain: float = f("Band 3 gain (dB)")
    band_3_frequency: float = f("Band 3 frequency (Hz)")
    band_3_bandwidth: float = f("Band 3 bandwidth (octaves)")
    high_shelving_gain: float = f("High-shelving gain (dB)")
    high_shelving_frequency: float = f("High-shelving frequency (Hz)")
    high_shelving_slope: float = f("High-shelving slope")

    input: Channel = c_in("Input")
    output: Channel = c_out("Output")


@dataclass(kw_only=True)
class MultibandEQ(Node):
    plugin: str = "mbeq_1197"
    label: str = "mbeq"

    gain_50hz: float = f("50Hz gain (low shelving)")
    gain_100hz: float = f("100Hz gain")
    gain_156hz: float = f("156Hz gain")
    gain_220hz: float = f("220Hz gain")
    gain_311hz: float = f("311Hz gain")
    gain_440hz: float = f("440Hz gain")
    gain_622hz: float = f("622Hz gain")
    gain_880hz: float = f("880Hz gain")
    gain_1250hz: float = f("1250Hz gain")
    gain_1750hz: float = f("1750Hz gain")
    gain_2500hz: float = f("2500Hz gain")
    gain_3500hz: float = f("3500Hz gain")
    gain_5000hz: float = f("5000Hz gain")
    gain_10000hz: float = f("10000Hz gain")
    gain_20000hz: float = f("20000Hz gain")

    input: Channel = c_in("Input")
    output: Channel = c_out("Output")


@dataclass(kw_only=True)
class Limiter(Node):
    plugin: str = "fast_lookahead_limiter_1913"
    label: str = "fastLookaheadLimiter"

    input_gain: float = f("Input gain (dB)")
    limit: float = f("Limit (dB)")
    release_time: float = f("Release time (s)")

    input1: Channel = c_in("Input 1")
    input2: Channel = c_in("Input 2")
    output1: Channel = c_out("Output 1")
    output2: Channel = c_out("Output 2")


@dataclass(kw_only=True)
class Lowpass(Node):
    plugin: str = "lowpass_iir_1891"
    label: str = "lowpass_iir"

    cutoff_frequency: float = f("Cutoff Frequency", 20000)
    # stages: int = f("Stages(2 poles per stage)", 1)

    input: Channel = c_in("Input")
    output: Channel = c_out("Output")


@dataclass(kw_only=True)
class Highpass(Node):
    plugin: str = "highpass_iir_1890"
    label: str = "highpass_iir"

    cutoff_frequency: float = f("Cutoff Frequency")
    # stages: int = f("Stages(2 poles per stage)", 1)

    input: Channel = c_in("Input")
    output: Channel = c_out("Output")


@dataclass(kw_only=True)
class MidSide(Node):
    plugin: str = "matrix_st_ms_1420"
    label: str = "matrixStMS"

    left: Channel = c_in("Left")
    right: Channel = c_in("Right")
    mid: Channel = c_out("Mid")
    side: Channel = c_out("Side")


@dataclass(kw_only=True)
class Valve(Node):
    plugin: str = "valve_1209"
    label: str = "valve"

    distortion_level: float = f("Distortion level")
    distortion_character: float = f("Distortion character")

    input: Channel = c_in("Input")
    output: Channel = c_out("Output")


# -------------------------- Chain --------------------------
def make_chain(G: Graph, name: str):
    out = """

# This file is automatically generated by chain.py
context.modules = [
  { name = libpipewire-module-filter-chain
    args = {

      node.name        = "{name}-Chain"
      node.description = "{name}-Chain"
      media.name       = "{name}-Chain"

      audio.rate      = 48000
      audio.channels  = 2
      audio.position  = [ FL FR ]    # <-- enables capture_FL / playback_FL

      capture.props  = { node.name = "{name}-Input"  media.class = "Audio/Sink" }
      playback.props = { node.name = "{name}-Output" media.class = "Audio/Source"}

      filter.graph =
"""
    out = out.replace("{name}", name)

    out += indent(G.to_config(), "  " * 3)

    out += "\n    }\n  }\n]"

    return out
