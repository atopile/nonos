# TCP-I2C Bridge

Modern Python implementation of TCP-I2C adapter with low-latency focus, comprehensive logging, and protocol dumping capabilities.

## Features

- **Modern Python Architecture**: Built with Python 3.11+, using modern libraries like `typer`, `structlog`, `pydantic`, and `asyncio`
- **Low-latency Design**: Async TCP server with `TCP_NODELAY` for minimal latency
- **Protocol Compatibility**: Fully compatible with the original C implementation
- **Comprehensive Logging**: Structured logging with rich console output
- **Protocol Dumping**: Dumps all network and I2C layer transactions to files
- **Multiple Backends**: Debug backend for testing, SMBus backend for hardware
- **Well-tested**: Comprehensive test suite with pytest and pytest-asyncio

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd sigma_tcp

# Install with uv (recommended)
uv sync --dev

# Or install with pip
pip install -e .
```

## Usage

### Debug Mode (No Hardware Required)

```bash
# Start debug server on default port 8086
tcp-i2c-bridge debug

# Start on specific port with debug logging
tcp-i2c-bridge debug --port 8087 --log-level DEBUG

# Enable protocol dumping
tcp-i2c-bridge debug --dump-dir ./protocol_dumps
```

### Hardware Mode (I2C Device Required)

```bash
# Connect to I2C device at address 0x48 on bus 1
tcp-i2c-bridge i2c 1 0x48

# With custom host and port
tcp-i2c-bridge i2c 1 0x48 --host 192.168.1.100 --port 8086
```

### CLI Options

```bash
# Show help
tcp-i2c-bridge --help

# Test protocol implementation
tcp-i2c-bridge test-protocol

# Show version
tcp-i2c-bridge version
```

## Protocol Specification

The TCP-I2C bridge implements a simple binary protocol:

### Header Format (8 bytes)
```
[command][total_len_hi][total_len_lo][reserved][len_hi][len_lo][addr_hi][addr_lo]
```

### Commands
- `0x0A` - READ: Read data from I2C device
- `0x0B` - WRITE: Write data to I2C device

### Read Request
```
Header: [0x0A][0x00][0x08][0x00][len_hi][len_lo][addr_hi][addr_lo]
```

### Write Request
```
Header: [0x0B][total_len_hi][total_len_lo][0x00][len_hi][len_lo][addr_hi][addr_lo]
Data: [data_bytes...]
```

### Read Response
```
Header: [0x0B][total_len_hi][total_len_lo][0x00][len_hi][len_lo][0x00][0x00]
Status: [status_byte]
Data: [data_bytes...]
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   TCP Client    │◄──►│   TCP Server    │◄──►│   I2C Backend   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Protocol Dumper │
                    └─────────────────┘
```

### Key Components

- **TCP Server**: Async TCP server handling multiple concurrent connections
- **Protocol Handler**: Parses and validates TCP-I2C protocol packets
- **I2C Backend**: Abstraction layer for I2C communication
  - `SMBusI2CBackend`: Real hardware using Linux I2C subsystem
  - `DebugI2CBackend`: Simulated memory for testing
- **Protocol Dumper**: Logs all network and I2C transactions to files
- **Structured Logging**: Rich console output with file logging support

## Testing

```bash
# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/test_protocol.py      # Protocol tests
uv run pytest tests/test_i2c_backend.py   # I2C backend tests
uv run pytest tests/test_integration.py   # Integration tests

# Run with coverage
uv run pytest --cov=tcp_i2c_bridge
```

## Development

### Project Structure
```
src/tcp_i2c_bridge/
├── __init__.py          # Package initialization
├── app.py               # Main application class
├── cli.py               # Typer CLI interface
├── i2c_backend.py       # I2C backend implementations
├── logging_config.py    # Logging configuration
├── protocol.py          # Protocol definitions
├── protocol_dumper.py   # Protocol dumping functionality
└── server.py            # TCP server implementation

tests/
├── test_protocol.py     # Protocol unit tests
├── test_i2c_backend.py  # I2C backend tests
├── test_server.py       # Server tests
└── test_integration.py  # Integration tests
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff src/ tests/

# Type checking
uv run mypy src/
```

## Protocol Dumping

When enabled, the bridge creates detailed logs of all communication:

```
dumps/
└── session_20250711_114427/
    ├── network/          # Binary network packets
    ├── i2c/              # Binary I2C transactions
    ├── network.log       # Network layer log
    ├── i2c.log           # I2C layer log
    └── summary.txt       # Session summary
```

## Performance Characteristics

- **Latency**: Sub-millisecond response times with TCP_NODELAY
- **Throughput**: Supports concurrent connections with asyncio
- **Memory**: Minimal memory footprint with efficient buffering
- **Scalability**: Handles multiple simultaneous I2C operations

## Compatibility

- **Python**: 3.11+ required
- **Operating System**: Linux (for hardware I2C access)
- **I2C Devices**: Compatible with standard Linux I2C subsystem (`/dev/i2c-*`)
- **Protocol**: 100% compatible with original C implementation

## Example Client Code

```python
import socket
import struct

# Connect to bridge
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8086))

# Write 4 bytes to address 0x1000
write_header = struct.pack(">BHHBBH", 0x0B, 12, 0, 0, 4, 0x1000)
write_data = b"test"
sock.send(write_header + write_data)

# Read 4 bytes from address 0x1000
read_header = struct.pack(">BHHBBH", 0x0A, 8, 0, 0, 4, 0x1000)
sock.send(read_header)

# Receive response
response = sock.recv(1024)
# Parse response...

sock.close()
```

## License

This project maintains compatibility with the original C implementation's licensing terms.