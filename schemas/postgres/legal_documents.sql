-- Migration: Legal Documents and Acceptance Tracking
-- Description: Create tables for legal document management and user acceptance tracking
-- Created: 2026-01-21
-- ID: phase6_004_legal_documents

BEGIN;

-- Legal documents table
CREATE TABLE IF NOT EXISTS legal_documents (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    effective_date DATE NOT NULL,
    content TEXT,
    file_path VARCHAR(500),
    required BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User legal document acceptances
CREATE TABLE IF NOT EXISTS legal_document_acceptances (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    document_id VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    accepted_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (document_id) REFERENCES legal_documents(document_id) ON DELETE CASCADE,
    UNIQUE(user_id, document_id, version)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_legal_doc_acceptances_user_id ON legal_document_acceptances(user_id);
CREATE INDEX IF NOT EXISTS idx_legal_doc_acceptances_document_id ON legal_document_acceptances(document_id);
CREATE INDEX IF NOT EXISTS idx_legal_doc_acceptances_accepted_at ON legal_document_acceptances(accepted_at);

-- Insert default legal documents
INSERT INTO legal_documents (document_id, name, version, effective_date, required) VALUES
    ('terms_of_service', 'Terms of Service', '1.0', '2026-01-21', TRUE),
    ('privacy_policy', 'Privacy Policy', '1.0', '2026-01-21', TRUE),
    ('cookie_policy', 'Cookie Policy', '1.0', '2026-01-21', FALSE),
    ('risk_disclosure', 'Risk Disclosure Statement', '1.0', '2026-01-21', TRUE)
ON CONFLICT (document_id) DO NOTHING;

COMMIT;
