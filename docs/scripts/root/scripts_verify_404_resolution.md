# Script: verify_404_resolution.py

## Overview
`verify_404_resolution.py` is a regression checking script focusing on previously broken API endpoints.

## Core Functionality
- **Endpoint Probing**: specifically targets a list of URLs that were known to return 404 errors in previous audits. It validates that the endpoints are now properly bound and returning valid success or error (non-404) responses.

## Status
**Essential (QC)**: ensures that routing fixes are permanent and haven't been regressed by subsequent blueprint changes.
