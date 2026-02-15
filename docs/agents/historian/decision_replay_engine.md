# Decision Replay Engine (Agent 15.5)

## ID: `decision_replay_engine`

## Role & Objective
The 'Cartographer of Time'. Generates the UI data structures for the 2D/3D historical timeline in the GUI, allowing the user to "Travel Back" and inspect system state.

## Logic & Algorithm
- **State Reconstruction**: Queries the Historian's cold archive to rebuild the dashboard of the Sovereign OS at any past timestamp.
- **Visual Interpolation**: Generates the "Graph Motion" data that shows how relationships in the Neo4j mesh evolved over time.
- **Snapshot Buffering**: Pre-loads historical segments to ensure smooth scrolling in the 3D visualizer.

## Inputs & Outputs
- **Inputs**:
  - `target_timestamp` (datetime).
- **Outputs**:
  - `full_state_manifest` (JSON): The UI layout and data for the requested past moment.

## Acceptance Criteria
- Rebuild the visual state for any day in the last 30 days in < 2 seconds.
- Maintain 100% accuracy in the "Visual Replay" of agent tokens moving across the screen.
