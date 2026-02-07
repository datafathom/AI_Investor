# Script: frontend_full_audit.py

## Overview
`frontend_full_audit.py` is a specialized execution of the frontend audit that uses an extended 6-second delay per route to ensure maximum stability for complex visualizations.

## Core Functionality
- **High-Latence Verification**: By using a fixed 6-second delay, it guarantees that even the heaviest 3D dashboards have enough time to finish their initial data fetch and render cycle before the audit captures the state.
- **Stability Focused**: Ideal for use in development environments where the local machine might be under high CPU load.

## Status
**Support Utility**: A more stable, albeit slower, version of the frontend audit.
