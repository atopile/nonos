"""I2C backend implementation for TCP-I2C bridge."""

from abc import ABC, abstractmethod
from pathlib import Path

import smbus2
import structlog

logger = structlog.get_logger()


class I2CBackend(ABC):
    """Abstract base class for I2C backends."""

    @abstractmethod
    def read(self, addr: int, length: int) -> bytes:
        """Read data from I2C device."""
        pass

    @abstractmethod
    def write(self, addr: int, data: bytes) -> None:
        """Write data to I2C device."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the I2C backend."""
        pass


class SMBusI2CBackend(I2CBackend):
    """I2C backend using SMBus/I2C-dev interface."""

    def __init__(self, i2c_bus: int | smbus2.SMBus, device_addr: int):
        """Initialize SMBus I2C backend.

        Args:
            i2c_bus: I2C bus number (e.g., 1 for /dev/i2c-1)
            device_addr: I2C device address (7-bit)
        """
        self.i2c_bus = i2c_bus
        self.device_addr = device_addr
        self.bus: smbus2.SMBus | None = None

        # Validate device address
        if not (0 <= device_addr <= 0x7F):
            raise ValueError(f"Invalid I2C device address: 0x{device_addr:02X}")

        if isinstance(i2c_bus, int):
            # Check if I2C device exists
            i2c_dev_path = Path(f"/dev/i2c-{i2c_bus}")
            if not i2c_dev_path.exists():
                raise FileNotFoundError(f"I2C device not found: {i2c_dev_path}")

            self._connect()
        else:
            self.bus = i2c_bus

        logger.info(
            "I2C backend initialized",
            bus=i2c_bus,
            device_addr=f"0x{device_addr:02X}",
            device_path=str(i2c_dev_path) if isinstance(i2c_bus, int) else None,
        )

    def _connect(self) -> None:
        """Connect to I2C bus."""
        assert isinstance(self.i2c_bus, int)
        try:
            self.bus = smbus2.SMBus(self.i2c_bus)
        except Exception as e:
            raise RuntimeError(f"Failed to open I2C bus {self.i2c_bus}: {e}") from e

    def read(self, addr: int, length: int) -> bytes:
        """Read data from I2C device using 16-bit register addressing.

        Args:
            addr: 16-bit register address
            length: Number of bytes to read

        Returns:
            Read data as bytes
        """
        if not self.bus:
            raise RuntimeError("I2C bus not connected")

        if length <= 0:
            raise ValueError("Read length must be positive")

        if length > 32:
            # SMBus has a 32-byte limit, use I2C block read for larger transfers
            return self._read_large(addr, length)

        try:
            # Use I2C write-read transaction for 16-bit addressing
            addr_bytes = [(addr >> 8) & 0xFF, addr & 0xFF]

            # Write register address, then read data
            write_msg = smbus2.i2c_msg.write(self.device_addr, addr_bytes)
            read_msg = smbus2.i2c_msg.read(self.device_addr, length)
            self.bus.i2c_rdwr(write_msg, read_msg)

            data = bytes(read_msg)
            logger.debug(
                "I2C read completed",
                addr=f"0x{addr:04X}",
                length=length,
                data=data.hex(),
            )
            return data

        except Exception as e:
            logger.error(
                "I2C read failed", addr=f"0x{addr:04X}", length=length, error=str(e)
            )
            raise RuntimeError(f"I2C read failed: {e}") from e

    def _read_large(self, addr: int, length: int) -> bytes:
        """Read large amounts of data using multiple transactions."""
        data = b""
        current_addr = addr
        remaining = length

        while remaining > 0:
            chunk_size = min(remaining, 32)
            chunk = self.read(current_addr, chunk_size)
            data += chunk
            current_addr += chunk_size
            remaining -= chunk_size

        return data

    def write(self, addr: int, data: bytes) -> None:
        """Write data to I2C device using 16-bit register addressing.

        Args:
            addr: 16-bit register address
            data: Data to write
        """
        if not self.bus:
            raise RuntimeError("I2C bus not connected")

        if len(data) == 0:
            raise ValueError("Write data cannot be empty")

        if len(data) > 30:  # 32 - 2 bytes for address
            # Split large writes into chunks
            self._write_large(addr, data)
            return

        try:
            # Combine address and data for single I2C transaction
            addr_bytes = [(addr >> 8) & 0xFF, addr & 0xFF]
            write_data = addr_bytes + list(data)

            write_msg = smbus2.i2c_msg.write(self.device_addr, write_data)
            self.bus.i2c_rdwr(write_msg)

            logger.debug(
                "I2C write completed",
                addr=f"0x{addr:04X}",
                length=len(data),
                data=data.hex(),
            )

        except Exception as e:
            logger.error(
                "I2C write failed",
                addr=f"0x{addr:04X}",
                length=len(data),
                data=data.hex(),
                error=str(e),
            )
            raise RuntimeError(f"I2C write failed: {e}") from e

    def _write_large(self, addr: int, data: bytes) -> None:
        """Write large amounts of data using multiple transactions."""
        offset = 0

        while offset < len(data):
            chunk_size = min(len(data) - offset, 30)  # 32 - 2 bytes for address
            chunk = data[offset : offset + chunk_size]
            self.write(addr + offset, chunk)
            offset += chunk_size

    def close(self) -> None:
        """Close the I2C bus connection."""
        if self.bus:
            self.bus.close()
            self.bus = None
            logger.info("I2C backend closed")


class DebugI2CBackend(I2CBackend):
    """Debug I2C backend for testing without hardware."""

    def __init__(self, memory_size: int = 256):
        """Initialize debug backend with simulated memory."""
        self.memory = bytearray(memory_size)
        self.base_addr = 0x4000
        logger.info("Debug I2C backend initialized", memory_size=memory_size)

    def read(self, addr: int, length: int) -> bytes:
        """Read from simulated memory."""
        if addr < self.base_addr or addr + length > self.base_addr + len(self.memory):
            # Return zeros for out-of-range addresses
            logger.debug("Debug read out of range", addr=f"0x{addr:04X}", length=length)
            return b"\x00" * length

        offset = addr - self.base_addr
        data = bytes(self.memory[offset : offset + length])

        logger.debug(
            "Debug read completed", addr=f"0x{addr:04X}", length=length, data=data.hex()
        )
        return data

    def write(self, addr: int, data: bytes) -> None:
        """Write to simulated memory."""
        if addr < self.base_addr or addr + len(data) > self.base_addr + len(
            self.memory
        ):
            logger.debug(
                "Debug write out of range", addr=f"0x{addr:04X}", length=len(data)
            )
            return

        offset = addr - self.base_addr
        self.memory[offset : offset + len(data)] = data

        logger.debug(
            "Debug write completed",
            addr=f"0x{addr:04X}",
            length=len(data),
            data=data.hex(),
        )

    def close(self) -> None:
        """Close debug backend."""
        logger.info("Debug I2C backend closed")
