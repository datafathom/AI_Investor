# Script: check_conn.py

## Overview
`check_conn.py` is a lightweight diagnostic utility for performing quick connectivity checks between the development machine and the critical network services of the AI Investor stack.

## Core Functionality
- **Health Probing**: Sends HTTP GET requests to the backend health endpoint (`http://127.0.0.1:5050/health`) and the frontend development server (`http://127.0.0.1:5173`).
- **Status Reporting**: Prints the HTTP status code for each probe, allowing developers to immediately identify if a service is down or hung.

## Usage
```bash
python scripts/check_conn.py
```

## Status
**Essential (Utility)**: While simple, it is the first line of defense when debugging startup issues. It avoids the overhead of a full Selenium run to answer the question, "Is the server even up?"
