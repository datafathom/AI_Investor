# Script: generate_agent_defs.py

## Overview
`generate_agent_defs.py` is a generator script that creates the `agent_definitions.json` file, which serves as the registry for all AI agents in the system.

## Core Functionality
- **Source Mapping**: Takes a structured Python dictionary (or hardcoded list) containing agent names, roles, goals, and capabilities.
- **JSON Serialization**: Formats this data into a schema-compliant JSON file that is consumed by the `AgentOrchestrationService` and the frontend "Missions" dashboard.

## Status
**Essential (Configuration)**: This is the single source of truth for agent identities. Any change to the agent roster must be made here and regenerated.
