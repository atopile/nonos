"""Main application for TCP-I2C bridge."""

import asyncio
import signal
from pathlib import Path

import structlog

from tcp_i2c_bridge.i2c_backend import DebugI2CBackend, I2CBackend, SMBusI2CBackend
from tcp_i2c_bridge.logging_config import setup_logging
from tcp_i2c_bridge.server import TCPServer

logger = structlog.get_logger()


class TCPBridgeApp:
    """Main application class for TCP-I2C bridge."""

    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8086,
        i2c_backend: I2CBackend | None = None,
        dump_dir: Path | None = None,
        log_level: str = "INFO",
        log_file: Path | None = None,
        json_logs: bool = False,
    ):
        """Initialize the TCP-I2C bridge application.

        Args:
            host: TCP server host to bind to
            port: TCP server port to bind to
            i2c_backend: I2C backend instance
            dump_dir: Directory to dump protocol logs
            log_level: Logging level
            log_file: Optional log file path
            json_logs: Whether to use JSON log format
        """
        self.host = host
        self.port = port
        self.i2c_backend = i2c_backend or DebugI2CBackend()
        self.dump_dir = dump_dir

        # Set up logging
        setup_logging(log_level, log_file, json_logs)

        # Create server
        self.server = TCPServer(
            host=self.host,
            port=self.port,
            i2c_backend=self.i2c_backend,
            dump_dir=self.dump_dir,
        )

        # Track if we're running
        self.running = False
        self.shutdown_event = asyncio.Event()

    async def start(self) -> None:
        """Start the TCP-I2C bridge application."""
        try:
            logger.info("Starting TCP-I2C bridge application")

            # Start TCP server
            await self.server.start()
            self.running = True

            # Set up signal handlers
            self._setup_signal_handlers()

            logger.info("TCP-I2C bridge application started successfully")

        except Exception as e:
            logger.error("Failed to start application", error=str(e))
            await self.cleanup()
            raise

    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""

        def signal_handler(signum):
            logger.info(f"Received signal {signum}, initiating shutdown")
            self.shutdown_event.set()

        # Use asyncio's event loop signal handling for proper integration
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, signal_handler, signal.SIGINT)
        loop.add_signal_handler(signal.SIGTERM, signal_handler, signal.SIGTERM)

    async def run(self) -> None:
        """Run the application until shutdown."""
        try:
            await self.start()

            # Wait for shutdown signal
            await self.shutdown_event.wait()

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down")
        except Exception as e:
            logger.error("Application error", error=str(e))
            raise
        finally:
            await self.cleanup()

    async def cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up resources")

        try:
            # Stop server
            if self.server:
                await self.server.stop()

            # Close I2C backend
            if self.i2c_backend:
                self.i2c_backend.close()

            # Create protocol dump summary
            if self.server.protocol_dumper:
                self.server.protocol_dumper.create_summary_report()

            logger.info("Cleanup completed")

        except Exception as e:
            logger.error("Error during cleanup", error=str(e))

        self.running = False

    @classmethod
    def create_with_i2c_backend(
        cls, i2c_bus: int, device_addr: int, **kwargs
    ) -> "TCPBridgeApp":
        """Create application with SMBus I2C backend.

        Args:
            i2c_bus: I2C bus number
            device_addr: I2C device address
            **kwargs: Additional arguments for TCPBridgeApp

        Returns:
            Configured application instance
        """
        i2c_backend = SMBusI2CBackend(i2c_bus, device_addr)
        return cls(i2c_backend=i2c_backend, **kwargs)

    @classmethod
    def create_with_debug_backend(cls, **kwargs) -> "TCPBridgeApp":
        """Create application with debug I2C backend.

        Args:
            **kwargs: Additional arguments for TCPBridgeApp

        Returns:
            Configured application instance
        """
        i2c_backend = DebugI2CBackend()
        return cls(i2c_backend=i2c_backend, **kwargs)


async def main() -> None:
    """Main entry point for the application."""
    app = TCPBridgeApp.create_with_debug_backend()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
