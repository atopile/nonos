"""Tests for I2C backend implementations."""

from unittest.mock import Mock, patch

import pytest

from tcp_i2c_bridge.i2c_backend import DebugI2CBackend, SMBusI2CBackend


class TestDebugI2CBackend:
    """Test debug I2C backend."""

    def test_init(self):
        """Test backend initialization."""
        backend = DebugI2CBackend(memory_size=512)
        assert len(backend.memory) == 512
        assert backend.base_addr == 0x4000

    def test_read_in_range(self):
        """Test reading data in range."""
        backend = DebugI2CBackend()

        # Write some data first
        addr = 0x4010
        test_data = b"test_data"
        backend.write(addr, test_data)

        # Read it back
        read_data = backend.read(addr, len(test_data))
        assert read_data == test_data

    def test_read_out_of_range(self):
        """Test reading data out of range."""
        backend = DebugI2CBackend()

        # Read from below base address
        data = backend.read(0x1000, 4)
        assert data == b"\x00\x00\x00\x00"

        # Read from above memory range
        data = backend.read(0x5000, 4)
        assert data == b"\x00\x00\x00\x00"

    def test_write_in_range(self):
        """Test writing data in range."""
        backend = DebugI2CBackend()

        addr = 0x4020
        test_data = b"hello"
        backend.write(addr, test_data)

        # Verify data was written
        offset = addr - backend.base_addr
        assert backend.memory[offset : offset + len(test_data)] == test_data

    def test_write_out_of_range(self):
        """Test writing data out of range."""
        backend = DebugI2CBackend()

        # Should not crash
        backend.write(0x1000, b"test")
        backend.write(0x5000, b"test")

    def test_close(self):
        """Test closing backend."""
        backend = DebugI2CBackend()
        # Should not raise exception
        backend.close()


class TestSMBusI2CBackend:
    """Test SMBus I2C backend."""

    def test_init_invalid_device_address(self):
        """Test initialization with invalid device address."""
        with pytest.raises(ValueError, match="Invalid I2C device address"):
            SMBusI2CBackend(1, 0x80)  # Address too high

        with pytest.raises(ValueError, match="Invalid I2C device address"):
            SMBusI2CBackend(1, -1)  # Negative address

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    def test_init_missing_device(self, mock_path):
        """Test initialization with missing I2C device."""
        mock_path.return_value.exists.return_value = False

        with pytest.raises(FileNotFoundError, match="I2C device not found"):
            SMBusI2CBackend(1, 0x48)

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_init_success(self, mock_smbus, mock_path):
        """Test successful initialization."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)

        assert backend.i2c_bus == 1
        assert backend.device_addr == 0x48
        assert backend.bus is mock_bus
        mock_smbus.assert_called_once_with(1)

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_connect_failure(self, mock_smbus, mock_path):
        """Test connection failure."""
        mock_path.return_value.exists.return_value = True
        mock_smbus.side_effect = Exception("Connection failed")

        with pytest.raises(RuntimeError, match="Failed to open I2C bus"):
            SMBusI2CBackend(1, 0x48)

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_read_small_data(self, mock_smbus, mock_path):
        """Test reading small amount of data."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)

        # Mock the read message
        mock_read_msg = Mock()
        mock_read_msg.__iter__ = Mock(return_value=iter([0x01, 0x02, 0x03, 0x04]))

        with patch("tcp_i2c_bridge.i2c_backend.smbus2.i2c_msg.write"):
            with patch(
                "tcp_i2c_bridge.i2c_backend.smbus2.i2c_msg.read",
                return_value=mock_read_msg,
            ):
                data = backend.read(0x1000, 4)

        assert data == b"\x01\x02\x03\x04"
        mock_bus.i2c_rdwr.assert_called_once()

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_read_invalid_length(self, mock_smbus, mock_path):
        """Test reading with invalid length."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)

        with pytest.raises(ValueError, match="Read length must be positive"):
            backend.read(0x1000, 0)

        with pytest.raises(ValueError, match="Read length must be positive"):
            backend.read(0x1000, -1)

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_read_no_connection(self, mock_smbus, mock_path):
        """Test reading without connection."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)
        backend.bus = None  # Simulate no connection

        with pytest.raises(RuntimeError, match="I2C bus not connected"):
            backend.read(0x1000, 4)

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_write_small_data(self, mock_smbus, mock_path):
        """Test writing small amount of data."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)

        with patch("tcp_i2c_bridge.i2c_backend.smbus2.i2c_msg.write"):
            backend.write(0x1000, b"test")

        mock_bus.i2c_rdwr.assert_called_once()

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_write_empty_data(self, mock_smbus, mock_path):
        """Test writing empty data."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)

        with pytest.raises(ValueError, match="Write data cannot be empty"):
            backend.write(0x1000, b"")

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_write_no_connection(self, mock_smbus, mock_path):
        """Test writing without connection."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)
        backend.bus = None  # Simulate no connection

        with pytest.raises(RuntimeError, match="I2C bus not connected"):
            backend.write(0x1000, b"test")

    @patch("tcp_i2c_bridge.i2c_backend.Path")
    @patch("tcp_i2c_bridge.i2c_backend.smbus2.SMBus")
    def test_close(self, mock_smbus, mock_path):
        """Test closing backend."""
        mock_path.return_value.exists.return_value = True
        mock_bus = Mock()
        mock_smbus.return_value = mock_bus

        backend = SMBusI2CBackend(1, 0x48)
        backend.close()

        mock_bus.close.assert_called_once()
        assert backend.bus is None
