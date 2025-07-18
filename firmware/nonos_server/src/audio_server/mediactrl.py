import asyncio
import json
import socket
import subprocess

from dbus_next import BusType
from dbus_next.aio import MessageBus


async def find_mpris_services():
    bus = await MessageBus(bus_type=BusType.SESSION).connect()
    introspection = await bus.introspect(
        "org.freedesktop.DBus", "/org/freedesktop/DBus"
    )
    dbus_proxy = bus.get_proxy_object(
        "org.freedesktop.DBus", "/org/freedesktop/DBus", introspection
    )
    dbus = dbus_proxy.get_interface("org.freedesktop.DBus")

    names = await dbus.call_list_names()
    mpris_services = [
        name for name in names if name.startswith("org.mpris.MediaPlayer2.")
    ]

    return mpris_services


async def for_all_mpris_services(func):
    bus = await MessageBus(bus_type=BusType.SESSION).connect()
    for service in await find_mpris_services():
        PATH = "/org/mpris/MediaPlayer2"
        proxy = await bus.introspect(service, PATH)
        player = bus.get_proxy_object(service, PATH, proxy)
        interface = player.get_interface("org.mpris.MediaPlayer2.Player")
        await func(interface)


async def a_play_pause():
    await for_all_mpris_services(lambda interface: interface.call_play_pause())


async def a_next():
    await for_all_mpris_services(lambda interface: interface.call_next())


async def a_previous():
    await for_all_mpris_services(lambda interface: interface.call_previous())


MPV_SOCKET = None
mpv_proc = None


def play_mpv():
    global MPV_SOCKET, mpv_proc
    # mpv --input-ipc-server=/tmp/mpvsocket somefile.mp3
    MPV_SOCKET = "/tmp/mpv_socket"
    mpv_proc = subprocess.Popen(
        [
            "mpv",
            "--volume=70",
            "--no-video",
            "--loop-playlist=inf",
            "--input-ipc-server=" + MPV_SOCKET,
            "/home/atopile/yearmix2024.mp3",
            "/home/atopile/yearmix2023.mp3",
        ]
    )


def close_mpv():
    global mpv_proc
    if mpv_proc is not None:
        mpv_proc.terminate()
        mpv_proc = None


def _send_mpv_command(command):
    assert MPV_SOCKET is not None
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(MPV_SOCKET)
    msg = json.dumps({"command": command})
    sock.send((msg + "\n").encode("utf-8"))
    response = sock.recv(4096)
    sock.close()
    return json.loads(response)


def play_pause_track():
    if MPV_SOCKET is not None:
        _send_mpv_command(["cycle", "pause"])
        return

    asyncio.run(a_play_pause())


def next_track():
    if MPV_SOCKET is not None:
        # _send_mpv_command(["playlist-next", "force"])
        _send_mpv_command(["seek", 60, "relative"])
        return

    asyncio.run(a_next())


def previous_track():
    if MPV_SOCKET is not None:
        # _send_mpv_command(["playlist-prev", "force"])
        _send_mpv_command(["seek", -60, "relative"])
        return

    asyncio.run(a_previous())


if __name__ == "__main__":
    play_pause_track()
