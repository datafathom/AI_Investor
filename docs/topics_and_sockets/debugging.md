# Troubleshooting & Debugging

Common issues and solutions for the Messaging/WebSocket system.

## 1. Socket.IO Connection Failures ("OFFLINE")

### Cause: Backend Hang (Kafka)
In `dev-no-db` mode, the backend may try to connect to a non-existent Kafka broker.
- **Symptom**: `python cli.py check-backend` returns a timeout.
- **Solution**: Check `services/kafka/admin_client.py`. Ensure the timeout is LOW (e.g., 2s). We implemented this to prevent the event loop from blocking.

### Cause: Proxy Mismatch
Vite acts as a proxy for WebSockets.
- **Symptom**: Console error "Connection refused for http://localhost:5173/socket.io".
- **Solution**: Verify `vite.config.js` has `ws: true` in the `/socket.io` proxy config. Ensure the frontend is connecting to `127.0.0.1:5050` if the relative proxy is failing.

## 2. Empty Topic List

### Cause: No Publishers
Topics are created when events are published.
- **Solution**: Run `python scripts/test_event_bus.py` to populate the bus.

### Cause: Singleton Initialization
The `EventBusService` must be initialized before the Broadcaster starts.
- **Solution**: Confirm `fastapi_gateway.py` calls `start_event_bus_broadcast()` during startup.

## 3. Missing Events in UI

### Cause: Payload Structure
Filters expect `priority` inside the payload.
- **Bad Payload**: `{ "topic": "x", "priority": "HIGH" }`
- **Good Payload**: `{ "topic": "x", "payload": { "priority": "HIGH", "data": {} } }`

## 4. Performance: EPS Spikes
High message volume can lag the React render loop.
- **Solution**: Use `useMemo` for filtering and avoid setting state inside high-frequency `on("event")` handlers without throttling if the message volume is $>100/sec$.
