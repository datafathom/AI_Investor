# Utility: API and Metadata Extraction

## Overview
Extraction utilities parse the source code to generate structured metadata about the system's external interfaces.

## Key Utilities

### [extract_api_routes.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/extract_api_routes.py)
The core extractor that scans Flask/FastAPI blueprints to generate the `api_routes.json` manifest. It identifies endpoints, methods, and docstrings.

### [categorize_cli.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/categorize_cli.py)
Parses the CLI configuration to group commands into functional modules (e.g., "Network", "Database", "AI") for reporting and documentation purposes.

### [list_postman_folders.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/scripts/util/list_postman_folders.py)
Synchronizes the local API structure with Postman collection folders to facilitate automated API testing.

## Status
**Essential (Metadata)**: forms the data foundation for automated documentation and test generation.
