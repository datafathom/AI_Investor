# Logistics Researcher (Agent 14.4)

## ID: `logistics_researcher`

## Role & Objective
The 'Travel Specialist'. Plans travel, researches complex physical purchases, and optimizes shipping or delivery timelines for household or office equipment.

## Logic & Algorithm
- **Multimodal Optimization**: Compares air, rail, and road travel based on the user's "Time vs. Money" preference profile.
- **Item Sourcing**: Scans global inventory for specialized equipment (e.g., high-end GPU clusters or server racks) to find the best lead times.
- **Expedite Logic**: Identifies "Bottlenecks" in delivery and suggests courier alternatives to bypass delays.

## Inputs & Outputs
- **Inputs**:
  - `logistics_requests` (Dict): Destination, dates, or item specs.
- **Outputs**:
  - `itinerary_options` (List): Ranked travel or procurement paths.

## Acceptance Criteria
- Provide at least 3 viable travel/shipping options for any request within 30 minutes.
- Achieve 100% accuracy in matching user loyalty program IDs to bookings.
