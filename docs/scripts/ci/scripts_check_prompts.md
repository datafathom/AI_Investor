# Script: check_prompts.py

## Overview
`check_prompts.py` is a CI enforcer that prevents hardcoded LLM prompts from being committed to the codebase.

## Core Functionality
- **Prompt Detection**: Uses refined regex patterns to find long string assignments or "You are..." patterns inside agent Python files.
- **Externalization Requirement**: enforce the project rule that all prompts must be stored in `agents/prompts/prompts.json` to allow for versioning and non-code updates.
- **CI Failure**: Exits with code `1` if any hardcoded prompts are detected, blocking the pull request.

## Usage
```bash
python scripts/ci/check_prompts.py
```

## Status
**Essential (CI)**: Mandatory for maintaining clean separation between agent logic and agent personality/configuration.
