# Script: get_logs.py

## Overview
`get_logs.py` is a diagnostic utility for retrieving the most recent browser console logs from a live Chrome instance.

## Core Functionality
- **Log Extraction**: Uses Selenium to pull the browser console buffer and formats it into a clean, readable text report.
- **Filtering**: Can be configured to show only specific log levels (e.g., Error, Info).

## Status
**Essential (Debugging)**: A go-to tool for developers to quickly check what is happening inside the browser without needing to open the DevTools manually.
