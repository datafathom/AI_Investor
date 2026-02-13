# Backend Usage Guide

How to interact with the Event Bus from Python services, agents, and API routers.

## 1. Publishing Events

Use the `EventBusService` singleton to publish events.

```python
from services.infrastructure.event_bus import EventBusService

eb = EventBusService()

# Topic structure: department.feature.action (e.g., risk.limit.breach)
eb.publish("risk.limit.breach", {
    "priority": "CRITICAL",  # Convention: LOW, MEDIUM, HIGH, CRITICAL
    "source": "RiskEngine",
    "data": {
        "limit_id": "L-99",
        "current_value": 1500,
        "max_value": 1000
    }
})
```

## 2. Subscribing to Events

You can subscribe to specific topics or all topics (global listener).

### Specific Topic
```python
def on_risk_breach(payload):
    print(f"ALARM: {payload}")

eb.subscribe("risk.limit.breach", on_risk_breach)
```

### Global Listener (Architecture Level)
Used for broadcasting to external systems like WebSockets.

```python
def global_handler(topic, payload):
    # Log or broadcast
    pass

eb.add_global_listener(global_handler)
```

## 3. Topic Registration

Topics are usually "lazily" initialized. When you publish to a new topic string, the `EventBusService` automatically creates the history and stats buffers for it.

## 4. Stability Best Practices

> [!WARNING]
> Avoid performing blocking I/O (like synchronous DB calls) inside an event handler, as it will block the entire Event Bus propagation thread. Use background tasks or async patterns if heavy processing is required.
