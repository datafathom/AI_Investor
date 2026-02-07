# Script: slack_verify_bot.py

## Overview
`slack_verify_bot.py` is a health-check script for the Slack bot integration.

## Core Functionality
- **Connection Test**: verify that the bot can connect to the Slack WebSocket (RTM/Socket Mode) and respond to a simple ping or health command.
- **Permission Audit**: checks if the current token has all required scopes for production operations.

## Status
**Essential (Diagnostics)**: the first check performed when Slack notifications fail to appear.
