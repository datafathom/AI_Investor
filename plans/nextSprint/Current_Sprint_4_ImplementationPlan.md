# Implementation Plan: Sprint 4 - Evolution Lab

## Goal
Expand the AI training suite into a functional "Genomic Lab" for agent creation, monitoring, and splicing.

## 1. Evolution Core logic
### 1.1 Gene Splicing Engine
- **Logic**: Combine specific gene arrays (Conviction, Leverage, Exit Signals) from two successful agents.
- **Validation**: Ensure resulting "Child" agent passes syntax and sanity checks.

### 1.2 Genomic Playback
- **Logic**: Fetch historical state from the `Evolution` database and "Re-run" a specific trade cycle in a virtual sandbox.

## 2. Sprint 4 Widgets (Genomics & AI Training)
| Widget | Purpose | Technical Logic |
|--------|---------|-----------------|
| `FitnessSurface3D` | Training terrain | 3D surface plot (Three.js) showing the agent's optimization journey. |
| `GeneFrequencyPlot` | Mutation trends | Bar chart of gene prevalence across generations. |
| `MutationRateSlider` | Live speed control | Sends `SIGUSR1` or WebSocket message to backend training process. |
| `SurvivalProbabilityMeter` | MC Simulation | Runs a 1000-pass Monte Carlo to estimate agent bankruptcy risk. |
| `AncestorLineageMap` | Genetic tree | D3 Tree layout showing "Who fathered whom" in the agent pool. |
| `SplicingConflictResolver` | Diff visualizer | Side-by-side gene comparison with "Auto-Resolve" strategies. |

## 3. Acceptance Criteria
- [x] **Splicing**: Creating a "Hybrid Agent" from two parents successfully registers a new Agent ID in the registry.
- [x] **Simulation**: `FitnessSurface3D` updates real-time as the backend evolution job progresses.
- [x] **Control**: Moving the `MutationRateSlider` is reflected in the backend job logs in < 500ms.
- [x] **Lineage**: Clicking an agent in `AncestorLineageMap` shows its full "Genetic Heritage" back to the root.

## 4. Testing & Code Coverage
- **Unit Tests**:
    - `gene_logic.py`: Verify mutation and crossover algorithms.
    - `EvolutionDashboard.jsx`: Verify WebSocket event parsing and store updates.
- **E2E Tests**:
    - `test_evolution_lab.py`: Start a job, adjust mutation rate, wait for generation 10, and perform a splice.
- **Targets**:
    - 95% coverage for agent mutation logic.
    - 85% component coverage for the genomic UI suite.
