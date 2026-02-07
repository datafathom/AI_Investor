# CLI Orchestration (`cli.py`)

The AI Investor CLI is the "Sovereign Control Panel." It provides a unified interface for managing every aspect of the project, from infrastructure setup to agent debugging.

## Core Component: `cli.py`

The CLI is a metadata-driven dispatcher. Instead of hardcoding logic, it reads from a global configuration and routes commands to specialized "Runners."

### Command Registry (`config/cli_configuration.json`)
Every command available in the system is registered here. The registry defines:
- **Command Name & Category**: For help documentation.
- **Handler**: The exact Python function to execute (e.g., `scripts.runners.dev_runner:start_dev_mode`).
- **Arguments & Flags**: Typed inputs with defaults and help text.
- **Post-Handlers**: Sequential cleanup or notification tasks.

## Key Operational Modes

### 1. Developer Modes
The CLI provides three distinct modes for starting the environment:
- **`python cli.py dev`**: Standard mode. Starts hot-reloading Backend (5050) and Frontend (5173).
- **`python cli.py dev-full`**: Starts all Docker infrastructure, then the dev environment.
- **`python cli.py dev-no-db`**: Lightweight mode. Starts only the UI and API (assumes DB is at a remote LAN IP).

### 2. Infrastructure Management (`docker`)
Wraps `docker-compose` to manage the lifecycle of the data layer:
- `python cli.py docker up`: Start Postgres, Redis, Kafka, Neo4j.
- `python cli.py docker down`: Graceful stop and optional volume purge (`-v`).

### 3. Systematic Controls
- **`stop-all`**: Gracefully terminates all backend and frontend runners.
- **`reset-dev`**: A "Nuke and Pave" command that stops, clears, restarts, and re-seeds the environment.
- **`check-runtimes`**: Verification tool to ensure required ports are active.

## Execution Flow
1. **Invocation**: User runs `python cli.py <cmd>`.
2. **Registry Lookup**: `CommandRegistry` loads the configuration and finds the handler.
3. **Lazy Import**: The handler module is imported only when needed to keep the CLI fast.
4. **Validation**: Arguments are parsed and validated against the registry definition.
5. **Dispatch**: The handler is executed with the provided arguments.
6. **Telemetry**: Success or failure is logged via the `UnifiedActivityService`.
