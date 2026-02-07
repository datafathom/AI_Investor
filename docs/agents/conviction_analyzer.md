# Conviction Analyzer Agent (`conviction_analyzer_agent.py`)

## Description
The `ConvictionAnalyzerAgent` is a high-level strategic agent that identifies "Sure Thing" investment opportunities. It looks for fundamental moats, specific catalysts, and market dislocations.

## Role in Department
It acts as the "Architect" of aggressive plays, identifying opportunities that warrant leverage and higher position sizing.

## Input & Output
- **Input**: Symbol, news context, market data, and qualitative indicators (e.g., "technology lead", "government contract").
- **Output**: `ConvictionAnalysis` with a thesis, recommended leverage (up to 2x), and suggested allocation.

## Decision Criteria
- **Moat Detection**: Identifies "Technology Corner" (NVIDIA), "Network Effects" (Visa), and "Regulatory Capture" (PBMs).
- **Catalyst Detection**: Monitors for government contracts, market panic, or misread earnings.
- **Conviction Scoring**: Levels range from LOW to SURE_THING.

## Pipelines & Integration
- **Stacker Agent**: Feeds high-conviction signals to the `StackerAgent` for final trade aggregation.
- **Portfolio Manager**: Recommendations are used to adjust position sizing within the Aggressive vs. Defensive portfolios.
