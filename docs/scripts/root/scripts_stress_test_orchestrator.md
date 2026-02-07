# Script: stress_test_orchestrator.py

## Overview
`stress_test_orchestrator.py` is a performance testing utility for the Agent Orchestration Service.

## Core Functionality
- **Load Generation**: Simulates hundreds of concurrent "event bursts" to the Orchestrator to see how it handles queuing, prioritization, and dispatching to sub-agents.
- **Latency Monitoring**: measures the response time of the orchestrator under varying levels of simulated pressure.

## Status
**Essential (Performance)**: Critical for ensuring the system can handle market volatility bursts where thousands of trade signals might trigger simultaneously.
