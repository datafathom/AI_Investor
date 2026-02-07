# Backend Service: Streaming (The Event Bus)

## Overview
The **Streaming Service** provides real-time data pipelines using Kafka. It consumes messages from department-specific topics (events, metrics, agent status) and relays them to WebSocket clients, enabling live dashboard updates.

## Core Components

### 1. Kafka Department Consumer (`kafka_dept_consumer.py`)
- **Topic Subscription**: Subscribes to per-department topics for events, metrics, and agent status.
- **Fallback Simulation**: If Kafka is unavailable, simulates realistic department updates for development.
- **WebSocket Relay**: Integrates with `DepartmentBroadcaster` to push messages to frontend clients.

### Topic Structure
| Topic Pattern | Purpose | Retention |
| :--- | :--- | :--- |
| `dept.{id}.events` | Department events | 7 days |
| `dept.{id}.metrics` | Performance metrics | 24 hours |
| `dept.{id}.agents` | Agent status updates | 1 hour |
| `telemetry.stream` | Global telemetry | 24 hours |
| `system.alerts` | System-wide alerts | 7 days |

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Mission Control** | Live Metrics | `kafka_dept_consumer` → WebSocket | **Implemented** |
| **Agent Monitor** | Status Panel | `topic: dept.{id}.agents` | **Implemented** |

## Usage Example

```python
from services.streaming.kafka_dept_consumer import start_dept_consumer
import asyncio

async def main():
    consumer = await start_dept_consumer()
    
    def my_broadcast(dept_id, topic_type, message):
        print(f"Dept {dept_id} [{topic_type}]: {message}")
    
    consumer.set_broadcast_callback(my_broadcast)
    
    # Let it run
    await asyncio.sleep(60)
    await consumer.stop()

asyncio.run(main())
```
