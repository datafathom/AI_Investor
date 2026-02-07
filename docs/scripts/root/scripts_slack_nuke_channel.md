# Script: slack_nuke_channel.py

## Overview
`slack_nuke_channel.py` is a powerful administrative utility for clearing all message history from a specific Slack channel.

## Core Functionality
- **Mass Deletion**: Iterates through the message history of a specified channel via the Slack Web API and deletes every message. 
- **Safety**: Requires explicit confirmation and the `admin` scope on the Slack token.

## Usage
```bash
python scripts/slack_nuke_channel.py --channel C12345678
```

## Status
**Essential (Administrative)**: Used during testing phases to reset the Slack environment before a clean integration run.
