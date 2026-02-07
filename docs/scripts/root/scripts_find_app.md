# Script: find_app.py

## Overview
`find_app.py` is a utility script designed to locate FastAPI application instances within the project structure.

## Core Functionality
- **Discovery**: Automatically scans the `web/` and root directories for files containing `FastAPI()` declarations.
- **Reporting**: Identifies the module path and variable name of the application instance (e.g., `web.fastapi_gateway:app`).

## Status
**Essential (DevOps)**: Used by deployment and debugging scripts to dynamically determine the correct Uvicorn/Gunicorn entry point without hardcoding paths.
