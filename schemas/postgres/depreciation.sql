-- Phase 130: Property Depreciation Schedules
-- Tracks the tax shield benefits of direct real estate ownership

CREATE TABLE IF NOT EXISTS property_depreciation_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    property_id UUID NOT NULL,
    user_id UUID NOT NULL,
    
    -- Basis Details
    purchase_price DECIMAL(20, 2) NOT NULL,
    land_value DECIMAL(20, 2) NOT NULL,
    building_value DECIMAL(20, 2) GENERATED ALWAYS AS (purchase_price - land_value) STORED,
    placed_in_service_date DATE NOT NULL,
    
    -- Depreciation Method
    prop_type VARCHAR(20) NOT NULL, -- RESIDENTIAL (27.5), COMMERCIAL (39)
    recovery_period_years DECIMAL(4, 1) NOT NULL,
    
    -- Tracking
    accumulated_depreciation DECIMAL(20, 2) DEFAULT 0,
    current_year_deduction DECIMAL(20, 2),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_depr_user ON property_depreciation_schedules(user_id);
