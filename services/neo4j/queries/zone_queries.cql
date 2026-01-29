// Find nearest Supply Zone above current price
MATCH (z:LIQUIDITY_ZONE {type: 'SUPPLY', is_mitigated: false})
WHERE z.price_low > $current_price
RETURN z
ORDER BY z.price_low ASC
LIMIT 1;

// Find nearest Demand Zone below current price
MATCH (z:LIQUIDITY_ZONE {type: 'DEMAND', is_mitigated: false})
WHERE z.price_high < $current_price
RETURN z
ORDER BY z.price_high DESC
LIMIT 1;

// Find Unmitigated Zones intersecting a price range
MATCH (z:LIQUIDITY_ZONE {is_mitigated: false})
WHERE z.price_high >= $range_low AND z.price_low <= $range_high
RETURN z;
