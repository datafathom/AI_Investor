# Backend Service: Kafka (Real-Time Streaming)

## Overview
The **Kafka Service** is the high-throughput asynchronous backbone of the Sovereign OS. It facilitates the real-time movement of "Market Bytes" and "Agent Signals" across the distributed architecture. By utilizing a robust **Base Consumer** framework with integrated circuit breakers, the service ensures that the platform can process tens of thousands of price updates, order book shifts, and inter-agent communications every second with minimal latency and high fault tolerance.

## Core Components

### 1. Unified Consumer Framework (`consumer.py`)
The platform's standardized entry point for event-driven logic.
- **Base Consumer Class**: Implements background polling, threading, and deserialization for all agents. It features a built-in **Circuit Breaker** that halts consumption if more than 10 consecutive errors occur, protecting the system from cascading failures during network instability.
- **Domain Consumers**: Provides specialized listeners for `market.vix` (Volatility Update), `market.equity` (Price Feed), and `agent.signals` (Inter-Agent Messaging).

### 2. High-Fidelity Orderbook Streamer (`orderbook_consumer.py`)
Processes Level 2 Depth-of-Book data in real-time.
- **Liquidity Analysis**: Aggregates bid/ask depth to identify significant imbalances (e.g., >50% sell-side pressure).
- **Market Microstructure**: Forwards high-fidelity book summaries to risk engines and the trading terminal, enabling precision execution based on available liquidity.

### 3. Graph Correlation Bridge (`graph_bridge.py`)
Synchronizes the streaming layer with the relationship graph (Neo4j).
- **Dynamic Correlation Engine**: Consumes price updates for FX and Equity pairs and recalculates Pearson correlation coefficients on-the-fly using a rolling history window.
- **Graph Persistence**: Updates the "Edge Weights" (Correlation Strength) in the Neo4j graph, allowing the platform to visualize the real-time "Nervous System" of the global market.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Trading Terminal** | Level 2 Orderbook Depth | `orderbook_consumer.latest_books` |
| **Market Intelligence** | Real-time Correlation Graph | `graph_bridge.process_message()` (Edge weights) |
| **System Monitor** | Consumer Health Pulse | `base_consumer.health_check()` |
| **Whale Watch Terminal** | Institutional Block Signal Feed| `kafka.consumer` (Signals) |
| **Mission Control** | Volatility (VIX) Ticker | `vix_consumer.process_message()` |

## Dependencies
- `confluent-kafka`: High-performance Python client for Apache Kafka.
- `Neo4j`: Used by the Graph Bridge to persist market correlations.
- `json`: Standard format for event serialization/deserialization.

## Usage Examples

### Implementing a Custom Market Data Consumer
```python
from services.kafka.consumer import BaseConsumer, ConsumerConfig

class MyAlphaConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers=None):
        config = ConsumerConfig(
            topics=['market.alpha.signals'],
            group_id='alpha-detection-team'
        )
        super().__init__(config, bootstrap_servers)

    def process_message(self, message):
        print(f"NEW ALPHA SIGNAL: {message['signal_id']} for {message['ticker']}")

consumer = MyAlphaConsumer()
consumer.start() # Runs in background thread
```

### Checking the Health of the Kafka Infrastructure
```python
from services.kafka.orderbook_consumer import orderbook_consumer

# Inspect the health status of the high-fidelity depth consumer
status = orderbook_consumer.health_check()

if status['healthy']:
    print(f"Depth Consumer is active on: {status['topics']}")
else:
    print(f"CRITICAL: Consumer halted after {status['error_count']} errors.")
```

### Visualizing Real-time Market Imbalance
```python
from services.kafka.orderbook_consumer import orderbook_consumer

# Fetch the latest processed book for NVIDIA
book = orderbook_consumer.get_book("NVDA")

if book:
    print(f"NVDA Bid Size: {book['total_bid_size']}")
    print(f"NVDA Ask Size: {book['total_ask_size']}")
```
