# Chaos Agent (`chaos_agent.py`)

## Description
The `ChaosAgent` is the "Joker" of the system, responsible for resilience testing. It proactively injects faults into the Sovereign OS to verify that high-availability and self-healing mechanisms are functional.

## Role in Department
Acts as a security and infrastructure auditor, simulating real-world failures to ensure the "Sovereign Kernel" can survive hardware or network instability.

## Input & Output
- **Input**: Stress test triggers (e.g., `start_stress_test`).
- **Output**: Trace events indicating the type of fault injected and the system's reaction.

## Capabilities
- **Latency Injection**: Simulates network jitter or slow API responses.
- **Consumer Lag**: Mocks Kafka lag to test the `TrafficControllerAgent`'s backpressure logic.
- **Process Termination**: Simulates container crashes (e.g., "killing" an analyst agent) to verify automatic restarts.

## Integration
- **Docker API**: In a production environment, this agent interacts with Docker to kill containers or throttle resources.
- **Observability**: Every "Chaos Event" is traced so engineers can correlate system behavior with the injected fault.
