# Debate Chamber Agent (`debate_chamber_agent.py`)

## Description
The `DebateChamberAgent` orchestrates adversarial debates between multiple AI personas (e.g., The Bull vs. The Bear). It synthesizes these arguments to reach a final consensus score for a given ticker or proposal.

## Role in Department
Acts as the central "Conflict Resolution" mechanism, ensuring that every trade is viewed from multiple perspectives before execution.

## Input & Output
- **Input**: Ticker symbol or trade proposal.
- **Output**: Full debate transcript and a consensus summary (Decision: BUY/SELL/HOLD, Confidence Score, Averaged Metrics).

## Integration points
- **Persona Agents**: Leverages specialized Bull and Bear personas to generate reasoning.
- **LLM**: Uses Anthropic's Claude for high-quality dialectical synthesis.
- **Frontend**: Results are stored in the `DebateStore` for visualization in the "Debate Chamber" UI.

## Logic Flow
1. **Request Bull Argument**: Highlights momentum and growth.
2. **Request Bear Argument**: Highlights risk and headwinds.
3. **Moderator Synthesis**: Acts as the judge, weighting arguments and calculating a confidence score.
