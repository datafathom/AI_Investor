# Phase 23: Distributed Tracing Implementation
> **Phase ID**: 23
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement distributed tracing across the AI Investor's microservices architecture. This allows us to track requests as they flow from the API gateway, through various agents, into the database, and out via Kafka. Tracing is essential for identifying bottlenecks and debugging complex asynchronous workflows.

## Objectives
- [ ] Install **OpenTelemetry** SDK and instrumentation libraries.
- [ ] Set up a **Jaeger** or **Zipkin** instance (Dockerized).
- [ ] Instrument the Flask backend to start trace spans for all API requests.
- [ ] Instrument Kafka producers and consumers to propagate trace context across the event bus.
- [ ] Integrate tracing into the **System Health** dashboard for visual bottleneck analysis.

## Files to Modify/Create
1.  `requirements.txt` (Add `opentelemetry-api`, `opentelemetry-sdk`, etc.)
2.  `services/system/tracing_service.py` **[NEW]**
3.  `web/app.py` (Initialize OpenTelemetry middleware)
4.  `plans/Performance_Security_GoingLive/Phase_23_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Context Propagation**: Use W3C Trace Context headers for HTTP and Kafka headers for asynchronous events.
- **Exporting**: Export traces to a local Jaeger instance for development, with a modular exporter for production (e.g., Honeycomb or AWS X-Ray).

## Verification Plan
### Automated Tests
- Trigger a complex workflow (e.g., backtest start) and verify that a complete trace is generated in Jaeger with all spans correctly parented.

### Manual Verification
1. Open the Jaeger UI.
2. Select the `ai-investor-backend` service.
3. Inspect a trace and confirm sub-spans exist for DB queries and Kafka publishes.
