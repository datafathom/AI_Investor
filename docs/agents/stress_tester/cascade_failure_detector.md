# Cascade Failure Detector (Agent 16.4)

## ID: `cascade_failure_detector`

## Role & Objective
The 'Flash Crowd' simulator. Floods individual components (API Gateway, DB, Workers) with 1,000x normal request volume to find the breaking point and test horizontal autoscaling.

## Logic & Algorithm
- **Load Generation**: Uses distributed stress-testing tools (e.g., Locust or JMeter) to hammer the system with concurrent requests.
- **Resource Profiling**: Monitors CPU, Memory, and Disk I/O to identify which process fails first under pressure.
- **Circuit Breaker Audit**: Verifies that the system "Fails Gracefully" by shutting down non-critical UI features while preserving the core trade-engine.

## Inputs & Outputs
- **Inputs**:
  - `target_service_endpoints` (List).
- **Outputs**:
  - `load_test_report` (Dict): Throughput (RPS), Error Rate, and Scaling latency.

## Acceptance Criteria
- Identify the "Maximum Capacity" of the API gateway within a 5% error margin.
- Successfully scale from 1 to 10 worker nodes in < 60 seconds under 80% CPU load.
