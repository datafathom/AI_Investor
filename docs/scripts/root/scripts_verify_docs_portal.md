# Script: verify_docs_portal.py

## Overview
`verify_docs_portal.py` is a stability check for the internal documentation server and its UI.

## Core Functionality
- **Liveness Check**: Connects to the docs server (port `5055`) and verifies that the main sidebar and file tree correctly load.
- **Content Integrity**: ensure that critical folders (like `_PLANS`) are correctly indexed and visible in the UI.

## Status
**Essential (Infrastructure)**: Ensures that technical teams can reliably access documentation during critical development cycles.
