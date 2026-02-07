# Phase 6: Real-time Integration

> **Duration**: 3 Weeks  
> **Status**: [ ] Not Started  
> **Dependencies**: Phase 1-4 Complete  
> **Owner**: TBD  

---

## Phase Overview

Implement Kafka event streaming and WebSocket gateway for real-time department metrics, agent status updates, and cross-department communication.

---

## Deliverables Checklist

### 6.1 Kafka Topic Structure
- [ ] Topics created per schema
- [ ] Retention policies configured
- [ ] Consumer groups defined

### 6.2 Backend Kafka Service
- [ ] Producer singleton
- [ ] Consumer service
- [ ] Error handling + DLQ

### 6.3 WebSocket Gateway
- [ ] FastAPI WebSocket endpoints
- [ ] JWT authentication
- [ ] Room-based subscriptions
- [ ] Heartbeat mechanism

### 6.4 Frontend WebSocket Hook
- [ ] `useDepartmentSocket` hook
- [ ] Auto-reconnect logic
- [ ] Message parsing

---

## Deliverable 6.1: Kafka Topic Structure

### Topic Schema

```
# Department Events
dept.{1-18}.events       # General dept events      (retention: 7d)
dept.{1-18}.metrics      # Performance metrics      (retention: 24h)
dept.{1-18}.agents       # Agent status updates     (retention: 1h)

# Cross-Department
telemetry.stream         # Unified telemetry        (retention: 24h)
system.alerts            # High-priority alerts     (retention: 30d)
system.commands          # Global commands          (retention: 1d)

# Audit
audit.agent_invocations  # Agent call logs          (retention: 90d)
audit.user_actions       # User action logs         (retention: 90d)
```

### Topic Configuration

```yaml
# docker/kafka/topics.yaml
topics:
  - name: dept.1.events
    partitions: 3
    replication_factor: 1
    config:
      retention.ms: 604800000  # 7 days
      cleanup.policy: delete

  - name: telemetry.stream
    partitions: 6
    replication_factor: 1
    config:
      retention.ms: 86400000  # 24 hours
      cleanup.policy: delete

  - name: system.alerts
    partitions: 1
    replication_factor: 1
    config:
      retention.ms: 2592000000  # 30 days
      cleanup.policy: delete
```

---

## Deliverable 6.2: Backend Kafka Service

### File: `services/kafka_service.py`

```python
"""
Kafka Service - Singleton for message production and consumption
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.errors import KafkaError

logger = logging.getLogger(__name__)


class KafkaService:
    """Async Kafka producer and consumer service."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._producer: Optional[AIOKafkaProducer] = None
        self._consumers: Dict[str, AIOKafkaConsumer] = {}
        self._bootstrap_servers = "kafka-broker:9092"
        self._handlers: Dict[str, List[Callable]] = {}
    
    async def start(self):
        """Initialize Kafka producer."""
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            enable_idempotence=True
        )
        await self._producer.start()
        logger.info("Kafka producer started")
    
    async def stop(self):
        """Shutdown all connections."""
        if self._producer:
            await self._producer.stop()
        
        for consumer in self._consumers.values():
            await consumer.stop()
        
        logger.info("Kafka connections closed")
    
    async def produce(
        self, 
        topic: str, 
        message: Dict[str, Any],
        key: Optional[str] = None
    ) -> None:
        """Produce message to topic."""
        if not self._producer:
            await self.start()
        
        try:
            await self._producer.send_and_wait(topic, message, key=key)
        except KafkaError as e:
            logger.exception(f"Failed to produce to {topic}: {e}")
            raise
    
    async def subscribe(
        self,
        topics: List[str],
        group_id: str,
        handler: Callable[[str, Dict], None]
    ) -> None:
        """Subscribe to topics with handler callback."""
        consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=self._bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )
        
        await consumer.start()
        self._consumers[group_id] = consumer
        
        # Start consumer loop
        asyncio.create_task(self._consume_loop(consumer, handler))
        
        logger.info(f"Subscribed to {topics} with group {group_id}")
    
    async def _consume_loop(
        self,
        consumer: AIOKafkaConsumer,
        handler: Callable
    ) -> None:
        """Background consumer loop."""
        try:
            async for msg in consumer:
                try:
                    await handler(msg.topic, msg.value)
                except Exception as e:
                    logger.exception(f"Handler error: {e}")
                    # Send to DLQ
                    await self.produce(
                        'dlq.errors',
                        {
                            'original_topic': msg.topic,
                            'message': msg.value,
                            'error': str(e)
                        }
                    )
        except asyncio.CancelledError:
            logger.info("Consumer cancelled")


# Department-specific helpers
async def publish_department_event(dept_id: int, event_type: str, data: Dict) -> None:
    """Helper to publish department events."""
    kafka = KafkaService()
    await kafka.produce(
        f"dept.{dept_id}.events",
        {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


async def publish_agent_status(dept_id: int, agent_id: str, status: str) -> None:
    """Helper to publish agent status updates."""
    kafka = KafkaService()
    await kafka.produce(
        f"dept.{dept_id}.agents",
        {
            "agent_id": agent_id,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )
```

