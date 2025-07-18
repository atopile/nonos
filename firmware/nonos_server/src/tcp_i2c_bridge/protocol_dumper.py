"""Protocol dumper for network and I2C layer logging."""

from datetime import datetime
from pathlib import Path

import structlog

logger = structlog.get_logger()


class ProtocolDumper:
    """Dump network and I2C protocol layers to files."""

    def __init__(self, dump_dir: Path | None = None):
        """Initialize protocol dumper.

        Args:
            dump_dir: Directory to dump files to. If None, use current directory.
        """
        if dump_dir is None:
            dump_dir = Path.cwd() / "dumps"

        self.dump_dir = dump_dir
        self.dump_dir.mkdir(exist_ok=True)

        # Create session-specific directory
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.dump_dir / f"session_{session_id}"
        self.session_dir.mkdir(exist_ok=True)

        # Create subdirectories for different layers
        self.network_dir = self.session_dir / "network"
        self.i2c_dir = self.session_dir / "i2c"
        self.network_dir.mkdir(exist_ok=True)
        self.i2c_dir.mkdir(exist_ok=True)

        # File handles for continuous logging
        self.network_log_file = self.session_dir / "network.log"
        self.i2c_log_file = self.session_dir / "i2c.log"

        logger.info(
            "Protocol dumper initialized",
            dump_dir=str(self.dump_dir),
            session_dir=str(self.session_dir),
        )

    async def dump_network_packet(
        self, client_id: str, direction: str, data: bytes
    ) -> None:
        """Dump network layer packet.

        Args:
            client_id: Client identifier
            direction: "RX" or "TX"
            data: Raw packet data
        """
        timestamp = datetime.now().isoformat()

        # Create individual packet file
        packet_filename = f"{timestamp}_{client_id.replace(':', '_')}_{direction}.bin"
        packet_path = self.network_dir / packet_filename

        try:
            # Write binary data
            packet_path.write_bytes(data)

            # Append to network log
            log_entry = (
                f"{timestamp} {client_id} {direction} "
                f"len={len(data)} data={data.hex()}\n"
            )

            with open(self.network_log_file, "a") as f:
                f.write(log_entry)

            logger.debug(
                "Network packet dumped",
                client=client_id,
                direction=direction,
                length=len(data),
                file=str(packet_path),
            )

        except Exception as e:
            logger.error(
                "Failed to dump network packet",
                client=client_id,
                direction=direction,
                error=str(e),
            )

    async def dump_i2c_transaction(
        self, client_id: str, operation: str, addr: int, length: int, data: bytes
    ) -> None:
        """Dump I2C layer transaction.

        Args:
            client_id: Client identifier
            operation: "READ" or "WRITE"
            addr: I2C register address
            length: Transaction length
            data: Transaction data
        """
        timestamp = datetime.now().isoformat()

        # Create individual transaction file
        transaction_filename = (
            f"{timestamp}_{client_id.replace(':', '_')}_"
            f"{operation}_{addr:04X}_{length}.bin"
        )
        transaction_path = self.i2c_dir / transaction_filename

        try:
            # Write binary data
            transaction_path.write_bytes(data)

            # Append to I2C log
            log_entry = (
                f"{timestamp} {client_id} {operation} "
                f"addr=0x{addr:04X} len={length} data={data.hex()}\n"
            )

            with open(self.i2c_log_file, "a") as f:
                f.write(log_entry)

            logger.debug(
                "I2C transaction dumped",
                client=client_id,
                operation=operation,
                addr=f"0x{addr:04X}",
                length=length,
                file=str(transaction_path),
            )

        except Exception as e:
            logger.error(
                "Failed to dump I2C transaction",
                client=client_id,
                operation=operation,
                addr=f"0x{addr:04X}",
                error=str(e),
            )

    def create_summary_report(self) -> None:
        """Create a summary report of the session."""
        summary_path = self.session_dir / "summary.txt"

        try:
            network_files = list(self.network_dir.glob("*.bin"))
            i2c_files = list(self.i2c_dir.glob("*.bin"))

            with open(summary_path, "w") as f:
                f.write("TCP-I2C Bridge Session Summary\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Session Directory: {self.session_dir}\n")
                f.write(f"Network Packets: {len(network_files)}\n")
                f.write(f"I2C Transactions: {len(i2c_files)}\n\n")

                f.write("Network Layer Files:\n")
                for file_path in sorted(network_files):
                    size = file_path.stat().st_size
                    f.write(f"  {file_path.name} ({size} bytes)\n")

                f.write("\nI2C Layer Files:\n")
                for file_path in sorted(i2c_files):
                    size = file_path.stat().st_size
                    f.write(f"  {file_path.name} ({size} bytes)\n")

            logger.info(
                "Session summary created",
                summary_file=str(summary_path),
                network_packets=len(network_files),
                i2c_transactions=len(i2c_files),
            )

        except Exception as e:
            logger.error("Failed to create summary report", error=str(e))
