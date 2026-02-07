# Script: verify_expanded_roles.py

## Overview
`verify_expanded_roles.py` ensures that all 13+ parent roles are correctly represented on the Missions Board and their workstations are accessible.

## Core Functionality
- **Role Presence Audit**: specific check for the new role tiers (Auditor, Envoy, Hunter, etc.) on the mission selection screen.
- **Dynamic Routing Test**: verify that navigating to a dynamically generated workstation path (like `/strategist/builder`) loads the correct component without white-screening.

## Status
**Essential (Verification)**: Validates the successful rollout of the expanded "Sovereign OS" role hierarchy.
