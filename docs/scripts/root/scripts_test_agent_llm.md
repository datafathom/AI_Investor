# Script: test_agent_llm.py

## Overview
`test_agent_llm.py` is a specialized test runner for verifying the LLM integration of individual agents.

## Core Functionality
- **Isolated Prompt Testing**: Invokes an agent's `process_event` or `generate_response` method using a mock LLM provider to verify that prompt templates are correctly filled and the agent logic handles various LLM outputs predictably.

## Status
**Essential (Testing)**: Used to debug agent reasoning and prompt engineering without consuming actual API credits.
