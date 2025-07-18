"""Logging configuration for TCP-I2C bridge."""

import logging
from pathlib import Path

import structlog
from rich.console import Console
from rich.logging import RichHandler


class CustomConsoleRenderer:
    """
    Renders log entries to the console with a custom format.
    - Timestamp
    - Single-letter log level
    - Padded event message
    - Key-value pairs
    """

    def __init__(self, pad_event: int = 30):
        self._pad_event = pad_event

    def __call__(self, _, __, event_dict: dict) -> str:
        # ts = event_dict.pop("timestamp", "")
        level = event_dict.pop("level", "")
        if level:
            level = level[0].upper()
        event = str(event_dict.pop("event", ""))

        exception = event_dict.pop("exception", None)
        stack = event_dict.pop("stack", None)

        # Event padding
        event = event.ljust(self._pad_event)

        # Key-value pairs
        kv_str = " ".join(f"{k}={v}" for k, v in sorted(event_dict.items()))

        log_line = f"{level} {event}"
        if kv_str:
            log_line += f" {kv_str}"

        if stack:
            log_line += f"\n{stack}"
        if exception:
            log_line += f"\n{exception}"

        return log_line


def setup_logging(
    log_level: str = "INFO", log_file: Path | None = None, json_logs: bool = False
) -> None:
    """Set up structured logging with rich console output.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file to write logs to
        json_logs: Whether to use JSON format for structured logs
    """
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=Console(stderr=True),
                rich_tracebacks=True,
                show_time=True,
                show_path=True,
            )
        ],
    )

    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(CustomConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Add file handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))

        if json_logs:
            file_formatter = logging.Formatter("%(message)s")
        else:
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

        file_handler.setFormatter(file_formatter)
        logging.getLogger().addHandler(file_handler)

    # Log initial configuration
    logger = structlog.get_logger()
    logger.info(
        "Logging configured",
        level=log_level,
        file=str(log_file) if log_file else None,
        json=json_logs,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: Logger name

    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)
