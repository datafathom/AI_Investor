-- Phase 135: Goal Milestones
-- Tracks target dates for automated glide-path shifts

CREATE TABLE IF NOT EXISTS goal_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    goal_type VARCHAR(50) NOT NULL, -- RETIREMENT, EDUCATION, MAJOR_PURCHASE
    target_date DATE NOT NULL,
    
    -- Glide Path Config
    glide_path_strategy VARCHAR(50) DEFAULT 'MODERATE', -- AGGRESSIVE, MODERATE, CONSERVATIVE
    equity_landing_point DECIMAL(5, 2) DEFAULT 0.40, -- Target equity % at goal date
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_goal_user_type ON goal_milestones(user_id, goal_type);
