"""Logger utility module."""
import logging
from typing import Any


class LoggerWrapper:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)

    def info(self, event: str, **kwargs: Any) -> None:
        self.logger.info(f"{event}: {kwargs}")

    def error(self, event: str, **kwargs: Any) -> None:
        self.logger.error(f"{event}: {kwargs}")

    def warning(self, event: str, **kwargs: Any) -> None:
        self.logger.warning(f"{event}: {kwargs}")


def get_logger(name: str) -> LoggerWrapper:
    return LoggerWrapper(name)
