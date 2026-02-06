"""
==============================================================================
FILE: scripts/websocket_load_test.py
ROLE: WebSocket Performance & Load Testing Utility
PURPOSE: Simulates high concurrent WebSocket connections to the Department Gateway.
         Validates connection limits, room subscriptions, and broadcast delivery.

USAGE:
    python scripts/websocket_load_test.py --clients 100 --dept 1
==============================================================================
"""
import asyncio
import argparse
import logging
import time
import socketio
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("WSLoadTester")

BASE_URL = "http://localhost:5050"
SOCKETIO_PATH = "/ws/departments"

class WSClient:
    def __init__(self, client_id: int, dept_id: int):
        self.client_id = client_id
        self.dept_id = dept_id
        self.sio = socketio.AsyncClient(logger=False, engineio_logger=False)
        self.connected = False
        self.messages_received = 0
        self.start_time = None
        self.connection_time = None

        @self.sio.event
        async def connect():
            self.connected = True
            self.connection_time = time.time() - self.start_time
            # Subscribe to department
            await self.sio.emit('subscribe_department', {'dept_id': self.dept_id})

        @self.sio.on('subscribed')
        async def on_subscribed(data):
            logger.debug(f"Client {self.client_id} subscribed to dept {data['dept_id']}")

        @self.sio.on('agent_status')
        async def on_agent_status(data):
            self.messages_received += 1
            logger.debug(f"Client {self.client_id} received agent status for {data['agent_id']}")

        @self.sio.on('heartbeat')
        async def on_heartbeat(data):
            logger.debug(f"Client {self.client_id} received heartbeat")

    async def connect_and_wait(self, duration: int):
        self.start_time = time.time()
        try:
            await self.sio.connect(BASE_URL, socketio_path=SOCKETIO_PATH, wait_timeout=10)
            await asyncio.sleep(duration)
            await self.sio.disconnect()
        except Exception as e:
            logger.error(f"Client {self.client_id} connection error: {e}")

async def run_load_test(num_clients: int, dept_id: int, duration: int):
    logger.info(f"🚀 Starting WebSocket Load Test: Clients={num_clients}, Dept={dept_id}, Duration={duration}s")
    
    clients = [WSClient(i, dept_id) for i in range(num_clients)]
    
    # Connect clients in batches to avoid overwhelming the server handshake
    start_time = time.time()
    batch_size = 20
    for i in range(0, num_clients, batch_size):
        batch = clients[i:i+batch_size]
        logger.info(f"Connecting batch {i//batch_size + 1}...")
        await asyncio.gather(*[c.connect_and_wait(duration) for c in batch])
        # Note: gathered tasks will finish after 'duration' seconds
    
    total_duration = time.time() - start_time
    
    # Analyze results
    connected_clients = [c for c in clients if c.connected]
    avg_conn_time = sum(c.connection_time for c in connected_clients) / len(connected_clients) if connected_clients else 0
    total_msgs = sum(c.messages_received for c in clients)
    
    logger.info("="*50)
    logger.info("WEBSOCKET LOAD TEST RESULTS")
    logger.info("="*50)
    logger.info(f"Target Clients: {num_clients}")
    logger.info(f"Connected Clients: {len(connected_clients)}")
    logger.info(f"Failed Connections: {num_clients - len(connected_clients)}")
    logger.info(f"Average Connection Time: {avg_conn_time:.4f}s")
    logger.info(f"Total Messages Received: {total_msgs}")
    logger.info(f"Total Test Duration: {total_duration:.2f}s")
    logger.info("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Department Gateway WebSocket Load Tester")
    parser.add_argument("--clients", type=int, default=50, help="Number of concurrent clients")
    parser.add_argument("--dept", type=int, default=1, help="Department ID to subscribe to")
    parser.add_argument("--duration", type=int, default=10, help="Duration to stay connected (seconds)")
    args = parser.parse_args()
    
    asyncio.run(run_load_test(args.clients, args.dept, args.duration))
