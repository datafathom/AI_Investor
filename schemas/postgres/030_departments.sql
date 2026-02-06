-- 030_departments.sql
-- Agent Departments Schema for AI Investor

-- Department Table
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    quadrant VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    primary_metric_label VARCHAR(100),
    primary_metric_value FLOAT DEFAULT 0,
    last_update TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Department Agents Mapping
CREATE TABLE IF NOT EXISTS department_agents (
    id SERIAL PRIMARY KEY,
    department_id INTEGER REFERENCES departments(id),
    agent_id VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    status VARCHAR(20) DEFAULT 'idle',
    last_invocation TIMESTAMP WITH TIME ZONE,
    UNIQUE(department_id, agent_id)
);

-- Seed Initial 18 Departments
INSERT INTO departments (id, name, slug, quadrant, primary_metric_label) VALUES
(1, 'The Orchestrator', 'orchestrator', 'META', 'System Latency'),
(2, 'The Architect', 'architect', 'META', 'On Track %'),
(3, 'The Data Scientist', 'data-scientist', 'ATTACK', 'Model Confidence'),
(4, 'The Strategist', 'strategist', 'ATTACK', 'Strategy Success Rate'),
(5, 'The Trader', 'trader', 'ATTACK', 'Execution Latency'),
(6, 'The Physicist', 'physicist', 'ATTACK', 'Theta Decay'),
(7, 'The Hunter', 'hunter', 'ATTACK', 'Signal Hit Rate'),
(8, 'The Sentry', 'sentry', 'DEFENSE', 'Threat Level'),
(9, 'The Steward', 'steward', 'HOUSEHOLD', 'Cost of Living'),
(10, 'The Guardian', 'guardian', 'DEFENSE', 'Days of Runway'),
(11, 'The Lawyer', 'lawyer', 'DEFENSE', 'Tax Liability'),
(12, 'The Auditor', 'auditor', 'DEFENSE', 'Fee Leakage'),
(13, 'The Envoy', 'envoy', 'HOUSEHOLD', 'Network Health'),
(14, 'The Front Office', 'front-office', 'HOUSEHOLD', 'Pending Tasks'),
(15, 'The Historian', 'historian', 'META', 'Logic Score'),
(16, 'The Stress-Tester', 'stress-tester', 'META', 'Robustness %'),
(17, 'The Refiner', 'refiner', 'META', 'Agent Efficiency'),
(18, 'The Banker', 'banker', 'HOUSEHOLD', 'Burn Rate')
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    slug = EXCLUDED.slug,
    quadrant = EXCLUDED.quadrant;
