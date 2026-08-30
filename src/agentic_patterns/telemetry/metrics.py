"""Metrics collector telemetry module."""
from typing import Any


class MetricsCollector:
    def __init__(self) -> None:
        self.metrics: dict[str, Any] = {}

    def record(self, metric_name: str, value: Any) -> None:
        self.metrics[metric_name] = value
