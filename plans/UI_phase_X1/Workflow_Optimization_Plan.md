# Developer Workflow Optimization Plan

## Problem Statement
Current iteration cycle requires running `python cli.py demo-start` for every change. This command performs a "Full Stop & Start" (killing processes, restarting Docker containers, rebooting servers), taking 15-30+ seconds. This breaks flow and slows down verification.

**Goal**: Achieve **<1s Hot Reload** for Code Changes while maintaining **Zero Docker/Port Conflicts**.

## Proposed Solution: "Safe Hot-Reload Mode"

We will implement a new CLI command: `python cli.py dev`.

### 1. Architecture

Instead of restarting the universe, `cli.py dev` will:
1.  **Check Infrastructure**: Ensure Docker containers (Postgres, Neo4j, Kafka) are *already* running. If not, start them *once*.
2.  **Launch Backend (Hot Reload)**: run Flask/FastAPI with file-watchers enabled.
    - Command: `python -m flask --app web.app run --port 5050 --debug` (or equivalent uvicorn reload).
3.  **Launch Frontend (Hot Reload)**: Run Vite dev server.
    - Command: `npm run dev` (Vite HMR).
4.  **Process Sentinel**: The CLI script will sit and monitor these two subprocesses.
    - **CRITICAL**: On `Ctrl+C` or error, the CLI will aggressively kill the specific process trees of the backend and frontend, ensuring no zombie processes hold port 5050 or 5173.

### 2. Implementation Steps

#### A. Modify `cli.py`
Add `dev` command:
```python
@main.command()
def dev():
    """
    Developer Mode: Hot-Reload for Backend & Frontend.
    1. Checks if Infra is up (doesn't restart if healthy).
    2. Starts Backend (API) with auto-reload.
    3. Starts Frontend (UI) with HMR.
    4. Handles cleanup on exit.
    """
    # Logic to be implemented
```

#### B. Safe Cleanup Logic
Implement `cleanup_handler` that uses `psutil` to identify children of the CLI process and terminate them cleanly. This solves the user's fear of "multiple runtimes".

### 3. Usage Workflow

**Initial Setup (Once per day)**:
`python cli.py start-infra` (Starts DBs)

**Development Loop**:
1. Run `python cli.py dev`
2. **Edit Code** (Backend `py` or Frontend `jsx`).
3. **Save File**.
4. **Auto-Update**:
   - Backend restarts purely the python process (FAST, <1s).
   - Frontend updates via HMR (INSTANT, <200ms).
   - No Docker restart required.
5. **Verify**: Check Browser.

**Stopping**:
1. Press `Ctrl+C` in terminal.
2. CLI kills Python Server + Node Server.
3. Ports 5050 and 5173 are freed immediately.

## Benefits
- **Speed**: Iteration time drops from ~30s to <1s.
- **Safety**: Managed process lifecycle prevents "Address already in use" errors.
- **Focus**: User stays in the flow.

## Verification
- Verify backend reloads when `market_routes.py` is saved.
- Verify frontend updates when `HypeMeterWidget.jsx` is saved.
- Verify process list is clean after `Ctrl+C`.
