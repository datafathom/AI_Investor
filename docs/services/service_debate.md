# Backend Service: Debate

## Overview
The **Debate Service** acts as the platform's "Decision Forensics" layer. It is responsible for recording the complete, immutable reasoning trail behind every AI-driven investment decision. By capturing the granular votes, dissenting opinions, and logical justifications of the multi-agent workforce, it provides the transparency required for institutional-grade AI governance.

## Core Components

### 1. Forensics Logger (`forensics_logger.py`)
The platform's "Black Box" recorder for agentic reasoning.
- **Decision Persistence**: Captures every investment proposal, the final decision (Buy/Sell/Hold), and the specific JSON-serialized votes of every agent involved in the debate.
- **Dissent Tracking**: Specifically records dissenting votes and the reasoning behind them, which is critical for post-trade analysis and understanding "edge case" risks that a majority consensus might have overlooked.
- **Audit Trails**: Links debate records to `proposal_id` and `symbol` for quick retrieval during compliance audits or performance reviews.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Admin Audit Console** | Decision Timeline | `forensics_logger.log_debate()` (Retrieved via DB) |
| **Market Terminal** | Agent Dissent Heatmap | `forensics_logger.log_debate()` |
| **Portfolio Detail** | "Why did we buy this?" Modal | `debate_logs` (Forensics retrieval) |
| **Compliance Station** | Regulatory Reporting | `forensics_logger.log_debate()` |

## Dependencies
- `utils.database_manager`: Handles the persistence of debate records to the central Postgres `debate_logs` table.
- `json`: Used to serialize complex multi-agent voting structures into queryable JSONB fields.

## Usage Examples

### Recording a Multi-Agent Decision Trail
```python
from services.debate.forensics_logger import forensics_logger

# Example multi-agent vote results
votes = [
    {"agent": "Strategist", "vote": "BUY", "confidence": 0.9, "reason": "Undervalued FCF"},
    {"agent": "Risk_Mgr", "vote": "HOLD", "confidence": 0.6, "reason": "Macro tailwinds unclear"},
    {"agent": "Market_Analyst", "vote": "BUY", "confidence": 0.85, "reason": "Bullish RSI breakout"}
]

# Log the outcome to the forensics database
forensics_logger.log_debate(
    proposal_id="PROP-7721-AAPL",
    symbol="AAPL",
    decision="BUY",
    votes=votes,
    metadata={"market_volatility": "Low", "model_version": "v2.1.0"}
)
```
