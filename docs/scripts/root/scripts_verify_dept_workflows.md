# Script: verify_dept_workflows.py

## Overview
`verify_dept_workflows.py` is a Selenium-based verification tool for department-specific action buttons and workflows.

## Core Functionality
- **UI Interaction**: Navigates through key department pages (Orchestrator, Trader, Physicist) and specifically searches for "action" buttons defined in those departments (e.g., "COMMAND INTERPRETER", "SNIPER", "THETA COLLECTOR").
- **Workflow Stability**: Ensures that clicking these buttons (or their mere presence) doesn't trigger component crashes and that the "industrial" metric panels are correctly populated.

## Status
**Essential (UI Verification)**: Validates the interactive core of the Department-centric OS interface.
