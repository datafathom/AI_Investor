# Backend Service: Evolution

## Overview
The **Evolution Service** is the platform's self-improvement and optimization laboratory. It utilizes genetic algorithms to evolve investment strategies by treating agent parameters as "genes." By performing crossover, mutation, and hybrid splicing, the service ensures that the platform's alpha-generating logic adapts to changing market regimes rather than remaining static.

## Core Components

### 1. Genetic Architect (`gene_logic.py`)
The foundational layer for strategy mutation and hybridization.
- **Crossover & Splice**: Combines "genomes" from two successful parent agents to create a hybrid offspring. It uses uniform crossover to inherit successful parameters from both sides.
- **Gene Mutation**: Applies subtle random variations to strategy parameters (e.g., tweaking an RSI threshold from 30 to 32) within safe mathematical bounds.
- **Gene Pulse**: Calculates the internal "vitality" of an agent. It tracks how often specific genes are activated in decisions and flags "volatile" genes that may be prone to drifting into unprofitable behavior.

### 2. Chronological Auditor (`playback_service.py`)
Facilitates the validation of evolved strategies in a virtual sandbox.
- **Genome Playback**: Maps genetic markers back to actionable strategy parameters and re-runs historical market cycles to see how a "mutated" agent would have performed.
- **Strategy Sandboxing**: Integrates with the `BacktestEngine` to provide a risk-free environment for testing "Generation Zero" hybrid agents before they are deployed to production environments.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Evolution Lab** | Gene Splicer Wizard | `gene_logic.splice_agents()` |
| **Evolution Lab** | Mutation Risk Heatmap | `gene_logic.get_gene_pulse()` |
| **Strategy Detail** | "Replay Master" (Backtest) | `playback_service.run_playback()` |
| **Agent Performance** | Genetic Lineage Tree | `gene_logic.splice_agents()` (Parent ID links) |
| **Research Station** | Pulse Vitality Meter | `gene_logic.get_gene_pulse()` |

## Dependencies
- `services.analysis.genetic_distillery`: Provides the base `Genome` schema for all agentic genetic material.
- `services.analysis.backtest_engine`: Used by the playback service for historical simulation.
- `uuid`: Generates unique identifiers for newly "born" hybrid agents.

## Usage Examples

### Splicing Two Successful Agents
```python
from services.evolution.gene_logic import get_gene_splicer

splicer = get_gene_splicer()

# Splicing "Strategist_V1" and "Risk_Mgr_V2"
child = splicer.splice_agents(
    parent1_id="AG-STRAT-01",
    parent2_id="AG-RISK-02",
    parent1_genes={"rsi_period": 14, "momentum_thresh": 0.8},
    parent2_genes={"stop_loss": 0.05, "rsi_period": 12},
    bounds={"rsi_period": (10, 20), "stop_loss": (0.02, 0.1)}
)

print(f"Hybrid Agent Created: {child['id']}")
print(f"Inherited Genes: {child['genes']}")
```

### Checking an Agent's Genetic Vitality
```python
from services.evolution.gene_logic import GeneSplicer

splicer = GeneSplicer()
genes = {"rsi_buy": 30, "rsi_sell": 70, "vol_spike": 1.5}

pulse = splicer.get_gene_pulse(agent_id="AGENT-X44", genes=genes)

print(f"Agent Vitality Score: {pulse['overall_vitality']*100:.1f}%")
for entry in pulse['pulse']:
    print(f"Gene: {entry['gene']} | Status: {entry['status']} (Instability: {entry['instability']})")
```
