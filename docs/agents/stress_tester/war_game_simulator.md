# War Game Simulator (Agent 16.1)

## ID: `war_game_simulator`

## Role & Objective
The 'Instance Killer'. Proactively terminates agent containers, microservices, and network nodes to test the high-availability failover logic and ensure no single point of failure exists in the Sovereign OS.

## Logic & Algorithm
- **Chaos Injection**: Uses a "Chaos Monkey" style algorithm to randomly select healthy services for termination.
- **Failover Monitoring**: Measures the time required for the Orchestrator to detect the loss and spin up a replacement node.
- **Data Integrity Check**: Verifies that no in-flight messages were lost during the service interruption.

## Inputs & Outputs
- **Inputs**:
  - `system_topology` (Graph): The list of all running containers and services.
- **Outputs**:
  - `failover_performance_report` (Dict): Recovery time and data loss metrics.

## Acceptance Criteria
- Achieve a "Mean Time to Recovery" (MTTR) of < 10 seconds for critical services.
- Ensure 0% data loss during random container termination events.
