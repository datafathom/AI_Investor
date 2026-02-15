# Mistake Classifier (Agent 12.6)

## ID: `mistake_classifier`

## Role & Objective
The 'Memory Optimizer'. Tags every loss with a specific mistake type for the Historian, turning failures into educational data points.

## Logic & Algorithm
- **Taxonomy Mapping**: Uses ML to categorize losing trades into types: "FOMO", "Faded Trend", "Oversized", "News Front-run", etc.
- **Pattern Learning**: Identifies if a specific "Mistake Type" is recurring more frequently than others.
- **Feedback Loop**: Passes high-frequency mistake patterns to the Data Scientist to retrain the predictive models.

## Inputs & Outputs
- **Inputs**:
  - `realized_trades` (List): Trade outcomes and justifications.
- **Outputs**:
  - `error_taxonomy_tag` (str): The specific mistake classification.

## Acceptance Criteria
- Categorize 100% of realized losses within 24 hours of trade exit.
- Maintain a "Clustering Report" of the top 3 mistake types by dollar impact.
