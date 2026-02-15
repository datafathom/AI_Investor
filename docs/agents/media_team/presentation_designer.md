# Presentation Designer (Agent 19.6)

## ID: `presentation_designer`

## Role & Objective
The 'Slide Deck Expert'. Creates professional-grade institutional presentations and slide decks from system-generated content and insights.

## Logic & Algorithm
- **Slideware Orchestration**: Breaks high-level narratives into "Slide Units" (Title, Bullet, Chart, Image).
- **Visual Hierarchy**: Ensures that key data points are emphasized through scale and color contrast.
- **Export Management**: Generates decks in multiple formats (PPTX, PDF, Interactive HTML).

## Inputs & Outputs
- **Inputs**:
  - `deck_narrative` (Text).
  - `chart_data` (List).
- **Outputs**:
  - `presentation_file` (PPTX): Professional slide deck.

## Acceptance Criteria
- Maintain a consistent "Institutional Theme" across 100% of slides.
- Support 3+ export formats for every created deck.
