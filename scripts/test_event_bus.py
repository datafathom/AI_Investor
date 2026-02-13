import requests
import time
import random
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5050/api/v1/admin/event-bus"

TOPICS = [
    # Market Data
    "market.data.tick.aapl",
    "market.data.tick.googl",
    "market.data.tick.btc",
    "market.analysis.trend",
    
    # Portfolio Management
    "portfolio.position.update",
    "portfolio.rebalance.signal",
    "portfolio.pnl.alert",
    
    # Risk Engine
    "risk.limit.breach",
    "risk.calculation.var",
    "risk.exposure.warning",
    
    # Agents
    "agent.sentiment.result",
    "agent.execution.order",
    "agent.status.heartbeat",
    
    # Compliance & System
    "compliance.audit.log",
    "system.resource.cpu",
    "system.resource.memory",
    "security.auth.login"
]

def emit_event():
    topic = random.choice(TOPICS)
    
    payload = {
        "timestamp": datetime.now().isoformat(),
        "source": "test_script",
        "priority": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
        "data": {
            "value": random.random() * 100,
            "metric": "cpu_load" if "health" in topic else "price",
            "message": f"Test event for {topic}"
        }
    }
    
    try:
        url = f"{BASE_URL}/topics/{topic}/replay"
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print(f"✅ Sent event to [{topic}]: {response.status_code}")
        else:
            print(f"❌ Failed to send to [{topic}]: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print(f"🚀 Starting Event Bus Test Emitter targeting {BASE_URL}")
    print("Press Ctrl+C to stop...")
    
    count = 0
    try:
        while True:
            emit_event()
            count += 1
            time.sleep(1)  # Send one event every second
            
            if count % 10 == 0:
                print(f"--- Sent {count} events ---")
                
    except KeyboardInterrupt:
        print("\n🛑 Stopped test emitter.")
