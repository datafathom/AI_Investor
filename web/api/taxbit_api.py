"""
==============================================================================
FILE: web/api/taxbit_api.py
ROLE: TaxBit API REST Endpoints
PURPOSE: RESTful endpoints for TaxBit tax reporting and document generation.

INTEGRATION POINTS:
    - TaxBitClient: Transaction ingestion and document generation
    - TaxDocumentService: Document retrieval and storage

ENDPOINTS:
    POST /api/v1/taxbit/ingest-transactions - Ingest transactions
    POST /api/v1/taxbit/generate-document - Generate tax document
    GET /api/v1/taxbit/documents - List tax documents
    GET /api/v1/taxbit/documents/{year} - Get document for year

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

taxbit_bp = Blueprint('taxbit', __name__, url_prefix='/api/v1/taxbit')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@taxbit_bp.route('/ingest-transactions', methods=['POST'])
def ingest_transactions():
    """Ingest transactions from brokerages."""
    try:
        data = request.json or {}
        source = data.get('source')  # alpaca, robinhood, ethereum, solana
        
        # In production, would sync transactions from connected brokerages
        return jsonify({
            "success": True,
            "source": source,
            "transactions_ingested": 0,
            "message": "Transaction ingestion initiated"
        })
    except Exception as e:
        logger.error(f"Failed to ingest transactions: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@taxbit_bp.route('/generate-document', methods=['POST'])
def generate_document():
    """Generate tax document for a year."""
    try:
        data = request.json or {}
        tax_year = data.get('tax_year')
        
        if not tax_year:
            return jsonify({"error": "Missing tax_year"}), 400
        
        # In production, would trigger TaxBit document generation
        return jsonify({
            "success": True,
            "tax_year": tax_year,
            "document_id": f"doc_{tax_year}",
            "status": "pending",
            "message": "Document generation initiated"
        })
    except Exception as e:
        logger.error(f"Failed to generate document: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@taxbit_bp.route('/documents', methods=['GET'])
def list_documents():
    """List available tax documents."""
    try:
        # Mock response
        return jsonify({
            "documents": [
                {
                    "tax_year": 2025,
                    "status": "available",
                    "document_id": "doc_2025",
                    "generated_at": "2026-01-15T10:00:00Z"
                },
                {
                    "tax_year": 2024,
                    "status": "available",
                    "document_id": "doc_2024",
                    "generated_at": "2025-01-15T10:00:00Z"
                }
            ]
        })
    except Exception as e:
        logger.error(f"Failed to list documents: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@taxbit_bp.route('/documents/<int:year>', methods=['GET'])
def get_document(year: int):
    """Get tax document for a specific year."""
    try:
        # In production, would retrieve from S3
        return jsonify({
            "tax_year": year,
            "document_id": f"doc_{year}",
            "download_url": f"/api/v1/taxbit/documents/{year}/download",
            "status": "available"
        })
    except Exception as e:
        logger.error(f"Failed to get document: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
