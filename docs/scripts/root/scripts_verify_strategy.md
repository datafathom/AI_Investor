# Script: verify_strategy.py

## Overview
`verify_strategy.py` is a simple variant of the Strategy verification script.

## Core Functionality
- **Page Load Check**: Navigates to `/analytics/strategy`, handles the login modal if present, and waits for the page source to stabilize.
- **Console Capture**: dumps the browser console to the terminal.

## Status
**Support Utility**: A simpler, less restrictive version of `final_verify.py` used for quick sanity checks during active development of the Strategy page.
