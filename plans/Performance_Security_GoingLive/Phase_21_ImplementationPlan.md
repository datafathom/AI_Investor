# Phase 21: WebSocket Horizontal Scaling
> **Phase ID**: 21
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Enable the platform's real-time communication system (Socket.IO) to scale horizontally across multiple backend instances. This is achieved by implementing a Redis-backed Pub/Sub adapter, allowing messages to be broadcast to all connected clients regardless of which server node they are connected to.

## Objectives
- [ ] Install `python-socketio[redis]` dependencies.
- [ ] Implement `RedisAdapter` for Flask-SocketIO in `app.py`.
- [ ] Configure **Session Stickiness** (Sticky Sessions) requirements for load balancers.
- [ ] Add horizontal scaling tests using multiple local port simulations.
- [ ] Create a "WebSocket Health" monitor widget to track connection stability across nodes.

## Files to Modify/Create
1.  `web/app.py` (Initialize Redis adapter for SocketIO)
2.  `services/system/socket_manager.py` (Centralize socket logic)
3.  `plans/Performance_Security_GoingLive/Phase_21_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Redis Pub/Sub**: Use Redis as the message broker between different Flask server instances.
- **Adapter**: `flask_socketio.RedisManager` will be used to synchronize multi-process/multi-server communication.

## Verification Plan
### Automated Tests
- `tests/system/test_socket_scaling.py`: Spin up two mock servers and ensure a message sent to one is received by a client on the other.

### Manual Verification
1. Open two browser tabs connected to different simulated backend ports.
2. Trigger an event and verify both receive the update in real-time.
