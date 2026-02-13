# Frontend Usage Guide

How to consume WebSocket events in React components.

## 1. Connection Logic

We use `socket.io-client`. Most of the complexity is handled by the `apiClient` and Vite proxy.

```javascript
import { io } from "socket.io-client";

// The path defaults to /socket.io, which is proxied by Vite
const socket = io("/admin/event-bus", {
  transports: ["websocket", "polling"],
});

socket.on("connect", () => console.log("Connected!"));
```

## 2. Shared Patterns: EventBusMonitor

The `EventBusMonitor.jsx` provides a reference implementation for:
- Defensive polling (ensure requests don't stack up during lag).
- Manual reconnection buttons.
- State-driven stats filtering.

## 3. Creating a Custom Listener

If you need to listen to events on a new page (e.g., a "Real-time Risk Dashboard"):

```javascript
useEffect(() => {
  const socket = io("/admin/event-bus");
  
  socket.on("event", (data) => {
    // data.topic -> "risk.limit.breach"
    // data.payload -> { priority: "CRITICAL", ... }
    processEvent(data);
  });

  return () => socket.disconnect();
}, []);
```

## 4. Key Security Considerations

- **Namespaces**: Don't leak admin topics to the root namespace.
- **Filtering**: Always filter by `priority` using the `payload.priority` field (not top-level).
- **EPS Management**: High-throughput topics (e.g., market ticks) should be throttled in the UI to prevent browser lag.

## 5. Mocking Data

Use `scripts/test_event_bus.py` to generate sample traffic. It uses the REST API `POST /api/v1/admin/event-bus/topics/{topic}/replay` to inject payloads into the live stream.
