"""Command-line interface for TCP-I2C bridge."""

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from tcp_i2c_bridge.app import TCPBridgeApp

console = Console()
app = typer.Typer(
    name="tcp-i2c-bridge",
    help="Modern TCP-I2C bridge with low-latency focus",
    no_args_is_help=True,
)


@app.command()
def debug(
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="Host to bind TCP server to"
    ),
    port: int = typer.Option(8086, "--port", "-p", help="Port to bind TCP server to"),
    dump_dir: Path | None = typer.Option(
        None, "--dump-dir", "-d", help="Directory to dump protocol logs"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    ),
    log_file: Path | None = typer.Option(None, "--log-file", help="Log file path"),
    json_logs: bool = typer.Option(
        False, "--json-logs", help="Use JSON format for logs"
    ),
) -> None:
    """Run TCP-I2C bridge with debug backend (no hardware required)."""

    console.print(
        Panel(
            Text("TCP-I2C Bridge - Debug Mode", style="bold green"),
            subtitle="Using simulated I2C memory for testing",
        )
    )

    bridge_app = TCPBridgeApp.create_with_debug_backend(
        host=host,
        port=port,
        dump_dir=dump_dir,
        log_level=log_level,
        log_file=log_file,
        json_logs=json_logs,
    )

    try:
        asyncio.run(bridge_app.run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def i2c(
    i2c_bus: int = typer.Argument(..., help="I2C bus number (e.g., 1 for /dev/i2c-1)"),
    device_addr: str = typer.Argument(
        ..., help="I2C device address (e.g., 0x48 or 72)"
    ),
    host: str = typer.Option(
        "0.0.0.0", "--host", "-h", help="Host to bind TCP server to"
    ),
    port: int = typer.Option(8086, "--port", "-p", help="Port to bind TCP server to"),
    dump_dir: Path | None = typer.Option(
        None, "--dump-dir", "-d", help="Directory to dump protocol logs"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", "-l", help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    ),
    log_file: Path | None = typer.Option(None, "--log-file", help="Log file path"),
    json_logs: bool = typer.Option(
        False, "--json-logs", help="Use JSON format for logs"
    ),
) -> None:
    """Run TCP-I2C bridge with hardware I2C backend."""

    # Parse device address
    try:
        if device_addr.startswith("0x") or device_addr.startswith("0X"):
            device_addr_int = int(device_addr, 16)
        else:
            device_addr_int = int(device_addr)
    except ValueError as e:
        console.print(f"[red]Invalid device address: {device_addr}[/red]")
        raise typer.Exit(1) from e

    if not (0 <= device_addr_int <= 0x7F):
        console.print(
            f"[red]Device address out of range: 0x{device_addr_int:02X}[/red]"
        )
        raise typer.Exit(1)

    console.print(
        Panel(
            Text("TCP-I2C Bridge - Hardware Mode", style="bold blue"),
            subtitle=f"Using I2C bus {i2c_bus}, device 0x{device_addr_int:02X}",
        )
    )

    try:
        bridge_app = TCPBridgeApp.create_with_i2c_backend(
            i2c_bus=i2c_bus,
            device_addr=device_addr_int,
            host=host,
            port=port,
            dump_dir=dump_dir,
            log_level=log_level,
            log_file=log_file,
            json_logs=json_logs,
        )

        asyncio.run(bridge_app.run())

    except FileNotFoundError as e:
        console.print(f"[red]I2C device not found: {e}[/red]")
        raise typer.Exit(1) from e
    except PermissionError as e:
        console.print(f"[red]Permission denied: {e}[/red]")
        console.print("[yellow]Try running with sudo or add user to i2c group[/yellow]")
        raise typer.Exit(1) from e
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down...[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def version() -> None:
    """Show version information."""
    from tcp_i2c_bridge import __version__

    console.print(f"TCP-I2C Bridge version {__version__}")
    console.print("Built with modern Python for low-latency I2C access")


@app.command()
def test_protocol() -> None:
    """Test protocol implementation without hardware."""
    from tcp_i2c_bridge.protocol import ProtocolHeader, ReadRequest, WriteRequest

    console.print(Panel("Protocol Test", style="bold cyan"))

    # Test read request
    read_req = ReadRequest(addr=0x1000, len=16)
    header = read_req.to_header()
    packed = header.pack()
    unpacked = ProtocolHeader.unpack(packed)

    console.print(f"Read Request: addr=0x{read_req.addr:04X}, len={read_req.len}")
    console.print(f"Packed: {packed.hex()}")
    console.print(f"Unpacked: {unpacked}")

    # Test write request
    write_req = WriteRequest(addr=0x2000, data=b"Hello")
    header = write_req.to_header()
    packed = header.pack()
    unpacked = ProtocolHeader.unpack(packed)

    console.print(
        f"\nWrite Request: addr=0x{write_req.addr:04X}, data={write_req.data}"
    )
    console.print(f"Packed: {packed.hex()}")
    console.print(f"Unpacked: {unpacked}")

    console.print("\n[green]Protocol test completed successfully![/green]")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
