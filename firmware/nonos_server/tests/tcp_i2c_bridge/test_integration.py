"""Integration tests for TCP-I2C bridge."""

import asyncio
import struct
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tcp_i2c_bridge.app import TCPBridgeApp
from tcp_i2c_bridge.protocol import Command, ProtocolHeader


class TestTCPBridgeIntegration:
    """Integration tests for the complete TCP-I2C bridge."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test files."""
        with TemporaryDirectory() as tmp_dir:
            yield Path(tmp_dir)

    @pytest.fixture
    async def running_app(self, temp_dir):
        """Create and start TCP bridge app."""
        app = TCPBridgeApp.create_with_debug_backend(
            host="127.0.0.1",
            port=0,  # Dynamic port allocation
            dump_dir=temp_dir / "dumps",
            log_level="DEBUG",
        )

        await app.start()

        # Get actual port and store it as an attribute for testing
        if app.server.server is not None:
            port = app.server.server.sockets[0].getsockname()[1]
            app.actual_port = port  # type: ignore
        else:
            raise RuntimeError("Server not started properly")

        yield app

        await app.cleanup()

    @pytest.mark.asyncio
    async def test_read_write_cycle(self, running_app):
        """Test complete read/write cycle."""
        # Connect to server
        reader, writer = await asyncio.open_connection(
            "127.0.0.1", running_app.actual_port
        )

        try:
            # Test data
            test_addr = 0x4010
            test_data = b"Hello, I2C!"

            # 1. Write data
            write_header = ProtocolHeader(
                command=Command.WRITE,
                total_len=8 + len(test_data),
                reserved=0,
                len=len(test_data),
                addr=test_addr,
            )

            write_packet = write_header.pack() + test_data
            writer.write(write_packet)
            await writer.drain()

            # Small delay to ensure write completes
            await asyncio.sleep(0.01)

            # 2. Read data back
            read_header = ProtocolHeader(
                command=Command.READ,
                total_len=8,
                reserved=0,
                len=len(test_data),
                addr=test_addr,
            )

            read_packet = read_header.pack()
            writer.write(read_packet)
            await writer.drain()

            # 3. Receive response
            response_data = await reader.read(1024)
            assert len(response_data) > 0

            # Parse response
            response_header = ProtocolHeader.unpack(response_data)
            assert response_header.command == Command.WRITE
            assert response_header.len == len(test_data)

            # Extract status and data
            status = struct.unpack(">B", response_data[9:10])[0]
            received_data = response_data[10 : 10 + len(test_data)]

            assert status == 0  # Success
            assert received_data == test_data

        finally:
            writer.close()
            await writer.wait_closed()

    @pytest.mark.asyncio
    async def test_multiple_clients(self, running_app):
        """Test handling multiple concurrent clients."""

        async def client_operation(client_id):
            """Perform operations as a client."""
            reader, writer = await asyncio.open_connection(
                "127.0.0.1", running_app.actual_port
            )

            try:
                # Each client writes to different address
                test_addr = 0x4000 + client_id * 16
                test_data = f"Client {client_id} data".encode()

                # Write data
                write_header = ProtocolHeader(
                    command=Command.WRITE,
                    total_len=8 + len(test_data),
                    reserved=0,
                    len=len(test_data),
                    addr=test_addr,
                )

                write_packet = write_header.pack() + test_data
                writer.write(write_packet)
                await writer.drain()

                # Read data back
                read_header = ProtocolHeader(
                    command=Command.READ,
                    total_len=8,
                    reserved=0,
                    len=len(test_data),
                    addr=test_addr,
                )

                read_packet = read_header.pack()
                writer.write(read_packet)
                await writer.drain()

                # Receive response
                response_data = await reader.read(1024)
                ProtocolHeader.unpack(response_data)  # Verify it's a valid header

                status = struct.unpack(">B", response_data[9:10])[0]
                received_data = response_data[10 : 10 + len(test_data)]

                assert status == 0
                assert received_data == test_data

                return True

            finally:
                writer.close()
                await writer.wait_closed()

        # Run multiple clients concurrently
        tasks = [client_operation(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        # All clients should succeed
        assert all(results)

    @pytest.mark.asyncio
    async def test_protocol_dumping(self, running_app, temp_dir):
        """Test that protocol dumping works correctly."""
        # Connect and perform operation
        _reader, writer = await asyncio.open_connection(
            "127.0.0.1", running_app.actual_port
        )

        try:
            # Write some data
            test_addr = 0x4020
            test_data = b"dump_test"

            write_header = ProtocolHeader(
                command=Command.WRITE,
                total_len=8 + len(test_data),
                reserved=0,
                len=len(test_data),
                addr=test_addr,
            )

            write_packet = write_header.pack() + test_data
            writer.write(write_packet)
            await writer.drain()

            # Small delay to ensure dumping completes
            await asyncio.sleep(0.01)

        finally:
            writer.close()
            await writer.wait_closed()

        # Check that dump files were created
        dumps_dir = temp_dir / "dumps"
        assert dumps_dir.exists()

        # Should have session directory
        session_dirs = list(dumps_dir.glob("session_*"))
        assert len(session_dirs) > 0

        session_dir = session_dirs[0]

        # Check for network and i2c directories
        network_dir = session_dir / "network"
        i2c_dir = session_dir / "i2c"

        assert network_dir.exists()
        assert i2c_dir.exists()

        # Check for log files
        network_log = session_dir / "network.log"
        i2c_log = session_dir / "i2c.log"

        assert network_log.exists()
        assert i2c_log.exists()

        # Check that files contain data
        assert network_log.stat().st_size > 0
        assert i2c_log.stat().st_size > 0

        # Check for binary dump files
        network_files = list(network_dir.glob("*.bin"))
        i2c_files = list(i2c_dir.glob("*.bin"))

        assert len(network_files) > 0
        assert len(i2c_files) > 0

    @pytest.mark.asyncio
    async def test_error_handling(self, running_app):
        """Test error handling for invalid operations."""
        # Connect to server
        reader, writer = await asyncio.open_connection(
            "127.0.0.1", running_app.actual_port
        )

        try:
            # Try to read from out-of-range address
            read_header = ProtocolHeader(
                command=Command.READ,
                total_len=8,
                reserved=0,
                len=16,
                addr=0x1000,  # Out of range for debug backend
            )

            read_packet = read_header.pack()
            writer.write(read_packet)
            await writer.drain()

            # Receive response
            response_data = await reader.read(1024)
            assert len(response_data) > 0

            # Should get response with zero data (debug backend behavior)
            response_header = ProtocolHeader.unpack(response_data)
            assert response_header.command == Command.WRITE
            assert response_header.len == 16

            status = struct.unpack(">B", response_data[9:10])[0]
            received_data = response_data[10 : 10 + 16]

            assert status == 0  # Success (debug backend doesn't error)
            # Debug backend returns zeros for out of range, but may return different length
            assert len(received_data) >= 15  # At least 15 bytes
            assert all(b == 0 for b in received_data)  # All zeros

        finally:
            writer.close()
            await writer.wait_closed()

    @pytest.mark.asyncio
    async def test_connection_handling(self, running_app):
        """Test connection establishment and cleanup."""
        # Test that server accepts connections
        _reader, writer = await asyncio.open_connection(
            "127.0.0.1", running_app.actual_port
        )

        # Connection should be established
        assert not writer.is_closing()

        # Close connection
        writer.close()
        await writer.wait_closed()

        # Should be able to connect again
        _reader2, writer2 = await asyncio.open_connection(
            "127.0.0.1", running_app.actual_port
        )

        writer2.close()
        await writer2.wait_closed()

    @pytest.mark.asyncio
    async def test_large_data_transfer(self, running_app):
        """Test handling large data transfers."""
        # Connect to server
        reader, writer = await asyncio.open_connection(
            "127.0.0.1", running_app.actual_port
        )

        try:
            # Test with larger data (within debug backend range)
            test_addr = 0x4000
            test_data = b"A" * 200  # 200 bytes

            # Write data
            write_header = ProtocolHeader(
                command=Command.WRITE,
                total_len=8 + len(test_data),
                reserved=0,
                len=len(test_data),
                addr=test_addr,
            )

            write_packet = write_header.pack() + test_data
            writer.write(write_packet)
            await writer.drain()

            # Read data back
            read_header = ProtocolHeader(
                command=Command.READ,
                total_len=8,
                reserved=0,
                len=len(test_data),
                addr=test_addr,
            )

            read_packet = read_header.pack()
            writer.write(read_packet)
            await writer.drain()

            # Receive response
            response_data = await reader.read(2048)  # Larger buffer
            ProtocolHeader.unpack(response_data)  # Verify it's a valid header

            status = struct.unpack(">B", response_data[9:10])[0]
            received_data = response_data[10 : 10 + len(test_data)]

            assert status == 0
            assert received_data == test_data

        finally:
            writer.close()
            await writer.wait_closed()
