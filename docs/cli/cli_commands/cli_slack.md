# Slack Bot & Notifications

Control the AI Investor Slack Bot, send notifications, and manage the background listener.

## Usage

```bash
python cli.py slack [subcommand] [flags]
```

## Subcommands

### `send`
Send a generic notification to the configured Slack channel.

**Arguments:**
- `message` (required): The text content to send.

**Flags:**
- `--level`: Severity level of the notification. Color codes the attachment.
    - `info` (default): Grey
    - `success`: Green
    - `warning`: Gold
    - `critical`: Red

**Example:**
```bash
python cli.py slack send "Database migration completed" --level success
```

---

### `complete`
Send a rich task completion alert. Ideal for agents to report finished work.

**Arguments:**
- `task`: Name of the task or job.
- `summary`: brief description of what was accomplished.

**Example:**
```bash
python cli.py slack complete "Data Ingestion" "Imported 500 records from AlphaVantage."
```

---

### `ask`
Request human input or decision making. Alerts the user with a distinct warning style.

**Arguments:**
- `prompt`: The question or action required from the user.
- `context` (optional): Additional details or background.

**Example:**
```bash
python cli.py slack ask "Approve Deployment?" --context "Tests passed, ready for production."
```

---

### `start`
Start the Slack Bot listener (Socket Mode) in the foreground or background.
The bot listens for:
- `@mentions`
- `ping` command
- Other interactive events

**Example:**
```bash
python cli.py slack start
```

---

### `stop`
Stop the background Slack Bot process.
Identifies the running python process executing `slack start` and terminates it.

**Example:**
```bash
python cli.py slack stop
```
