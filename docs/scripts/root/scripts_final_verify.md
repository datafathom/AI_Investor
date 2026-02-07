# Script: final_verify.py

## Overview
`final_verify.py` is an advanced Selenium script dedicated to verifying the "Strategy" dashboard's runtime state. It uses CDP-based authentication injection and specific DOM checks.

## Core Functionality
- **Auth Bypass**: Uses `driver.execute_cdp_cmd` to inject a `localStorage` setup script that executes before the page loads. This is more robust than standard `driver.execute_script` which runs after the page has begun loading.
- **Content Verification**: Checks for the presence of a `<canvas>` element (indicating the 3D strategy engine is active) and specific text markers like "ACTIVE STEWARDSHIP".
- **Screenshot Evidence**: Captures `strategy_final_verify.png` as proof of successful rendering.

## Usage
```bash
python scripts/final_verify.py
```

## Status
**Essential**: One of the most robust verification scripts in the project, used to prove the most complex dashboard is fully operational.
