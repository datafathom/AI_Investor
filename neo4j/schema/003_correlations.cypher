// Phase 9: Currency Correlation Schema
// Defines properties for CORRELATED_WITH relationships

// Note: Relationships don't have indexes in same way as nodes, 
// but we ensure asset uniqueness which is already done.

/*
Properties for CORRELATED_WITH:
- coefficient (float): Pearson coefficient [-1.0 to 1.0]
- confidence (float): Statistical confidence [0.0 to 1.0]
- timeframe (string): Calculation window (e.g., '1D', '4H')
- direction (string): POSITIVE|NEGATIVE|NEUTRAL
- updated_at (datetime): Last recalculation time
*/

// No additional constraints needed for relationships themselves,
// as they are defined by the start and end nodes.
