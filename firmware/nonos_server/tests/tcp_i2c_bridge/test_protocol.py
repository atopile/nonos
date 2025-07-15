"""Tests for protocol implementation."""

import struct

import pytest

from tcp_i2c_bridge.protocol import (
    Command,
    ProtocolHeader,
    ReadRequest,
    ReadResponse,
    WriteRequest,
    validate_packet_length,
)


class TestProtocolHeader:
    """Test ProtocolHeader class."""

    def test_pack_unpack_read_command(self):
        """Test packing and unpacking read command."""
        header = ProtocolHeader(
            command=Command.READ, total_len=8, reserved=0, len=16, addr=0x1000
        )

        packed = header.pack()
        unpacked = ProtocolHeader.unpack(packed)

        assert unpacked.command == Command.READ
        assert unpacked.total_len == 8
        assert unpacked.reserved == 0
        assert unpacked.len == 16
        assert unpacked.addr == 0x1000

    def test_pack_unpack_write_command(self):
        """Test packing and unpacking write command."""
        header = ProtocolHeader(
            command=Command.WRITE, total_len=12, reserved=0, len=4, addr=0x2000
        )

        packed = header.pack()
        unpacked = ProtocolHeader.unpack(packed)

        assert unpacked.command == Command.WRITE
        assert unpacked.total_len == 12
        assert unpacked.reserved == 0
        assert unpacked.len == 4
        assert unpacked.addr == 0x2000

    def test_struct_size(self):
        """Test that struct size is correct."""
        assert ProtocolHeader.SIZE == 9  # 1+2+2+1+1+2 = 9 bytes (with padding)

    def test_unpack_insufficient_data(self):
        """Test unpacking with insufficient data."""
        with pytest.raises(ValueError, match="Insufficient data"):
            ProtocolHeader.unpack(b"short")

    def test_invalid_command(self):
        """Test unpacking invalid command."""
        # Create valid header but with invalid command
        packed = struct.pack(">BHHBBH", 0xFF, 8, 0, 0, 16, 0x1000)

        with pytest.raises(ValueError):
            ProtocolHeader.unpack(packed)


class TestReadRequest:
    """Test ReadRequest class."""

    def test_to_header(self):
        """Test conversion to protocol header."""
        request = ReadRequest(addr=0x1000, len=16)
        header = request.to_header()

        assert header.command == Command.READ
        assert header.total_len == 8
        assert header.reserved == 0
        assert header.len == 16
        assert header.addr == 0x1000


class TestWriteRequest:
    """Test WriteRequest class."""

    def test_to_header(self):
        """Test conversion to protocol header."""
        data = b"Hello, World!"
        request = WriteRequest(addr=0x2000, data=data)
        header = request.to_header()

        assert header.command == Command.WRITE
        assert header.total_len == 8 + len(data)
        assert header.reserved == 0
        assert header.len == len(data)
        assert header.addr == 0x2000


class TestReadResponse:
    """Test ReadResponse class."""

    def test_create_success(self):
        """Test creating successful response."""
        data = b"response_data"
        response = ReadResponse.create_success(data)

        assert response.status == 0
        assert response.data == data

    def test_create_error(self):
        """Test creating error response."""
        response = ReadResponse.create_error(1)

        assert response.status == 1
        assert response.data == b""

    def test_pack_success_response(self):
        """Test packing successful response."""
        data = b"test"
        response = ReadResponse.create_success(data)
        packed = response.pack()

        # Should start with header indicating WRITE command
        header = ProtocolHeader.unpack(packed)
        assert header.command == Command.WRITE
        assert header.total_len == 4 + len(data)
        assert header.len == len(data)

        # Status should be at position 9 (after header)
        status = struct.unpack(">B", packed[9:10])[0]
        assert status == 0

        # Data should follow status
        response_data = packed[10 : 10 + len(data)]
        assert response_data == data

    def test_pack_error_response(self):
        """Test packing error response."""
        response = ReadResponse.create_error(1)
        packed = response.pack()

        header = ProtocolHeader.unpack(packed)
        assert header.command == Command.WRITE
        assert header.total_len == 4  # 4 (response without header) + 0 (data)
        assert header.len == 0

        status = struct.unpack(">B", packed[9:10])[0]
        assert status == 1


class TestPacketValidation:
    """Test packet validation functions."""

    def test_validate_read_packet(self):
        """Test validating read packet."""
        header = ProtocolHeader(
            command=Command.READ, total_len=8, reserved=0, len=16, addr=0x1000
        )

        # Should be valid with just header size
        assert validate_packet_length(header, ProtocolHeader.SIZE)

        # Should be invalid with insufficient data
        assert not validate_packet_length(header, ProtocolHeader.SIZE - 1)

    def test_validate_write_packet(self):
        """Test validating write packet."""
        data_len = 4
        header = ProtocolHeader(
            command=Command.WRITE,
            total_len=8 + data_len,
            reserved=0,
            len=data_len,
            addr=0x2000,
        )

        # Should be valid with header + data
        assert validate_packet_length(header, ProtocolHeader.SIZE + data_len)

        # Should be invalid with insufficient data
        assert not validate_packet_length(header, ProtocolHeader.SIZE + data_len - 1)
        assert not validate_packet_length(header, ProtocolHeader.SIZE)


class TestCommand:
    """Test Command enum."""

    def test_command_values(self):
        """Test command enum values."""
        assert Command.READ == 0x0A
        assert Command.WRITE == 0x0B
        assert int(Command.READ) == 10
        assert int(Command.WRITE) == 11
