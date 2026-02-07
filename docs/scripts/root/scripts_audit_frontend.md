# Script: audit_frontend.py

## Overview
`audit_frontend.py` is a comprehensive Selenium-based automation script used to audit clinical health and visual stability of all frontend routes in the AI Investor application. It ensures that every page loads without SEVERE console errors and captures visual proof of correctness.

## Core Functionality
- **Route Discovery**: Iterates through a predefined list of 50+ routes, including special operations, department dashboards, and account settings.
- **Automated Verification**:
  - Sets up a headless Chrome instance.
  - Bypasses authentication via LocalStorage injection.
  - Navigates to each route and waits for page load ($MAX\_RETRIES$ for stability).
  - Captures and filters browser console logs for `SEVERE` errors.
  - Saves screenshots for both successful and failed navigations.
- **Reporting**: Generates a JSON summary of the audit results and a text-based summary report.

## Technical Architecture
- **Selenium & WebDriver Manager**: Automatically manages the ChromeDriver installation.
- **Async Wait Logic**: Implements retry logic for flaky routes and explicit waits for React component hydration.
- **Noise Filtering**: Cleans console logs by removing common warnings (e.g., source map errors, dev server noise) to focus on breaking issues.

## Configuration
- `BASE_URL`: Defaults to `http://127.0.0.1:5173`.
- `OUTPUT_DIR`: Results are stored in a timestamped folder in `notes/FrontEndAudit_...`.
- `MAX_RETRIES`: Set to 4 attempts for improved reliability under high load.

## Usage
```bash
python scripts/audit_frontend.py
```

## Status
**Essential**: This is the primary verification tool for frontend-backend integration. It identifies broken dashboards, failed API calls, and React rendering crashes across the entire UI.
