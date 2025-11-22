#!/usr/bin/env python3
"""
Observability Hooks

Metrics collection, structured logging, and observability utilities.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
import time
import json
import logging


@dataclass
class MetricPoint:
    """Single metric data point"""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collect and export metrics"""

    def __init__(self):
        self.metrics: List[MetricPoint] = []

    def increment(self, name: str, value: float = 1.0, tags: Optional[Dict[str, str]] = None):
        """Increment a counter"""
        self.metrics.append(MetricPoint(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        ))

    def gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge value"""
        self.metrics.append(MetricPoint(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        ))

    def histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record histogram value (for timing, sizes, etc.)"""
        self.metrics.append(MetricPoint(
            name=name,
            value=value,
            timestamp=datetime.now(),
            tags=tags or {}
        ))

    def get_metrics(self) -> List[MetricPoint]:
        """Get all collected metrics"""
        return self.metrics

    def clear(self):
        """Clear all metrics"""
        self.metrics = []

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format"""
        lines = []
        for metric in self.metrics:
            tags_str = ",".join(f'{k}="{v}"' for k, v in metric.tags.items())
            line = f"{metric.name}{{{tags_str}}} {metric.value} {int(metric.timestamp.timestamp() * 1000)}"
            lines.append(line)
        return "\n".join(lines)


class TimingContext:
    """Context manager for timing operations"""

    def __init__(self, metrics: MetricsCollector, metric_name: str, tags: Optional[Dict[str, str]] = None):
        self.metrics = metrics
        self.metric_name = metric_name
        self.tags = tags or {}
        self.start_time: Optional[float] = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.metrics.histogram(
            f"{self.metric_name}_duration_seconds",
            duration,
            tags={**self.tags, "success": str(exc_type is None)}
        )
        return False  # Don't suppress exceptions


class StructuredLogger:
    """Structured logging with context"""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.context: Dict[str, Any] = {}

    def add_context(self, **kwargs):
        """Add context to all log messages"""
        self.context.update(kwargs)

    def clear_context(self):
        """Clear context"""
        self.context = {}

    def _log(self, level: int, message: str, **kwargs):
        """Log with structured data"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": logging.getLevelName(level),
            "message": message,
            "context": self.context,
            **kwargs
        }
        self.logger.log(level, json.dumps(log_data))

    def debug(self, message: str, **kwargs):
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, error: Optional[Exception] = None, **kwargs):
        if error:
            kwargs["error"] = {
                "type": type(error).__name__,
                "message": str(error),
            }
        self._log(logging.ERROR, message, **kwargs)


def main():
    """Example usage"""
    print("=== Observability Hooks Example ===\n")

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Create metrics collector
    metrics = MetricsCollector()

    # Create structured logger
    logger = StructuredLogger("my_service")
    logger.add_context(request_id="req_123", user_id="user_456")

    print("1. METRICS COLLECTION")
    print("-" * 60)

    # Increment counter
    metrics.increment("requests_total", tags={"endpoint": "/api/users", "method": "GET"})
    metrics.increment("requests_total", tags={"endpoint": "/api/users", "method": "POST"})

    # Set gauge
    metrics.gauge("active_connections", 42, tags={"server": "web-01"})

    # Record histogram (timing example)
    with TimingContext(metrics, "database_query", tags={"table": "users"}):
        time.sleep(0.1)  # Simulate query

    print(f"Collected {len(metrics.get_metrics())} metrics")
    print("\nPrometheus Export:")
    print(metrics.export_prometheus())

    print("\n2. STRUCTURED LOGGING")
    print("-" * 60)

    logger.info("Processing request", action="fetch_user", user_id="user_789")
    logger.warning("Rate limit approaching", current=90, limit=100)

    try:
        raise ValueError("Database connection failed")
    except ValueError as e:
        logger.error("Operation failed", error=e, operation="db_query")

    print("\n3. TIMING EXAMPLE")
    print("-" * 60)

    with TimingContext(metrics, "process_items", tags={"batch_size": "100"}):
        time.sleep(0.05)  # Simulate processing

    # Show timing metric
    timing_metrics = [m for m in metrics.get_metrics() if "duration" in m.name]
    for metric in timing_metrics:
        print(f"{metric.name}: {metric.value:.3f}s (tags: {metric.tags})")


if __name__ == "__main__":
    main()
