# Script: websocket_load_test.py

## Overview
`websocket_load_test.py` is a high-concurrency performance testing tool for the Department Gateway's WebSocket infrastructure.

## Core Functionality
- **Concurrent Simulation**: Uses `python-socketio` and dedicated asyncio tasks to simulate up to 100+ concurrent clients connecting to the server.
- **Room Subscription**: Each simulated client subscribes to a specific department room (e.g., Dept 1) and listens for broadcast events (heartbeats, agent status updates).
- **Metric Collection**: measures connection times, message throughput, and failure rates during a sustained load period.

## Usage
```bash
python scripts/websocket_load_test.py --clients 100 --dept 1 --duration 30
```

## Status
**Essential (Performance)**: Mandatory for validating that the real-time notification layer can handle the load of a large organizational mission without significant latency or connection drops.
