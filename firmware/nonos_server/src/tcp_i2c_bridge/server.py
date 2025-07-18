"""TCP server implementation for I2C bridge."""

import asyncio
import socket
import time
import traceback
from pathlib import Path

import structlog

from tcp_i2c_bridge.i2c_backend import I2CBackend
from tcp_i2c_bridge.protocol import (
    DecodeException,
    DecodeExceptionInsufficientData,
    DecodeExceptionInvalidHeaderCommand,
)
from tcp_i2c_bridge.protocol import (
    Header as NetworkHeader,
)
from tcp_i2c_bridge.protocol import (
    Read as NetworkRead,
)
from tcp_i2c_bridge.protocol import (
    Write as NetworkWrite,
)
from tcp_i2c_bridge.protocol_dumper import ProtocolDumper

logger = structlog.get_logger()


class TCPClientHandler:
    """Handle individual TCP client connections."""

    def __init__(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        i2c_backend: I2CBackend,
        protocol_dumper: ProtocolDumper,
        client_addr: tuple[str, int],
    ):
        self.reader = reader
        self.writer = writer
        self.i2c_backend = i2c_backend
        self.protocol_dumper = protocol_dumper
        self.client_addr = client_addr
        self.buffer = b""
        self.client_id = f"{client_addr[0]}:{client_addr[1]}"

        logger.info("Client connected", client=self.client_id)

    async def handle_connection(self) -> None:
        """Handle client connection until it closes."""
        try:
            while True:
                # Read more data from client
                data = await self.reader.read(4096)
                now = time.perf_counter_ns()
                if not data:
                    break

                self.buffer += data

                data_len = len(self.buffer)

                # Process all complete packets in buffer
                while await self._process_packet():
                    pass

                logger.info(
                    "Processed packet: took %0.2f ms, %d bytes",
                    (time.perf_counter_ns() - now) / 1000000,
                    data_len,
                )

        except Exception as e:
            logger.error("Client handler error", client=self.client_id, error=str(e))
        finally:
            self.writer.close()
            await self.writer.wait_closed()
            logger.info("Client disconnected", client=self.client_id)

    async def _process_packet(self) -> bool:
        """Process one complete packet from buffer.

        Returns:
            True if a packet was processed, False if need more data
        """
        # Need at least header size
        logger.debug(
            "Processing packet",
            client=self.client_id,
            buffer_len=len(self.buffer),
            needed=NetworkHeader.SIZE,
            buffer_hex=self.buffer.hex(),
        )

        if len(self.buffer) < NetworkHeader.SIZE:
            return False

        try:
            # Parse header
            header = NetworkHeader.unpack(self.buffer)
        except DecodeExceptionInvalidHeaderCommand as e:
            logger.error(
                "Failed to decode header",
                client=self.client_id,
                error=str(e),
                raw=self.buffer.hex(),
            )
            self.buffer = b""
            return False
        except DecodeException:
            logger.error(
                "Failed to decode header",
                client=self.client_id,
                error=traceback.format_exc(),
                raw=self.buffer.hex(),
            )
            self.buffer = b""
            return False

        # Dump network layer
        await self.protocol_dumper.dump_network_packet(
            self.client_id, "RX_RAW", self.buffer
        )

        try:
            request, remaining_buffer = header.get_request(self.buffer)
        except DecodeExceptionInsufficientData:
            return False
        except DecodeException as e:
            logger.error(
                "Failed to decode request",
                client=self.client_id,
                error=str(e),
            )
            self.buffer = b""
            return False
        except Exception:
            logger.error(
                "Fatal fail to decode request",
                client=self.client_id,
                raw=self.buffer.hex(),
                error=traceback.format_exc(),
            )
            self.buffer = b""
            return False

        if isinstance(request, NetworkRead.Request):
            await self._handle_read_request(request)
        elif isinstance(request, NetworkWrite.Request):
            await self._handle_write_request(request)
        else:
            # Should never happen
            raise Exception(f"Unknown request type: {type(request)}")

        await self.protocol_dumper.dump_network_packet(
            self.client_id, "RX_DECODED", self.buffer[: -len(remaining_buffer)]
        )

        # Remove processed data from buffer
        self.buffer = remaining_buffer
        return bool(self.buffer)

    async def _handle_read_request(self, request: NetworkRead.Request) -> None:
        """Handle I2C read request."""

        logger.debug(
            "Processing read request",
            client=self.client_id,
            addr=f"0x{request.Address:04X}",
            length=request.Data_length,
        )

        try:
            # Perform I2C read
            data = self.i2c_backend.read(request.Address, request.Data_length)

            # Dump I2C layer
            await self.protocol_dumper.dump_i2c_transaction(
                self.client_id, "READ", request.Address, request.Data_length, data
            )

            # Send response
            response = request.create_response(data=data)
            response_data = response.pack()

            await self.protocol_dumper.dump_network_packet(
                self.client_id, "TX", response_data
            )

            self.writer.write(response_data)
            await self.writer.drain()

            logger.debug(
                "Read request completed",
                client=self.client_id,
                addr=f"0x{request.Address:04X}",
                length=request.Data_length,
                data_len=len(data),
                data_hex=data.hex(),
            )

        except Exception as e:
            logger.error(
                "Read request failed",
                client=self.client_id,
                addr=f"0x{request.Address:04X}",
                length=request.Data_length,
                error=str(e),
            )

            # Send error response
            response = request.create_response(error=True)
            response_data = response.pack()

            await self.protocol_dumper.dump_network_packet(
                self.client_id, "TX", response_data
            )

            self.writer.write(response_data)
            await self.writer.drain()

    async def _handle_write_request(self, request: NetworkWrite.Request) -> None:
        """Handle I2C write request."""
        # Extract data from buffer

        logger.debug(
            "Processing write request",
            client=self.client_id,
            addr=f"0x{request.Address:04X}",
            length=len(request.Data),
        )

        # TODO respect chip address

        try:
            # Perform I2C write
            self.i2c_backend.write(request.Address, request.Data)

            # Dump I2C layer
            await self.protocol_dumper.dump_i2c_transaction(
                self.client_id,
                "WRITE",
                request.Address,
                len(request.Data),
                request.Data,
            )

            logger.debug(
                "Write request completed",
                client=self.client_id,
                addr=f"0x{request.Address:04X}",
                length=len(request.Data),
                data_hex=request.Data.hex(),
            )

        except Exception as e:
            logger.error(
                "Write request failed",
                client=self.client_id,
                addr=f"0x{request.Address:04X}",
                length=len(request.Data),
                error=str(e),
            )


