-- Rollback Migration: Legal Documents and Acceptance Tracking
-- Description: Rollback for phase6_004_legal_documents
-- Created: 2026-01-21
-- ID: phase6_004_legal_documents

BEGIN;

DROP INDEX IF EXISTS idx_legal_doc_acceptances_accepted_at;
DROP INDEX IF EXISTS idx_legal_doc_acceptances_document_id;
DROP INDEX IF EXISTS idx_legal_doc_acceptances_user_id;

DROP TABLE IF EXISTS legal_document_acceptances;
DROP TABLE IF EXISTS legal_documents;

COMMIT;
