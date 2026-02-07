# Script: migrate_stores.py

## Overview
`migrate_stores.py` is a frontend utility for migrating Zustand stores to use the `storageAdapter`.

## Core Functionality
- **Persistence Layer Update**: Refactors the `persist` middleware configuration in Zustand stores to use a custom `storageAdapter` instead of the default LocalStorage. This allows for more granular control over serialization and encryption of stored state.

## Status
**Essential (Architecture)**: Key to implementing the system-wide security requirement for encrypted state persistence in the browser.
