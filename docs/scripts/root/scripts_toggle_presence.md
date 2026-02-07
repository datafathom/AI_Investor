# Script: toggle_presence.py

## Overview
`toggle_presence.py` is a helper utility for the Slack bot to manage its online visibility.

## Core Functionality
- **Presence Management**: Directly calls the `users.setPresence` Slack API to switch the bot's status between `auto` (online) and `away`.

## Usage
```bash
python scripts/toggle_presence.py --state away
```

## Status
**Support Utility**: Helpful for signaling bot availability to users during maintenance or development windows.