class TCPServer:
    """TCP server for I2C bridge."""

    def __init__(
        self,
        host: str,
        port: int,
        i2c_backend: I2CBackend,
        dump_dir: Path | None = None,
    ):
        self.host = host
        self.port = port
        self.i2c_backend = i2c_backend
        self.protocol_dumper = ProtocolDumper(dump_dir)
        self.server: asyncio.Server | None = None
        self.clients: set[asyncio.Task] = set()

    async def start(self) -> None:
        """Start the TCP server."""
        self.server = await asyncio.start_server(
            self._handle_client, self.host, self.port, reuse_port=True
        )

        # Get actual bound address
        server_host, server_port = self.server.sockets[0].getsockname()

        logger.info(
            "TCP server started",
            host=server_host,
            port=server_port,
            dump_dir=str(self.protocol_dumper.dump_dir)
            if self.protocol_dumper.dump_dir
            else None,
        )

        # Show available IP addresses
        self._show_network_addresses()

    def _show_network_addresses(self) -> None:
        """Show available network addresses."""
        import socket

        hostname = socket.gethostname()
        try:
            # Get all network interfaces
            addresses = []
            for info in socket.getaddrinfo(hostname, None):
                addr = info[4][0]
                if (
                    addr not in addresses
                    and not isinstance(addr, int)
                    and not addr.startswith("127.")
                ):
                    addresses.append(addr)

            if addresses:
                logger.info("Available network addresses", addresses=addresses)
            else:
                logger.info("Server listening on localhost only")

        except Exception:
            logger.debug("Could not enumerate network addresses")

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        """Handle new client connection."""
        client_addr = writer.get_extra_info("peername")

        # Set TCP_NODELAY for low latency
        sock = writer.get_extra_info("socket")
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        handler = TCPClientHandler(
            reader, writer, self.i2c_backend, self.protocol_dumper, client_addr
        )

        # Create task for this client
        task = asyncio.create_task(handler.handle_connection())
        self.clients.add(task)

        try:
            await task
        finally:
            self.clients.discard(task)

    async def stop(self) -> None:
        """Stop the TCP server."""
        if self.server:
            logger.info("Stopping TCP server")

            # Stop accepting new connections
            self.server.close()
            await self.server.wait_closed()

            # Cancel all client tasks
            for task in self.clients:
                task.cancel()

            # Wait for all clients to finish
            if self.clients:
                await asyncio.gather(*self.clients, return_exceptions=True)

            self.clients.clear()
            logger.info("TCP server stopped")

    async def serve_forever(self) -> None:
        """Serve forever until interrupted."""
        if not self.server:
            raise RuntimeError("Server not started")

        async with self.server:
            await self.server.serve_forever()
