# Kafka Topic Schemas

## Topic: `market-data`
**Purpose**: Real-time price and volume updates.
```json
{
  "symbol": "AAPL",
  "price": 150.25,
  "volume": 100,
  "timestamp": "2026-01-18T14:30:00Z",
  "source": "polygon"
}
```

## Topic: `risk-alerts`
**Purpose**: System-generated risk warnings.
```json
{
  "level": "CRITICAL",
  "message": "Exposure limit exceeded for AAPL",
  "component": "RiskEngine",
  "timestamp": "2026-01-18T14:30:00Z",
  "metadata": {
      "limit": 10000,
      "current": 10500
  }
}
```

## Topic: `agent-heartbeat`
**Purpose**: Liveness tracking for agents.
```json
{
  "agent_id": "agent-001",
  "status": "alive",
  "cpu_usage": 12.5,
  "memory_usage": 256,
  "timestamp": "2026-01-18T14:30:00Z"
}
```

## Topic: `social-sentiment`
**Purpose**: Ingested social media sentiment.
```json
{
  "source": "Reddit",
  "symbol": "GME",
  "sentiment": 0.8,
  "text": "Huge upside potential!",
  "timestamp": "2026-01-18T14:30:00Z"
}
```
