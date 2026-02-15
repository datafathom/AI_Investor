# Flash Crash Circuit Breaker (Agent 5.6)

## ID: `flash_crash_circuit_breaker`

## Role & Objective
The "Emergency Stop". The ultimate safeguard that halts all trading activity if extreme, non-human market anomalies or system failures are detected.

## Logic & Algorithm
1. **SOT Monitoring**: Tracks the "Speed of Tape"—identifying vertical, high-velocity price drops indicative of a flash crash.
2. **Desync Detection**: Monitors if venue prices are diverging significantly, indicating a broken feed.
3. **Kill Switch**: Issues a system-wide SIGKILL to all execution-level agents if thresholds are breached.

## Inputs & Outputs
- **Inputs**:
  - `global_price_stream` (Dict): Live ticker data.
  - `venue_health_status` (Dict): Network health.
- **Outputs**:
  - `system_halt_signal` (bool): Halt flag.
  - `reason_code` (str): e.g., 'FLASH_CRASH_DETECTED'.

## Acceptance Criteria
- Halt signal must propagate to the execution engine in < 5ms of detection.
- Circuit breaker must be "latched"—requiring manual human reset after a halt.
