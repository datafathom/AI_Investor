# Phase 24: Centralized Logging & Correlation (ELK/Loki Stack)
> **Phase ID**: 24
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement a centralized logging system that aggregates logs from all microservices, the database, and the message bus. This phase ensures that every log entry is enriched with a `trace_id` from Phase 23, allowing for seamless correlation between distributed traces and log messages.

## Objectives
- [ ] Configure **Structured Logging** (JSON) for the Flask backend.
- [ ] Implement a **Logging Middleware** to inject `trace_id` and `span_id` into every log entry.
- [ ] Set up a **Grafana Loki** or **ELK** stack configuration (Dockerized).
- [ ] Create a "Live System Logs" widget in the Architect/Admin views.
- [ ] Implement log-based alerting for critical errors (e.g., 500 errors > 1% threshold).

## Files to Modify/Create
1.  `services/system/logging_service.py` **[NEW]**
2.  `web/app.py` (Register logging middleware)
3.  `config/loki_config.yaml` **[NEW]**
4.  `plans/Performance_Security_GoingLive/Phase_24_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Structured Logging**: Use `python-json-logger` to format logs as JSON, making them easily searchable in Loki/Elasticsearch.
- **Correlation**: Use OpenTelemetry's context to extract the current `trace_id` and add it to the log record extras.

## Verification Plan
### Automated Tests
- Trigger an error and verify that the resulting log entry contains the correct `trace_id` matching the distributed trace.

### Manual Verification
1. Inspect logs in the terminal/files and confirm JSON format.
2. View the Loki dashboard and search for a specific `trace_id` to see all related log entries.
