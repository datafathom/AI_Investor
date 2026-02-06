# AI Investor Project Folder Structure

This document provides a verbose description of every directory and file in the AI Investor project root.

## Core Directories

### AI_Investor/agents/
Contains the core logic for all AI agents in the system.
- **Inheritance**: All agents inherit from `BaseAgent`.
- **Funneling**: Agent prompts are funneled through `services.system.prompt_loader.PromptLoader`. Prompts are stored in `agents/prompts/prompts.json` and are dynamically loaded with injection protection.
- **Subdirectories**:
  - `prompts/`: Stores the dynamic prompt templates in JSON format.
  - `factory/`: Logic for instantiating specific agents.




==================================
### AI_Investor/apis/
Houses the API route definitions and controllers.
- **Framework**: Primarily uses FastAPI or FastAPI depending on the service.
- **Organization**: Endpoints are grouped by domain (e.g., `trading`, `compliance`, `billing`).


==================================
### AI_Investor/config/
Centralized configuration management.
- **Key Files**:
  - `cli_configuration.json`: Maps CLI commands to their respective runner functions.
  - `system_config.json`: General system parameters.
  - `secret_mapping.json`: Defines how secrets are pulled from the `SecretManager`.


==================================
### AI_Investor/docs/
Project documentation, organized for consumption by the team's internal webapp.
- **Subdirectories**:
  - `cli/`: Manuals and unification guides for the `cli.py` tool.
  - `coverage/`: Comprehensive test coverage reports.
  - `testing/`: Guides for manual and automated verification.
  - `launch/`: Readiness checklists and pre-flight reports.


==================================
### AI_Investor/frontend2/
The main frontend client application.
- **Tech Stack**: React.js with functional components and hooks.
- **State Management**: Uses the Context API for global state.


==================================
### AI_Investor/infra/
Infrastructure-as-Code (IaC) and deployment configurations.
- **Contents**: Docker Compose files, Kubernetes manifests, and environment-specific provisioning scripts.


==================================
### AI_Investor/logs/
The central repository for all system-generated logs and transient diagnostic files.
- **Contents**:
  - `*.log`: Application-level logs.
  - `*.txt`: Transient audit reports and debugging outputs.
  - `*.json`: Structured error and audit reports.


==================================
### AI_Investor/migrations/
Database evolution scripts.
- **Targets**: PostgreSQL (Alembic), TimescaleDB, and Neo4j Cypher migrations.


==================================
### AI_Investor/models/
Data models and schemas used across the application.
- **Contents**: SQLAlchemy models for persistence and Pydantic schemas for data validation/API contracts.


==================================
### AI_Investor/services/
The core business logic layer of the application.
- **Pattern**: Implements a Singleton pattern for all service-level managers.
- **Subdirectories**:
  - `system/`: Core orchestrators like `SecretManager`, `TracingService`, and `HousekeepingService`.
  - `financial/`: Specialized logic for trading, risk, and compliance.


==================================
### AI_Investor/tests/
The automated testing suite.
- **Categorization**:
  - `unit/`: Isolated logic testing for individual components.
  - `integration/`: Testing interactions between services and external boundaries (e.g., Kafka, DB).
  - `system/`: End-to-end and browser-based verification (Selenium).


==================================
### AI_Investor/scripts/
Utilities and archived development artifacts.
- **Subdirectories**:
  - `util/`: Stable, non-phase-specific utility scripts.
  - `runners/`: Handler logic for all `cli.py` commands.
  - `archive/`: Legacy phase scripts and one-off development tasks.

### AI_Investor/analysis/
Specialized mathematical and financial modeling logic.
- **Contents**: Jupyter notebooks and Python scripts for Monte Carlo simulations, HMM (Hidden Markov Models), and FFT (Fast Fourier Transform) analysis.

==================================
### AI_Investor/backups/
Automated and manual snapshots of critical configuration and research data.

==================================
### AI_Investor/data/
Local storage for static assets, mock database dumps, and temporary processing buffers.

==================================
### AI_Investor/hedging_engine/
Advanced derivative and hedging logic.
- **Purpose**: Calculates optimal hedging ratios and manages liquidity risks for complex portfolios.

==================================
### AI_Investor/mobile/
Source code for the cross-platform mobile application.

==================================
### AI_Investor/neo4j/
Graph database configuration.
- **Contents**: Cypher scripts for graph schema definitions and spatial logic for relationship mapping.


