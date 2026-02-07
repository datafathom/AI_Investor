# Research Agent (`research_agent.py`)

## Description
The `ResearchAgent` is responsible for conducting external market research and gathering real-world intelligence using advanced search capabilities.

## Role in Department
Acts as the "Information Scout," providing qualitative data that complements quantitative signals from price scanners.

## Input & Output
- **Input**: Natural language research queries (e.g., "What is the current regulatory outlook for ARM-based chips in China?").
- **Output**: Detailed answers with citations and confidence levels.

## Integration & Strategy
- **Perplexity Client**: Uses the Perplexity API for high-accuracy, real-time web search and citation generation.
- **History Management**: maintains an in-memory history of queries and results to build context for multi-step research missions.
- **Synthesis**: Feeds citations and summaries back to the `Orchestrator` or `ConvictionAnalyzer` for decision support.

## Singleton Pattern
Uses a Singleton pattern to ensure that the `Perplexity` client and research history are consistently managed across the session.
