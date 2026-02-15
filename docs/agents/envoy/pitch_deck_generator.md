# Pitch Deck Generator (Agent 13.6)

## ID: `pitch_deck_generator`

## Role & Objective
The 'Synthesis Architect'. Converts raw system performance data and complex deal analysis into high-fidelity PDF presentations for partners or lenders.

## Logic & Algorithm
- **Data Visualization**: Converts Polars/Pandas dataframes into D3-style charts optimized for static PDF export.
- **Executive Summary**: Uses LLMs to draft the narrative around the "Investment Thesis" or "Performance Audit."
- **Branding Enforcement**: Ensures all exported documents follow the consistent Sovereign OS visual style (Dark Mode, Grid layouts).

## Inputs & Outputs
- **Inputs**:
  - `raw_performance_data` (Dict): Returns, PnL, and Risk metrics.
  - `deal_thesis_notes` (Text): The user's subjective insights.
- **Outputs**:
  - `branded_partnership_deck` (PDF): A professional investment presentation.

## Acceptance Criteria
- Generate a 10-slide performance deck in < 60 seconds given a data source.
- Maintain 100% consistency across fonts, colors, and chart styles for institutional-grade output.
