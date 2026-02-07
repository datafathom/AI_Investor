# CLI: Slack Notifications & Bot Control

## Overview
The `slack` command group in the AI Investor CLI provides granular control over the Slack integration, enabling both automated alerts and interactive bot features.

---

## Commands

### 1. `slack start`
Starts the Slack bot listener using Bolt and Socket Mode.
- **Action**: Spawns a background process that listens for Slack events.
- **Registry**: `scripts.runners.slack_runner:start_bot`
- **Behavior**: Also triggers `_ensure_worker_running()` in `SlackService` to ensure the job queue is ready.

### 2. `slack stop`
Stops all Slack-related background processes.
- **Action**: Terminates the bot listener and the standalone worker.
- **Registry**: `scripts.runners.slack_runner:stop_bot`

### 3. `slack send`
Sends a one-off notification to the default Slack channel.
- **Arguments**:
  - `message` (required): The text content to send.
- **Flags**:
  - `--level` (default: `info`): Severity level (`info`, `success`, `warning`, `critical`).
- **Usage**:
  ```powershell
  python cli.py slack send "System rebalance triggered" --level success
  ```

### 4. `slack complete`
Sends a task completion alert with a summary.
- **Arguments**:
  - `task` (required): Name of the completed task.
  - `summary` (required): Brief description of the results.
- **Usage**:
  ```powershell
  python cli.py slack complete "Weekly Audit" "All 49 schemas documented successfully."
  ```

### 5. `slack ask`
Requests human input via Slack. This is used for decision points that require human oversight.
- **Arguments**:
  - `prompt` (required): The question or action required.
  - `context` (optional): Additional background information.
- **Behavior**: Sends a `warning` level alert to ensure it catches the attention of a human operator.

---

## Configuration
All Slack CLI behaviors are managed via:
1. **Environment Variables**: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_CHANNEL_ID`.
2. **Command Registry**: `config/cli_configuration.json`.
3. **Bot Configuration**: `config/slackbot_config.json`.
