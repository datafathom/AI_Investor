"""
==============================================================================
FILE: web/api/documents_api.py
ROLE: Document Management REST API (FastAPI)
PURPOSE: RESTful endpoints for document upload, retrieval, and deletion.
         Integrates with S3Service for secure storage.
==============================================================================
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Header, Depends
from pydantic import BaseModel
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from services.storage.s3_service import get_s3_service as _get_s3_service

def get_s3_provider():
    """Dependency for getting the S3 service."""
    return _get_s3_service()

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


# In-memory document metadata store (should be database in production)
_document_metadata_store: Dict[str, Dict[str, Any]] = {}


class DocumentMeta(BaseModel):
    document_id: str
    filename: str
    size_bytes: int
    content_type: str
    category: str
    description: str = ""
    uploaded_at: str


class ListDocumentsResponse(BaseModel):
    documents: List[DocumentMeta]
    pagination: Dict[str, Any]


# def _get_s3_service():
#     """Lazy-load S3 service."""
#     from services.storage.s3_service import get_s3_service
#     return get_s3_service()


@router.post("", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("general"),
    description: str = Form(""),
    x_user_id: str = Header("demo-user"),
    service = Depends(get_s3_provider)
):
    """Upload a document to S3."""
    try:
        # Validate category
        valid_categories = ['tax', 'kyc', 'report', 'user_upload', 'general']
        if category not in valid_categories:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=400, content={"success": False, "detail": f"Category must be one of: {', '.join(valid_categories)}"})
        
        # Read file content
        content = await file.read()
        if len(content) == 0:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=400, content={"success": False, "detail": "File is empty"})
        
        # Check file size (10MB limit)
        max_size = 10 * 1024 * 1024
        if len(content) > max_size:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=400, content={"success": False, "detail": f"File exceeds maximum size of {max_size / 1024 / 1024}MB"})
        
        # Upload to S3
        result = await service.upload_file(
            user_id=x_user_id,
            filename=file.filename,
            content=content,
            category=category,
            metadata={"description": description} if description else None
        )
        
        # Store metadata
        document_id = result.document_id
        document_metadata = {
            "document_id": document_id,
            "user_id": x_user_id,
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
        
        _document_metadata_store[document_id] = document_metadata
        
        logger.info(f"Document uploaded: {document_id} for user {x_user_id}")
        
        return {
            "success": True,
            "data": {
                "document_id": document_id,
                "filename": file.filename,
                "size_bytes": result.size_bytes,
                "category": category,
                "uploaded_at": document_metadata["uploaded_at"]
            }
        }
        
    except Exception as e:
        logger.exception("Document upload failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("")
async def list_documents(
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    x_user_id: str = Header("demo-user")
):
    """List user's documents with pagination."""
    try:
        # Filter user's documents
        user_docs = [
            doc for doc in _document_metadata_store.values()
            if doc['user_id'] == x_user_id
        ]
        
        if category:
            user_docs = [doc for doc in user_docs if doc['category'] == category]
        
        user_docs.sort(key=lambda x: x['uploaded_at'], reverse=True)
        
        total = len(user_docs)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_docs = user_docs[start:end]
        
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
        
        return {
            "success": True,
            "data": {
                "documents": formatted_docs,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": (total + per_page - 1) // per_page
                }
            }
        }
    except Exception as e:
        logger.exception("List documents failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/{document_id}")
async def get_document_url(
    document_id: str,
    expires_in: int = Query(3600),
    x_user_id: str = Header("demo-user"),
    service = Depends(get_s3_provider)
):
    """Get presigned download URL for document."""
    try:
        doc_metadata = _document_metadata_store.get(document_id)
        if not doc_metadata:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=404, content={"success": False, "detail": f"Document {document_id} not found"})
        
        if doc_metadata['user_id'] != x_user_id:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=403, content={"success": False, "detail": "You do not have access to this document"})
        
        url = service.generate_presigned_url(
            s3_key=doc_metadata['s3_key'],
            bucket=doc_metadata['bucket'],
            expiration_seconds=expires_in,
            category=doc_metadata['category']
        )
        
        return {
            "success": True,
            "data": {
                "document_id": document_id,
                "filename": doc_metadata['filename'],
                "download_url": url,
                "expires_in": expires_in,
                "expires_at": datetime.fromtimestamp(datetime.now().timestamp() + expires_in).isoformat()
            }
        }
    except Exception as e:
        logger.exception("Get document URL failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    x_user_id: str = Header("demo-user"),
    service = Depends(get_s3_provider)
):
    """Delete document from S3 and metadata store."""
    try:
        doc_metadata = _document_metadata_store.get(document_id)
        if not doc_metadata:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=404, content={"success": False, "detail": f"Document {document_id} not found"})
        
        if doc_metadata['user_id'] != x_user_id:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=403, content={"success": False, "detail": "You do not have access to this document"})
        
        deleted = await service.delete_file(
            s3_key=doc_metadata['s3_key'],
            bucket=doc_metadata['bucket'],
            category=doc_metadata['category']
        )
        
        if not deleted:
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=500, content={"success": False, "detail": "Failed to delete file from storage"})
        
        del _document_metadata_store[document_id]
        
        logger.info(f"Document deleted: {document_id} by user {x_user_id}")
        
        return {
            "success": True,
            "data": {"document_id": document_id, "deleted": True}
        }
    except Exception as e:
        logger.exception("Delete document failed")
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