---

## Deliverable 6.3: WebSocket Gateway

### File: `web/websocket/department_gateway.py`

```python
"""
WebSocket Gateway for Department Real-time Updates
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect, Depends, Query
from services.kafka_service import KafkaService
from services.auth_service import verify_websocket_token

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections per department."""
    
    def __init__(self):
        # dept_id -> set of WebSocket connections
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # ws -> user_id for tracking
        self.connection_users: Dict[WebSocket, str] = {}
    
    async def connect(
        self, 
        websocket: WebSocket, 
        dept_id: int,
        user_id: str
    ) -> None:
        await websocket.accept()
        
        if dept_id not in self.active_connections:
            self.active_connections[dept_id] = set()
        
        self.active_connections[dept_id].add(websocket)
        self.connection_users[websocket] = user_id
        
        logger.info(f"User {user_id} connected to dept {dept_id}")
    
    def disconnect(self, websocket: WebSocket, dept_id: int) -> None:
        if dept_id in self.active_connections:
            self.active_connections[dept_id].discard(websocket)
        
        user_id = self.connection_users.pop(websocket, None)
        logger.info(f"User {user_id} disconnected from dept {dept_id}")
    
    async def broadcast_to_department(
        self, 
        dept_id: int, 
        message: Dict
    ) -> None:
        """Send message to all connections in a department."""
        if dept_id not in self.active_connections:
            return
        
        dead_connections = []
        
        for connection in self.active_connections[dept_id]:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)
        
        # Clean up dead connections
        for conn in dead_connections:
            self.disconnect(conn, dept_id)
    
    async def broadcast_global(self, message: Dict) -> None:
        """Send message to all department connections."""
        for dept_id in self.active_connections:
            await self.broadcast_to_department(dept_id, message)


manager = ConnectionManager()


# FastAPI WebSocket endpoint
@router.websocket("/ws/departments/{dept_id}")
async def department_websocket(
    websocket: WebSocket,
    dept_id: int,
    token: str = Query(...)
):
    """
    WebSocket endpoint for department real-time updates.
    
    Connect: wss://host/ws/departments/5?token=JWT_TOKEN
    
    Messages sent:
    - { type: "metrics", data: {...} }
    - { type: "agent_status", data: {...} }
    - { type: "alert", data: {...} }
    
    Messages received:
    - { type: "subscribe", topics: ["metrics", "agents"] }
    - { type: "ping" }
    """
    # Verify JWT
    try:
        user = await verify_websocket_token(token)
    except Exception as e:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    await manager.connect(websocket, dept_id, user.id)
    
    # Start heartbeat task
    heartbeat_task = asyncio.create_task(
        send_heartbeat(websocket)
    )
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif data.get("type") == "subscribe":
                # Handle subscription changes
                pass
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, dept_id)
        heartbeat_task.cancel()
    except Exception as e:
        logger.exception(f"WebSocket error: {e}")
        manager.disconnect(websocket, dept_id)
        heartbeat_task.cancel()


async def send_heartbeat(websocket: WebSocket):
    """Send heartbeat every 30 seconds."""
    while True:
        try:
            await asyncio.sleep(30)
            await websocket.send_json({
                "type": "heartbeat",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        except Exception:
            break


# Kafka -> WebSocket bridge
async def kafka_to_websocket_bridge():
    """Bridge Kafka messages to WebSocket clients."""
    kafka = KafkaService()
    
    async def handler(topic: str, message: Dict):
        # Extract dept_id from topic (e.g., "dept.5.metrics")
        parts = topic.split('.')
        if len(parts) >= 2 and parts[0] == 'dept':
            dept_id = int(parts[1])
            await manager.broadcast_to_department(dept_id, message)
    
    # Subscribe to all department topics
    topics = [f"dept.{i}.metrics" for i in range(1, 19)]
    topics += [f"dept.{i}.agents" for i in range(1, 19)]
    
    await kafka.subscribe(
        topics=topics,
        group_id="websocket-bridge",
        handler=handler
    )
```

