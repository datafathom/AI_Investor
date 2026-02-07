# Script: generate_api_docs.py

## Overview
`generate_api_docs.py` is an automated documentation generator that transforms the `api_routes.json` manifest into human-readable Markdown documentation.

## Core Functionality
- **Transformation**: Iterates through the list of API endpoints and generates a structured Markdown file for each category.
- **Content Enrichment**: Includes information about authentication requirements, expected methods, and error codes.
- **Output Management**: populates the `docs/api/` directory with the generated files.

## Status
**Essential (Documentation)**: Ensures that API documentation remains in sync with the actual implementation by deriving it from the source-of-truth manifest.
