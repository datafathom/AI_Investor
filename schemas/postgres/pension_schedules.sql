-- Phase 118: Pension Schedules
-- Tracks defined benefit pension details and employer solvency metrics

CREATE TABLE IF NOT EXISTS pension_schedules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    pension_provider VARCHAR(255),
    monthly_benefit DECIMAL(20, 2),
    payment_start_date DATE,
    cola_adjustment DECIMAL(8, 6), -- Cost of Living Adjustment
    survivor_benefit_pct DECIMAL(8, 6),
    funding_ratio DECIMAL(8, 6), -- Plan assets vs liabilities
    employer_credit_rating VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pension_user ON pension_schedules(user_id);