==================================
### AI_Investor/notes/
Knowledge base and developer documentation.
- **Contents**: 
  - `Project_Folder_Structure.md`: This comprehensive index.
  - `All_Frontend_Routes.txt`: A plain text list of all application paths.
  - `All_Frontend_Routes.json`: Detailed metadata for every frontend route, including descriptions and security status.
  - Other architectural decision logs and design patterns.


==================================
### AI_Investor/plans/
Implementation roadmaps and sprint planning artifacts.


==================================
### AI_Investor/queries/
Repository of raw SQL and Cypher queries used by the service layer.


==================================
### AI_Investor/schemas/
Centralized API response and request schemas.
- **Funneling**: Often used by `models` and `apis` for strict type enforcement during I/O operations.


==================================
### AI_Investor/screenshots/
Visual logs from automated browser tests.


==================================
### AI_Investor/utils/
Shared utility library for basic operations (e.g., date formatting, string manipulation).


==================================
### AI_Investor/web/
Legacy web assets or public-facing documentation components.

==================================
### AI_Investor/DEBUGGING/
Active investigation and break-fix laboratory.
- **Contents**: Temporary scripts and logs used for real-time debugging of complex production or development issues that do not fall under standard tests.

---


==================================
## Technical & Hidden Directories (Internal)

### .agent/
Custom configuration and instruction directory for the Antigravity AI agentic workflow.
- **Purpose**: Primarily used by the agent to store persistent session state, workflow definitions, and instructions specifically for this project.

==================================
### .git/
The core repository metadata for Git version control.
- **Note**: This is an internal directory managed by Git; it contains the entire history of the project's source code evolution.

==================================
### .github/
Centralized configuration for GitHub-specific features.
- **Workflow Automation**: Contains YAML files in `.github/workflows/` that define the CI/CD pipelines (e.g., automated testing and linting on every push).

==================================
### .pytest_cache/
Performance optimization directory for the project's test suite.
- **Mechanism**: Stores information about previous test runs to speed up subsequent executions by only re-running affected tests.

==================================
### .vscode/
Project-level settings and debugging configurations for Visual Studio Code.
- **Integration**: Defines task runners, debug targets, and workspace-specific extension settings to ensure consistency across developer environments.

==================================
### venv/
The Python Virtual Environment.
- **Isolation**: Manages all project dependencies separately from the system-wide Python installation, ensuring that the project runs with the exact versions of libraries specified in `requirements.txt`.
- **Note**: Should always be activated before running any project-specific Python commands.

---


==================================
## Root Files

### AI_Investor/cli.py
The unified entry point for all project commands.
- **Funneling**: Logic is funneled through `scripts/runners/` based on mappings in `config/cli_configuration.json`.
- **Usage**: `./venv/Scripts/python.exe cli.py <command>`.

### GEMINI.md
The system definition and behavioral rulebook for the Antigravity AI assistant. Contains critical coding standards and workflow requirements.

### README.md
The primary landing page and high-level overview of the AI Investor platform. Contains project descriptions and general instructions.

==================================
### .env
Contains local environment variables and secrets.
- **Security**: Never committed to version control. Used by `SecretManager` and other services to load sensitive credentials like API keys and database passwords.

==================================
### .env.template
A master reference for all required environment variables.
- **Documentation**: Provides a blueprint for developers to create their own `.env` file without exposing actual production secrets.

==================================
### .gitignore
Defines patterns of files and directories that Git should ignore.
- **Maintenance**: Crucial for keeping the repository clean of build artifacts, local logs, and sensitive `.env` files.

==================================
### .dockerignore
Optimizes the Docker build process by excluding unnecessary files from the container context.
- **Efficiency**: Prevents copying heavy folders like `venv/` or `.git/` into the Docker image, leading to faster and smaller builds.

==================================
### .coveragerc
Configuration file for `coverage.py`.
- **Testing Logic**: Defines which files should be included or excluded from code coverage calculations.

==================================
### pytest.ini
The global configuration file for the Pytest testing framework.
- **Execution**: Sets default CLI options, test discovery patterns, and custom markers for the entire test suite.

==================================
### .gitleaks.toml
Security policy configuration for Gitleaks.
- **Audit**: Defines regex patterns to detect and prevent secrets, passwords, or tokens from being accidentally committed to the repository history.
