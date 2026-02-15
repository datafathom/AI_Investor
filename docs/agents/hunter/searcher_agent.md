# Searcher Agent (`searcher_agent.py`)

## Description
Known as "The Scout," the `SearcherAgent` traverses the market and the system's internal knowledge graph (Neo4j) to identify high-liquidity paths and emerging trading opportunities.

## Role in Department
Operates as the front-line scanner for the `Trader` and `Strategist` departments, spotting patterns before the high-frequency engines engage.

## Input & Output
- **Input**: Scan triggers (sector, minimum liquidity, correlation thresholds).
- **Output**: A list of scored opportunities including symbols, identified patterns, and correlation data.

## Key Capabilities
- **Neo4j Graph Traversal**: Finds correlations and dependencies between assets (e.g., NVDA -> TSMC -> ASML).
- **Market Scanning**: Integrates with `MarketScannerService` to monitor major trading pairs in real-time.
- **Pattern Recognition**: Uses `PatternRecognition` engine to identify technical or structural market setups.

## Pipelines
- **Opportunity Scorer**: Every identified pattern is scored (0-100), and only those above a quality threshold (typically 50+) are emitted.
- **Stacker Integration**: Emitters results as `SCAN_COMPLETE` events which are picked up by the `StackerAgent`.
