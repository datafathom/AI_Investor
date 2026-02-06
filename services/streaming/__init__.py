# services/streaming/__init__.py
"""Streaming services for real-time data processing."""

from .kafka_dept_consumer import (
    KafkaDepartmentConsumer,
    get_dept_consumer,
    start_dept_consumer
)

__all__ = [
    'KafkaDepartmentConsumer',
    'get_dept_consumer',
    'start_dept_consumer'
]
