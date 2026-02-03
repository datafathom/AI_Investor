"""
KYC API - Identity Verification & Document Management (Flask Version)
Phase 54: Endpoints for KYC verification and document management.
"""

from flask import Blueprint, jsonify, request, send_file
import io
import logging

from services.security.kyc_service import (
    get_kyc_service,
    DocumentType
)

kyc_bp = Blueprint('kyc_api', __name__, url_prefix='/api/v1/kyc')
logger = logging.getLogger(__name__)

@kyc_bp.route('/status', methods=['GET'])
def get_verification_status():
    user_id = request.args.get('user_id', 'demo-user')
    service = get_kyc_service()
    import asyncio
    result = asyncio.run(service.get_verification_status(user_id))
    
    if result is None:
        return jsonify({
            "is_verified": False,
            "level": "none",
            "missing_documents": ["passport", "utility_bill"],
            "expires_at": None
        })
    
    return jsonify({
        "is_verified": result.is_verified,
        "level": result.verification_level,
        "missing_documents": [d.value for d in result.missing_documents],
        "expires_at": result.expires_at
    })

@kyc_bp.route('/documents', methods=['GET'])
def list_documents():
    user_id = request.args.get('user_id', 'demo-user')
    service = get_kyc_service()
    import asyncio
    docs = asyncio.run(service.get_user_documents(user_id))
    
    return jsonify({
        "documents": [
            {
                "id": d.id,
                "document_type": d.document_type.value,
                "filename": d.filename,
                "status": d.status.value,
                "uploaded_at": d.uploaded_at,
                "expires_at": d.expires_at
            } for d in docs
        ],
        "total": len(docs)
    })

@kyc_bp.route('/documents/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    doc_type_str = request.form.get('document_type')
    user_id = request.form.get('user_id', 'demo-user')
    
    if not doc_type_str:
        return jsonify({"error": "Missing document_type"}), 400
        
    service = get_kyc_service()
    import asyncio
    content = file.read()
    
    doc = asyncio.run(service.upload_document(
        user_id=user_id,
        document_type=doc_type_str,
        filename=file.filename,
        content=content
    ))
    
    return jsonify({
        "id": doc.id,
        "document_type": doc.document_type.value,
        "filename": doc.filename,
        "status": doc.status.value,
        "uploaded_at": doc.uploaded_at
    }), 201

@kyc_bp.route('/filings/calendar', methods=['GET'])
def get_filing_calendar():
    service = get_kyc_service()
    import asyncio
    deadlines = asyncio.run(service.get_filing_calendar())
    
    return jsonify({
        "deadlines": [
            {
                "filing_type": d.filing_type,
                "due_date": d.due_date,
                "description": d.description,
                "status": d.status,
                "days_remaining": d.days_remaining
            } for d in deadlines
        ]
    })

@kyc_bp.route('/verify', methods=['POST'])
def trigger_verification():
    user_id = request.json.get('user_id', 'demo-user')
    service = get_kyc_service()
    import asyncio
    docs = asyncio.run(service.get_user_documents(user_id))
    result = asyncio.run(service.verify_identity(user_id, docs))
    
    return jsonify({
        "is_verified": result.is_verified,
        "level": result.verification_level,
        "missing_documents": [d.value for d in result.missing_documents],
        "expires_at": result.expires_at
    })
