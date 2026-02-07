# Script: slack_worker.py

## Overview
`slack_worker.py` is a standalone background worker process dedicated to handling asynchronous Slack-based operations. It acts as a bridge between the main application services and the Slack API, processing job requests sequentially to avoid rate limiting and race conditions.

## Core Functionality
- **Job Polling**: continuously monitors a file-based bridge (`.slack_kafka_bridge.jsonl`) for new job requests. While the system is designed for Kafka, this bridge allows for resilient operation without a full message broker.
- **Sequential Processing**: ensures that only one Slack job is processed at a time using a lock-file mechanism. This is critical for maintaining correct message threading and avoiding Slack API rate limits.
- **Status Updates**: Updates the state of the job bridge to reflect the current status of each task (Queued -> In Progress -> Completed/Error).
- **Liveness Heartbeat**: Maintains a `.slack_worker_alive` file with a timestamp, allowing monitoring systems to verify that the worker process is still polling and healthy.
- **Graceful Shutdown**: Handles termination signals to ensure that any in-progress Slack messages are finalized before the process exits.

## Technical Details
- **Error Handling**: Implements robust retry logic for Slack API calls, specifically handling network timeouts and temporary service unavailability.
- **Logging**: Detailed logging of every job processed, including the payload summary and the eventual result (e.g., message timestamp, destination channel).

## Usage
Standardly started via the CLI:
```bash
python cli.py slack start
```
Or manually for debugging:
```bash
python scripts/slack_worker.py
```

## Status
**Essential (Infrastructure)**: Provides the vital link for all asynchronous notifications, alert dispatching, and interactive bot commands. Without this worker, the system's ability to communicate with human operators via Slack is disabled.
