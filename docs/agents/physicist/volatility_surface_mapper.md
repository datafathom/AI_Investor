# Volatility Surface Mapper (Agent 6.2)

## ID: `volatility_surface_mapper`

## Role & Objective
The "Surface Architect". This agent maps Implied Volatility (IV) across all available strikes and expiries to identify statistical mispricing in the options market.

## Logic & Algorithm
1. **Mesh Construction**: Builds a 3D visualization of IV (the 'Smile' or 'Smirk') for major underlying assets.
2. **Skew Analysis**: Compares the pricing of downside protection (Puts) vs upside speculation (Calls).
3. **Mean Reversion Scoring**: Flags strikes where IV is significantly stretched compared to its 20-day moving average.

## Inputs & Outputs
- **Inputs**:
  - `option_chain_data` (Dict): Comprehensive pricing/IV data.
- **Outputs**:
  - `v_surface_3d` (List): Data points for 3D UI render.
  - `skew_alert` (Dict): Deep-dive into skew deviations.

## Acceptance Criteria
- Reconstruct the global volatility surface every 5 minutes during market hours.
- Identify "cheap" vs "expensive" volatility with 90% confidence based on historical standard deviation.
