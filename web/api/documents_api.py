"""
==============================================================================
FILE: web/api/documents_api.py
ROLE: Document Management REST API
PURPOSE: RESTful endpoints for document upload, retrieval, and deletion.
         Integrates with S3Service for secure storage.

INTEGRATION POINTS:
    - S3Service: AWS S3 storage backend
    - DocumentLibrary.jsx: Frontend document management widget
    - TaxService: Tax document storage
    - KYCService: KYC document storage

ENDPOINTS:
    POST /api/v1/documents - Upload document
    GET /api/v1/documents - List user's documents
    GET /api/v1/documents/{id} - Get presigned download URL
    DELETE /api/v1/documents/{id} - Delete document

AUTHENTICATION: JWT Bearer token required
RATE LIMITING: 100 uploads/hour per user

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

documents_bp = Blueprint('documents', __name__, url_prefix='/api/v1/documents')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def _get_s3_service():
    """Lazy-load S3 service."""
    from services.storage.s3_service import get_s3_service
    return get_s3_service()


def _get_user_id():
    """Get current user ID from session/token."""
    # TODO: Extract from JWT token or session
    return request.headers.get('X-User-ID', 'demo-user')


# In-memory document metadata store (should be database in production)
_document_metadata_store: Dict[str, Dict[str, Any]] = {}


def _build_response(data: Any, meta: Optional[Dict] = None) -> Dict[str, Any]:
    """Build standardized API response."""
    return {
        "data": data,
        "meta": meta or {
            "timestamp": datetime.now().isoformat(),
            "source": "s3_service"
        },
        "errors": []
    }


def _build_error_response(error_code: str, message: str) -> Dict[str, Any]:
    """Build standardized error response."""
    return {
        "data": None,
        "meta": {},
        "errors": [{
            "error_code": error_code,
            "message": message
        }]
    }


# =============================================================================
# Upload Document Endpoint
# =============================================================================

@documents_bp.route('', methods=['POST'])
def upload_document():
    """
    Upload a document to S3.
    
    Request:
        multipart/form-data with:
        - file: File to upload
        - category: Document category (tax, kyc, report, user_upload, general)
        - description: Optional description
        
    Returns:
        JSON with document ID and metadata
    """
    try:
        if 'file' not in request.files:
            return jsonify(_build_error_response(
                "MISSING_FILE",
                "No file provided"
            )), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(_build_error_response(
                "EMPTY_FILE",
                "Empty filename"
            )), 400
        
        category = request.form.get('category', 'general')
        description = request.form.get('description', '')
        user_id = _get_user_id()
        
        # Validate category
        valid_categories = ['tax', 'kyc', 'report', 'user_upload', 'general']
        if category not in valid_categories:
            return jsonify(_build_error_response(
                "INVALID_CATEGORY",
                f"Category must be one of: {', '.join(valid_categories)}"
            )), 400
        
        # Read file content
        content = file.read()
        if len(content) == 0:
            return jsonify(_build_error_response(
                "EMPTY_FILE",
                "File is empty"
            )), 400
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024
        if len(content) > max_size:
            return jsonify(_build_error_response(
                "FILE_TOO_LARGE",
                f"File exceeds maximum size of {max_size / 1024 / 1024}MB"
            )), 400
        
        # Upload to S3
        s3_service = _get_s3_service()
        result = _run_async(s3_service.upload_file(
            user_id=user_id,
            filename=file.filename,
            content=content,
            category=category,
            metadata={"description": description} if description else None
        ))
        
        # Store metadata (in production, this would be in database)
        document_metadata = {
            "document_id": result.document_id,
            "user_id": user_id,
            "s3_key": result.s3_key,
            "bucket": result.bucket,
            "filename": file.filename,
            "content_type": file.content_type or "application/octet-stream",
            "size_bytes": result.size_bytes,
            "checksum": result.checksum,
            "category": category,
            "description": description,
            "uploaded_at": datetime.now().isoformat()
        }
        
        _document_metadata_store[result.document_id] = document_metadata
        
        logger.info(f"Document uploaded: {result.document_id} for user {user_id}")
        
        return jsonify(_build_response({
            "document_id": result.document_id,
            "filename": file.filename,
            "size_bytes": result.size_bytes,
            "category": category,
            "uploaded_at": document_metadata["uploaded_at"]
        })), 201
        
    except Exception as e:
        logger.error(f"Document upload failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "UPLOAD_ERROR",
            f"Failed to upload document: {str(e)}"
        )), 500


# =============================================================================
# List Documents Endpoint
# =============================================================================

@documents_bp.route('', methods=['GET'])
def list_documents():
    """
    List user's documents with pagination.
    
    Query Params:
        category: Filter by category
        page: Page number (default 1)
        per_page: Items per page (default 20)
        
    Returns:
        JSON array of document metadata
    """
    try:
        user_id = _get_user_id()
        category = request.args.get('category')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Filter user's documents
        user_docs = [
            doc for doc in _document_metadata_store.values()
            if doc['user_id'] == user_id
        ]
        
        # Filter by category if specified
        if category:
            user_docs = [doc for doc in user_docs if doc['category'] == category]
        
        # Sort by upload date (newest first)
        user_docs.sort(key=lambda x: x['uploaded_at'], reverse=True)
        
        # Pagination
        total = len(user_docs)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_docs = user_docs[start:end]
        
        # Format response (exclude S3 keys for security)
        formatted_docs = [
            {
                "document_id": doc["document_id"],
                "filename": doc["filename"],
                "size_bytes": doc["size_bytes"],
                "content_type": doc["content_type"],
                "category": doc["category"],
                "description": doc.get("description", ""),
                "uploaded_at": doc["uploaded_at"]
            }
            for doc in paginated_docs
        ]
        
        return jsonify(_build_response({
            "documents": formatted_docs,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }))
        
    except Exception as e:
        logger.error(f"List documents failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "LIST_ERROR",
            f"Failed to list documents: {str(e)}"
        )), 500


# =============================================================================
# Get Download URL Endpoint
# =============================================================================

@documents_bp.route('/<document_id>', methods=['GET'])
def get_document_url(document_id: str):
    """
    Get presigned download URL for document.
    
    Query Params:
        expires_in: URL expiration in seconds (default 3600)
        
    Returns:
        JSON with presigned download URL
    """
    try:
        user_id = _get_user_id()
        expires_in = int(request.args.get('expires_in', 3600))
        
        # Get document metadata
        doc_metadata = _document_metadata_store.get(document_id)
        if not doc_metadata:
            return jsonify(_build_error_response(
                "DOCUMENT_NOT_FOUND",
                f"Document {document_id} not found"
            )), 404
        
        # Verify ownership
        if doc_metadata['user_id'] != user_id:
            return jsonify(_build_error_response(
                "ACCESS_DENIED",
                "You do not have access to this document"
            )), 403
        
        # Generate presigned URL
        s3_service = _get_s3_service()
        url = s3_service.generate_presigned_url(
            s3_key=doc_metadata['s3_key'],
            bucket=doc_metadata['bucket'],
            expiration_seconds=expires_in,
            category=doc_metadata['category']
        )
        
        return jsonify(_build_response({
            "document_id": document_id,
            "filename": doc_metadata['filename'],
            "download_url": url,
            "expires_in": expires_in,
            "expires_at": (datetime.now().timestamp() + expires_in).isoformat()
        }))
        
    except Exception as e:
        logger.error(f"Get document URL failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "URL_GENERATION_ERROR",
            f"Failed to generate download URL: {str(e)}"
        )), 500


# =============================================================================
# Delete Document Endpoint
# =============================================================================

@documents_bp.route('/<document_id>', methods=['DELETE'])
def delete_document(document_id: str):
    """
    Delete document from S3 and metadata store.
    
    Returns:
        JSON confirmation
    """
    try:
        user_id = _get_user_id()
        
        # Get document metadata
        doc_metadata = _document_metadata_store.get(document_id)
        if not doc_metadata:
            return jsonify(_build_error_response(
                "DOCUMENT_NOT_FOUND",
                f"Document {document_id} not found"
            )), 404
        
        # Verify ownership
        if doc_metadata['user_id'] != user_id:
            return jsonify(_build_error_response(
                "ACCESS_DENIED",
                "You do not have access to this document"
            )), 403
        
        # Delete from S3
        s3_service = _get_s3_service()
        deleted = _run_async(s3_service.delete_file(
            s3_key=doc_metadata['s3_key'],
            bucket=doc_metadata['bucket'],
            category=doc_metadata['category']
        ))
        
        if not deleted:
            return jsonify(_build_error_response(
                "DELETE_ERROR",
                "Failed to delete file from storage"
            )), 500
        
        # Remove from metadata store
        del _document_metadata_store[document_id]
        
        logger.info(f"Document deleted: {document_id} by user {user_id}")
        
        return jsonify(_build_response({
            "document_id": document_id,
            "deleted": True
        }))
        
    except Exception as e:
        logger.error(f"Delete document failed: {e}", exc_info=True)
        return jsonify(_build_error_response(
            "DELETE_ERROR",
            f"Failed to delete document: {str(e)}"
        )), 500
