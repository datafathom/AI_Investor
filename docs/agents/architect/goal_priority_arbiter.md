# Goal Priority Arbiter (Agent 2.6)

## ID: `goal_priority_arbiter`

## Role & Objective
The strategic decision-maker. It acts as the final judge of competing financial priorities, determining how surplus capital should be allocated across the user's defined goals.

## Logic & Algorithm
1. **Priority Hierarchy**: Ranks user goals from "Essential" to "Luxury".
2. **Trade-Off Simulation**: Models the impact of prioritizing one goal over another (e.g., "Retiring 2 years early" vs "Buying a luxury car").
3. **Optimality Scoring**: Grades the current savings plan on its mathematical alignment with the user's weighted goals.

## Inputs & Outputs
- **Inputs**:
  - Goal List (Amount & Date)
  - Surplus Monthly Cash Flow
- **Outputs**:
  - Goal Alignment Score
  - Trade-Off Impact Map

## Acceptance Criteria
- Trade-off analysis must complete in under 500ms to allow interactive "What-If" sliders in the GUI.
- The arbiter must flag any "Essential" goals that are at risk based on the current burn rate.
