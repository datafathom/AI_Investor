# web/websocket/__init__.py
"""WebSocket gateway modules for real-time communications."""

from .department_gateway import (
    get_dept_sio,
    get_dept_socket_app,
    dept_broadcaster,
    broadcast_agent_status,
    broadcast_metrics,
    broadcast_event,
    get_department_connection_count
)

__all__ = [
    'get_dept_sio',
    'get_dept_socket_app',
    'dept_broadcaster',
    'broadcast_agent_status',
    'broadcast_metrics',
    'broadcast_event',
    'get_department_connection_count'
]
