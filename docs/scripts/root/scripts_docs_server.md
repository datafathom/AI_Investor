# Script: docs_server.py

## Overview
`docs_server.py` is a FastAPI-based documentation hosting service. It serves the project's internal Markdown documentation and provides a structured API for browsing the documentation tree.

## Core Functionality
- **File System API**:
  - `/api/tree`: Returns a JSON representation of the `docs/` directory structure, including nested folders and file metadata.
  - `/api/content/{filepath}`: Streams the content of specific documentation files to the frontend viewer.
- **Static Assets**: Mounts the `docs/viewer/dist` directory to serve the pre-built React documentation viewer.
- **Internal Integration**: Specifically designed to work with the project's documentation infrastructure, including the `_PLANS` and `scripts` documentation folders.

## Technical Details
- **CORSMiddleware**: Configured to allow cross-origin requests, facilitating local development and integration with other internal portals.
- **Port Management**: Default to port `5055`.

## Usage
```bash
python scripts/docs_server.py
```

## Status
**Essential (Infrastructure)**: Provides the interactive portal used by the team to access architectural guidelines, sprint plans, and technical specifications.
