# AI Investor: Slack Application

## Overview
The AI Investor Slack application provides a command-and-control interface for the Sovereign OS. It allows team members to monitor system health, trigger intensive background jobs, and receive real-time alerts through a secure, Socket Mode-enabled bot.

---

## Architecture

The Slack integration is designed for reliability and asynchronous processing:

1. **`SlackService` (Services Layer)**: The core brain that manages the `bolt-python` lifecycle, handles Socket Mode connections, and maps Slack patterns to internal actions.
2. **`slack_worker.py` (Standalone Worker)**: A background process that polls a job queue and executes long-running tasks, ensuring the main bot listener remains responsive.
3. **`File-Based Bridge`**: A temporary transition layer (`.slack_kafka_bridge.jsonl`) that decouples the bot listener from the worker.
4. **`Socket Mode`**: Enables the bot to communicate with Slack without needing a public HTTP endpoint, making it ideal for firewalled or localhost development environments.

---

## Core Components

### 1. Bot Listener (`SlackService`)
- **Location**: `services/notifications/slack_service.py`
- **Role**: Maintains the active connection to Slack.
- **Security**: Filters commands based on the `SLACK_ALLOWED_USERS` environment variable.
- **Catch-up Logic**: Automatically processes missed messages from its offline period upon startup.
- **Presence Heartbeat**: Periodically re-asserts "Online" status to maintain visibility in the Slack client.

### 2. Standalone Worker (`slack_worker.py`)
- **Location**: `scripts/slack_worker.py`
- **Role**: Processes the job queue.
- **Running Standalone**: 
  ```powershell
  # Requires project root in PYTHONPATH
  $env:PYTHONPATH="."
  python scripts/slack_worker.py
  ```
- **Capabilities**:
  - Handles sequential job processing.
  - Updates job status in real-time (`Queued` -> `Started` -> `Completed`).
  - Sends progress notifications back to the originating Slack channel.

### 3. CLI Integration
- **Command**: `python cli.py slack [subcommand]`
- **Subcommands**:
  - `start`: Launches the Slack bot listener.
  - `stop`: Terminates the background processes.
  - `send --message "text"`: Broadcasts a manual notification.
  - `ask --prompt "question"`: Requests human intervention for high-stakes decisions.

---

## The Job Queue System

The "Job Queue" allows heavy computations or multi-stage workflows to be triggered directly from Slack.

### How it Works:
1. **Trigger**: A user sends a message like `!job test start`.
2. **Recognition**: `SlackService` matches the `!job` pattern from `config/slackbot_config.json`.
3. **Dispatch**: The service publishes a JSON payload to `.slack_kafka_bridge.jsonl`.
4. **Pick-up**: `slack_worker.py` detects the new entry, marks it as `Started`, and begins execution.
5. **Completion**: Once finished, the worker marks the job as `Completed` in `.slack_jobs_active` and notifies the user.

### Queue Configuration
Jobs are defined in `config/slackbot_config.json` under the `kafka_dispatch` action.

---

## Administrative Commands

| Command | Action | Description |
|---------|--------|-------------|
| `!health` | `service_call` | Returns a summary of Backend, Docker, and Gateway status. |
| `!risk` | `service_call` | Shows daily VaR (Value at Risk) and Circuit Breaker status. |
| `!nuke` | `service_call` | (Restricted) Clears all messages in the current channel. |
| `!portfolio` | `service_call` | Displays current paper trading account balance and positions. |

---

## Troubleshooting & Maintenance

- **Worker Logs**: Located at `logs/slack_worker.log`.
- **Worker Heartbeat**: Check `.slack_worker_alive` for the last successful poll timestamp.
- **Active Jobs Tracker**: View `.slack_jobs_active` to see the current state of all pending or running jobs.
- **Visibility Issues**: If the green "Online" dot is missing, ensure the bot is started and the `presence_heartbeat` loop is running in `SlackService`.
