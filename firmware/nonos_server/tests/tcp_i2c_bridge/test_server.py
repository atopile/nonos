"""Tests for TCP server implementation."""

import asyncio
import socket
import struct
from unittest.mock import AsyncMock, Mock, patch

import pytest

from tcp_i2c_bridge.i2c_backend import DebugI2CBackend
from tcp_i2c_bridge.protocol import Command, ProtocolHeader
from tcp_i2c_bridge.protocol_dumper import ProtocolDumper
from tcp_i2c_bridge.server import TCPClientHandler, TCPServer


class TestTCPClientHandler:
    """Test TCP client handler."""

    @pytest.fixture
    def mock_reader(self):
        """Create mock stream reader."""
        reader = Mock()
        reader.read = AsyncMock()
        return reader

    @pytest.fixture
    def mock_writer(self):
        """Create mock stream writer."""
        writer = Mock()
        writer.write = Mock()
        writer.drain = AsyncMock()
        writer.close = Mock()
        writer.wait_closed = AsyncMock()
        return writer

    @pytest.fixture
    def debug_backend(self):
        """Create debug I2C backend."""
        return DebugI2CBackend()

    @pytest.fixture
    def mock_protocol_dumper(self):
        """Create mock protocol dumper."""
        dumper = Mock(spec=ProtocolDumper)
        dumper.dump_network_packet = AsyncMock()
        dumper.dump_i2c_transaction = AsyncMock()
        return dumper

    @pytest.fixture
    def client_handler(
        self, mock_reader, mock_writer, debug_backend, mock_protocol_dumper
    ):
        """Create TCP client handler."""
        return TCPClientHandler(
            mock_reader,
            mock_writer,
            debug_backend,
            mock_protocol_dumper,
            ("127.0.0.1", 12345),
        )

    @pytest.mark.asyncio
    async def test_handle_read_request(
        self,
        client_handler,
        mock_reader,
        mock_writer,
        debug_backend,
        mock_protocol_dumper,
    ):
        """Test handling read request."""
        # Set up test data in debug backend
        test_addr = 0x4010
        test_data = b"test_response"
        debug_backend.write(test_addr, test_data)

        # Create read request packet
        header = ProtocolHeader(
            command=Command.READ,
            total_len=8,
            reserved=0,
            len=len(test_data),
            addr=test_addr,
        )

        # Mock reader to return the packet
        mock_reader.read.side_effect = [header.pack(), b""]

        # Handle connection
        await client_handler.handle_connection()

        # Verify response was sent
        mock_writer.write.assert_called()
        response_data = mock_writer.write.call_args[0][0]

        # Verify response format
        response_header = ProtocolHeader.unpack(response_data)
        assert response_header.command == Command.WRITE
        assert response_header.len == len(test_data)

        # Verify protocol dumping was called
        mock_protocol_dumper.dump_network_packet.assert_called()
        mock_protocol_dumper.dump_i2c_transaction.assert_called()

    @pytest.mark.asyncio
    async def test_handle_write_request(
        self,
        client_handler,
        mock_reader,
        mock_writer,
        debug_backend,
        mock_protocol_dumper,
    ):
        """Test handling write request."""
        test_addr = 0x4020
        test_data = b"write_data"

        # Create write request packet
        header = ProtocolHeader(
            command=Command.WRITE,
            total_len=8 + len(test_data),
            reserved=0,
            len=len(test_data),
            addr=test_addr,
        )

        packet = header.pack() + test_data

        # Mock reader to return the packet
        mock_reader.read.side_effect = [packet, b""]

        # Handle connection
        await client_handler.handle_connection()

        # Verify data was written to backend
        read_data = debug_backend.read(test_addr, len(test_data))
        assert read_data == test_data

        # Verify protocol dumping was called
        mock_protocol_dumper.dump_i2c_transaction.assert_called()

    @pytest.mark.asyncio
    async def test_handle_invalid_command(
        self, client_handler, mock_reader, mock_writer, mock_protocol_dumper
    ):
        """Test handling invalid command."""
        # Create packet with invalid command
        # We'll manually create the packet since we can't create a ProtocolHeader with invalid command
        invalid_packet = struct.pack(">BHHBBH", 0xFF, 8, 0, 0, 0, 0x1000)

        # Mock reader to return the packet
        mock_reader.read.side_effect = [invalid_packet, b""]

        # Should not raise exception
        await client_handler.handle_connection()

    @pytest.mark.asyncio
    async def test_handle_partial_packet(
        self, client_handler, mock_reader, mock_writer
    ):
        """Test handling partial packet."""
        # Create read request packet
        header = ProtocolHeader(
            command=Command.READ, total_len=8, reserved=0, len=4, addr=0x1000
        )

        packet = header.pack()

        # Mock reader to return packet in parts
        mock_reader.read.side_effect = [packet[:5], packet[5:], b""]

        # Should handle partial packets correctly
        await client_handler.handle_connection()

        # Should have sent response
        mock_writer.write.assert_called()


class TestTCPServer:
    """Test TCP server."""

    @pytest.fixture
    def debug_backend(self):
        """Create debug I2C backend."""
        return DebugI2CBackend()

    @pytest.fixture
    def tcp_server(self, debug_backend):
        """Create TCP server."""
        return TCPServer("127.0.0.1", 0, debug_backend)  # Port 0 for dynamic allocation

    @pytest.mark.asyncio
    async def test_start_stop(self, tcp_server):
        """Test starting and stopping server."""
        # Start server
        await tcp_server.start()
        assert tcp_server.server is not None

        # Get actual port
        port = tcp_server.server.sockets[0].getsockname()[1]
        assert port > 0

        # Stop server
        await tcp_server.stop()
        assert tcp_server.server is not None  # Server object still exists but closed

    @pytest.mark.asyncio
    async def test_serve_forever_not_started(self, tcp_server):
        """Test serve_forever without starting."""
        with pytest.raises(RuntimeError, match="Server not started"):
            await tcp_server.serve_forever()

    @pytest.mark.asyncio
    async def test_client_connection_handling(self, tcp_server):
        """Test that clients are properly handled."""
        await tcp_server.start()

        # Create mock client connection
        mock_reader = Mock()
        mock_writer = Mock()
        # Mock socket for TCP_NODELAY
        mock_socket = Mock()
        mock_writer.get_extra_info.side_effect = lambda key: {
            "peername": ("127.0.0.1", 12345),
            "socket": mock_socket,
        }[key]

        # Mock the handler's handle_connection method to avoid infinite loop
        with patch("tcp_i2c_bridge.server.TCPClientHandler") as mock_handler_class:
            mock_handler = Mock()
            mock_handler.handle_connection = AsyncMock()
            mock_handler_class.return_value = mock_handler

            # Test client handler creation
            await tcp_server._handle_client(mock_reader, mock_writer)

        # Verify TCP_NODELAY was set
        mock_socket.setsockopt.assert_called_with(
            socket.IPPROTO_TCP, socket.TCP_NODELAY, 1
        )

        await tcp_server.stop()

    @pytest.mark.asyncio
    async def test_multiple_clients(self, tcp_server):
        """Test handling multiple concurrent clients."""
        await tcp_server.start()

        # Simulate multiple clients
        initial_client_count = len(tcp_server.clients)

        # Create client task
        task = asyncio.create_task(asyncio.sleep(0.1))
        tcp_server.clients.add(task)

        assert len(tcp_server.clients) == initial_client_count + 1

        # Stop server (should cancel all client tasks)
        await tcp_server.stop()

        assert len(tcp_server.clients) == 0
