# Stacker Agent (`stacker_agent.py`)

## Description
The `StackerAgent` is the central "Decision Aggregator" of the Sovereign OS. It weighs evidence from multiple disparate sources (Market Scanners, Macro Regimes, Options Flow, Sentiment) and only triggers a trade when a statistical confidence threshold is met.

## Role in Department
It acts as the "Jury" that evaluates the "Evidence" provided by other agents. It is the final decision point before the `ProtectorAgent` validates the risk.

## Aggregation Logic (The Stack)
Weights signals from various sources (defaults):
- **SearcherAgent**: 30%
- **HMM Engine (Macro)**: 35%
- **FFT Engine (Freq)**: 20%
- **Options Flow (Whale Detection)**: 25%
- **ProtectorAgent**: 15% (Negative signals/Risk warnings carry heavy weight)

## Input & Output
- **Input**: `SIGNAL` events, `OPTIONS_FLOW` events, and `MACRO_REGIME` updates.
- **Output**: `TRADE_SIGNAL` when the aggregate confidence exceeds the `CONFIDENCE_THRESHOLD` (typically 0.65).

## Integration & Persistence
- **Neo4j**: Persists Whale Flow and Macro Regimes as nodes in the global knowledge graph to build historical context.
- **Kafka**: Listens for signals across the entire system and emits high-confidence execution calls.
