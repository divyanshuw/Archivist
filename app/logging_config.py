"""Shared logging configuration for Archivist entry points."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


LOG_DIRECTORY = Path(__file__).resolve().parent.parent / "logs"
_configured = False


def configure_logging(level: int = logging.INFO) -> None:
    """Configure console, server, and CLI log handlers once per process.

    Call this from an application entry point, such as a server startup function
    or ``respackage.main``. Importing this module alone does not configure
    logging.
    """
    global _configured

    if _configured:
        return

    LOG_DIRECTORY.mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    server_handler = RotatingFileHandler(
        LOG_DIRECTORY / "server.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    server_handler.setFormatter(formatter)

    respackage_handler = RotatingFileHandler(
        LOG_DIRECTORY / "respackage.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    respackage_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    server_logger = logging.getLogger("archivist.server")
    server_logger.setLevel(level)
    server_logger.addHandler(server_handler)
    server_logger.propagate = False

    respackage_logger = logging.getLogger("archivist.respackage")
    respackage_logger.setLevel(level)
    respackage_logger.addHandler(respackage_handler)
    respackage_logger.propagate = False

    _configured = True