---

## Deliverable 6.4: Frontend WebSocket Hook

### File: `frontend/src/hooks/useDepartmentSocket.js`

```javascript
import { useEffect, useRef, useCallback, useState } from 'react';
import { useAuthStore } from '@/stores/authStore';

const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
const RECONNECT_DELAY = 3000;
const MAX_RECONNECT_ATTEMPTS = 5;

/**
 * Hook for subscribing to department WebSocket updates
 * 
 * @param {number} departmentId - Department ID to subscribe to
 * @param {function} onMessage - Callback for incoming messages
 * @returns {object} - Connection state and send function
 */
export const useDepartmentSocket = (departmentId, onMessage) => {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const wsRef = useRef(null);
  const reconnectAttempts = useRef(0);
  const token = useAuthStore(s => s.token);
  
  const connect = useCallback(() => {
    if (!token || !departmentId) return;
    
    const url = `${WS_BASE_URL}/ws/departments/${departmentId}?token=${token}`;
    
    try {
      const ws = new WebSocket(url);
      wsRef.current = ws;
      
      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        reconnectAttempts.current = 0;
        console.log(`WebSocket connected to dept ${departmentId}`);
        
        // Subscribe to updates
        ws.send(JSON.stringify({
          type: 'subscribe',
          topics: ['metrics', 'agents', 'alerts']
        }));
      };
      
      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          
          // Handle heartbeat
          if (message.type === 'heartbeat') {
            return;
          }
          
          // Pass to callback
          onMessage?.(message);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };
      
      ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError('Connection error');
      };
      
      ws.onclose = (event) => {
        setIsConnected(false);
        wsRef.current = null;
        
        if (event.code !== 1000) {
          // Abnormal close - attempt reconnect
          if (reconnectAttempts.current < MAX_RECONNECT_ATTEMPTS) {
            reconnectAttempts.current++;
            console.log(`Reconnecting (${reconnectAttempts.current}/${MAX_RECONNECT_ATTEMPTS})...`);
            setTimeout(connect, RECONNECT_DELAY);
          } else {
            setError('Max reconnection attempts reached');
          }
        }
      };
    } catch (e) {
      setError(e.message);
    }
  }, [departmentId, token, onMessage]);
  
  // Connect on mount, disconnect on unmount
  useEffect(() => {
    connect();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close(1000, 'Component unmounted');
      }
    };
  }, [connect]);
  
  // Send message function
  const send = useCallback((message) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);
  
  return {
    isConnected,
    error,
    send
  };
};

export default useDepartmentSocket;
```

### Usage Example

```jsx
// In DeptTrader.jsx
import { useDepartmentSocket } from '@/hooks/useDepartmentSocket';
import { useDepartmentStore } from '@/stores/departmentStore';

const DeptTrader = () => {
  const updateMetrics = useDepartmentStore(s => s.updateDepartmentMetrics);
  
  const { isConnected, error } = useDepartmentSocket(5, (message) => {
    if (message.type === 'metrics') {
      updateMetrics(5, message.data);
    }
    
    if (message.type === 'agent_status') {
      // Update agent status in store
    }
    
    if (message.type === 'alert') {
      toast.warning(message.data.message);
    }
  });
  
  return (
    <div>
      <span className={isConnected ? 'status-live' : 'status-offline'}>
        {isConnected ? '● LIVE' : '○ OFFLINE'}
      </span>
      {/* Rest of component */}
    </div>
  );
};
```

---

## E2E Definition of Done

1. **Kafka**: All topics created with correct retention
2. **Producer**: `python -c "from services.kafka_service import KafkaService; ..."` works
3. **WebSocket**: Connect via browser DevTools Network tab
4. **Auth**: Invalid token returns 4001 close code
5. **Heartbeat**: Ping/pong every 30s visible in DevTools
6. **Reconnect**: Killing server triggers auto-reconnect
7. **Load**: 100 concurrent connections supported per department

---

## Phase Sign-Off

- [ ] Kafka topics created and tested
- [ ] WebSocket gateway deployed
- [ ] Frontend hook working with auto-reconnect
- [ ] Metrics updating in real-time on dashboards
- [ ] No memory leaks from unclosed connections
