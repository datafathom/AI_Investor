# Antigravity Global Rules & Standards

## 1. Code Style & Quality
- **Python Standards**: Strictly follow **PEP 8** guidelines.
- **Type Safety**: **MANDATORY** usage of typing annotations for all function arguments and return values.
- **Paradigm**: Prioritize **Object-Oriented Programming (OOP)** and inheritance.
- **Testing**: Every new module and class **must** have accompanying unit tests.

## 2. Developer Workflow
- **Virtual Environment**: **ALWAYS** activate `venv` before running ANY Python code or pip commands (`./venv/Scripts/activate`).
- **Terminal Commands**: **NEVER** run `pip install` outside the virtual environment.
- **Dependency Management**: **IMMEDIATELY** after installing any new package, you **MUST** update `requirements.txt` (e.g., `pip freeze > requirements.txt`). Failure to do this breaks deployment.
- **Databases**: Use **Dockerized** databases exclusively. No local instances.
- **Verification**: Confirm success with **End-to-End (E2E) tests** via terminal output and/or browser.
- **Pre-Browser Check**: Before verifying in Browser, **ALWAYS** confirm the backend is responding to HTTP requests and is ready for the frontend client.
- **Port Management**: **never** use sequential ports during development. **ALWAYS** ensure previous runtimes are fully stopped and default ports are available before starting.


## 3. Architecture & Patterns
- **CLI Configuration**: All commands **must** be registered in config/cli_configuration.json and handled in scripts/runners/.
- **Agent Implementation**: Inherit from BaseAgent. Implement process_event. Wrap external calls in circuit breakers.
- **Service Layer**: Use __new__ singleton pattern for managers. Lazy load heavy connections (Neo4j, Postgres).

## 4. Stability & Error Handling
- **Exceptions**: **NEVER** use bare except:. Cleanly catch specific exceptions and use logger.exception().
- **Validation**: Validate inputs at method entry points (fail fast) using Pydantic or explicit checks.

## 5. Agentic Development Optimization
- **Context Preservation**: Keep files < 400 lines. Refactor larger files into sub-modules.
- **Documentation**: Explain **WHY** (intent), not just HOW.
- **Naming**: Use descriptive names (calculate_candidate_score >> calc_score).
- **Self-Correction**: Analyze tool errors before retrying. 

## 6. Frontend Integration
- **Components**: Use functional components with Hooks (/hooks).
- **State**: Global state must be managed via Context API (/context).
- **API**: Use strictly typed services in Frontend/src/services/. No ad-hoc fetch calls.

## 7. Data & Observability
- **Logging**: Use UnifiedActivityService.log_activity for business actions.

## 8. File Structure & Knowledge
- **Modularity**: Separate concerns into distinct files/services.
- **Knowledge Base**: Store .md notes in 
otes/ and _ExtraContext/.
- **Instructions**: Consult .instructions for behavioral rules.

## 9. Output Format
- **Presentation**: Provide **minimal diffs** or targeted blocks to maximize clarity.

## 10. Browser Automation (CRITICAL)
- **Mandatory Method**: **ALWAYS** use local Python scripts with Selenium for browser control and verification.
- **Prohibited**: **NEVER** use internal browser tools or recursive agent calls for browser interaction.
- **Implementation**: Create scripts in `scripts/` (e.g., `scripts/verify_feature.py`), run them via terminal, and inspect the screenshots they generate.
- **Drivers**: Use `webdriver_manager` for automatic driver management.
