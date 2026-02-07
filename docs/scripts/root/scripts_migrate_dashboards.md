# Script: migrate_dashboards.py

## Overview
`migrate_dashboards.py` is a frontend refactoring utility used to transition dashboard components to a new storage architecture.

## Core Functionality
- **API Transition**: Replaces legacy state management calls with the new `StorageService` API.
- **Component Refactoring**: Updates the data-fetching and persistence logic in React components to use the centralized storage adapter, ensuring consistent data handling across all dashboards.

## Status
**Essential (Migration)**: Crucial for maintaining frontend performance and reliability by unifying how dashboards interact with the persistence layer.
