// Phase 24: Neo4j constraints for Liquidity Zones

CREATE CONSTRAINT ticker_unique IF NOT EXISTS FOR (a:ASSET) REQUIRE a.ticker IS UNIQUE;
CREATE INDEX zone_price_lookup IF NOT EXISTS FOR (z:LIQUIDITY_ZONE) ON (z.price_low, z.price_high);
CREATE INDEX zone_active_lookup IF NOT EXISTS FOR (z:LIQUIDITY_ZONE) ON (z.is_mitigated);
