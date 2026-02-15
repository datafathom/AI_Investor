# Traffic Controller (Agent 1.3)

## ID: `traffic_controller`

## Role & Objective
The systemic safeguard for the message bus. It monitors the health of the Kafka infrastructure and manages backpressure to prevent "event-flooding" during market high-volatility events.

## Logic & Algorithm
1. **Lag Monitoring**: Tracks real-time consumer lag on critical topics (e.g., `market.live`).
2. **Backpressure Trigger**: Automatically activates message throttling if lag cross the 200ms safety threshold.
3. **Routing Optimization**: Dynamically re-prioritizes high-importance signals (e.g., Flash-Crash alerts) over routine logging.

## Inputs & Outputs
- **Inputs**:
  - Kafka Consumer Metrics
  - System Throughput Stats
- **Outputs**:
  - Backpressure Status (BOOLEAN)
  - Route Optimization Signals

## Acceptance Criteria
- Maintain consumer lag < 200ms during message spikes of up to 5,000 msg/sec.
- Backpressure state must propagate to all 18 departments within 50ms of activation.
