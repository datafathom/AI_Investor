"""
KYC API - Identity Verification & Document Management Endpoints

Phase 54: REST endpoints for KYC verification, document management,
and regulatory filing features.

Routes:
    GET  /api/v1/kyc/status          - Get verification status
    GET  /api/v1/kyc/documents       - List user documents
    POST /api/v1/kyc/documents/upload - Upload document
    GET  /api/v1/kyc/filings/calendar - Get filing deadlines
    GET  /api/v1/kyc/filings/13f/{portfolio_id}/export - Export 13F XML
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

from services.security.kyc_service import (
    KYCService,
    Document,
    DocumentType,
    VerificationResult,
    FilingDeadline
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/kyc", tags=["KYC"])

# Singleton service instance
_kyc_service: Optional[KYCService] = None


def get_kyc_service() -> KYCService:
    """Get or create KYC service singleton."""
    global _kyc_service
    if _kyc_service is None:
        _kyc_service = KYCService()
    return _kyc_service


# ─────────────────────────────────────────────────────────────────────────────
# Response Models
# ─────────────────────────────────────────────────────────────────────────────

class DocumentResponse(BaseModel):
    """Document response model."""
    id: str
    document_type: str
    filename: str
    status: str
    uploaded_at: str
    expires_at: Optional[str]


class VerificationStatusResponse(BaseModel):
    """Verification status response."""
    is_verified: bool
    level: str
    missing_documents: List[str]
    expires_at: Optional[str]


class FilingDeadlineResponse(BaseModel):
    """Filing deadline response."""
    filing_type: str
    due_date: str
    description: str
    status: str
    days_remaining: int


class DocumentListResponse(BaseModel):
    """Documents list response."""
    documents: List[DocumentResponse]
    total: int


class FilingCalendarResponse(BaseModel):
    """Filing calendar response."""
    deadlines: List[FilingDeadlineResponse]


class RequiredDocumentsResponse(BaseModel):
    """Required documents response."""
    level: str
    documents: List[dict]


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/status")
async def get_verification_status(
    user_id: str = "demo-user",
    service: KYCService = Depends(get_kyc_service)
):
    """
    Get current verification status for user.
    
    Returns verification level, missing documents, and expiration.
    """
    try:
        result = await service.get_verification_status(user_id)
        
        if result is None:
            # Return default unverified status
            return {
                "success": True,
                "data": VerificationStatusResponse(
                    is_verified=False,
                    level="none",
                    missing_documents=["passport", "utility_bill"],
                    expires_at=None
                ).model_dump()
            }
        
        return {
            "success": True,
            "data": VerificationStatusResponse(
                is_verified=result.is_verified,
                level=result.verification_level,
                missing_documents=[d.value for d in result.missing_documents],
                expires_at=result.expires_at
            ).model_dump()
        }
    except Exception as e:
        logger.exception("Error getting verification status")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/documents")
async def list_documents(
    user_id: str = "demo-user",
    service: KYCService = Depends(get_kyc_service)
):
    """
    List all documents for a user.
    
    Returns document metadata including status and expiration.
    """
    try:
        docs = await service.get_user_documents(user_id)
        
        doc_responses = [
            DocumentResponse(
                id=d.id,
                document_type=d.document_type.value,
                filename=d.filename,
                status=d.status.value,
                uploaded_at=d.uploaded_at,
                expires_at=d.expires_at
            ).model_dump()
            for d in docs
        ]
        
        return {
            "success": True,
            "data": DocumentListResponse(
                documents=doc_responses,
                total=len(doc_responses)
            ).model_dump()
        }
    except Exception as e:
        logger.exception("Error listing documents")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Form(...),
    user_id: str = Form(default="demo-user"),
    service: KYCService = Depends(get_kyc_service)
):
    """
    Upload a document for KYC verification.
    
    Accepts document file and type, returns created document metadata.
    """
    try:
        # Validate document type
        try:
            doc_type = DocumentType(document_type.lower())
        except ValueError:
            valid_types = [t.value for t in DocumentType]
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": f"Invalid document_type. Valid types: {valid_types}"}
            )
        
        # Read file content
        content = await file.read()
        
        if len(content) == 0:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Empty file"})
        
        if len(content) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse(status_code=400, content={"success": False, "detail": "File too large (max 10MB)"})
        
        doc = await service.upload_document(
            user_id=user_id,
            document_type=document_type,
            filename=file.filename or "unknown",
            content=content
        )
        
        logger.info(f"Document uploaded: {doc.id} for user {user_id}")
        
        return {
            "success": True,
            "data": DocumentResponse(
                id=doc.id,
                document_type=doc.document_type.value,
                filename=doc.filename,
                status=doc.status.value,
                uploaded_at=doc.uploaded_at,
                expires_at=doc.expires_at
            ).model_dump()
        }
    except Exception as e:
        logger.exception("Error uploading document")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/filings/calendar")
async def get_filing_calendar(
    service: KYCService = Depends(get_kyc_service)
):
    """
    Get upcoming regulatory filing deadlines.
    
    Returns 13F, 13D/G, K-1, and other deadlines with status.
    """
    try:
        deadlines = await service.get_filing_calendar()
        
        deadline_responses = [
            FilingDeadlineResponse(
                filing_type=d.filing_type,
                due_date=d.due_date,
                description=d.description,
                status=d.status,
                days_remaining=d.days_remaining
            ).model_dump()
            for d in deadlines
        ]
        
        return {
            "success": True,
            "data": FilingCalendarResponse(deadlines=deadline_responses).model_dump()
        }
    except Exception as e:
        logger.exception("Error getting filing calendar")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/filings/13f/{portfolio_id}/export")
async def export_13f_xml(
    portfolio_id: str,
    service: KYCService = Depends(get_kyc_service)
) -> Response:
    """
    Export 13F filing as SEC-compliant XML.
    
    Returns downloadable XML file with all holdings data.
    """
    try:
        xml_bytes = await service.generate_13f_xml(portfolio_id)
        
        filename = f"13F_{portfolio_id}_{datetime.now().strftime('%Y%m%d')}.xml"
        
        return Response(
            content=xml_bytes,
            media_type="application/xml",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        logger.exception("Error exporting 13F")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})


@router.get("/requirements/{level}")
async def get_required_documents(
    level: str = "basic",
    service: KYCService = Depends(get_kyc_service)
):
    """
    Get required documents for a verification level.
    
    Levels: basic, enhanced, accredited
    """
    if level not in ["basic", "enhanced", "accredited"]:
        return JSONResponse(
            status_code=400,
            content={"success": False, "detail": "Invalid level. Valid: basic, enhanced, accredited"}
        )
    
    docs = service.get_required_documents(level)
    
    return {
        "success": True,
        "data": RequiredDocumentsResponse(
            level=level,
            documents=docs
        ).model_dump()
    }


@router.post("/verify")
async def trigger_verification(
    user_id: str = "demo-user",
    service: KYCService = Depends(get_kyc_service)
):
    """
    Trigger verification for a user based on uploaded documents.
    
    Analyzes all uploaded documents and determines verification level.
    """
    try:
        docs = await service.get_user_documents(user_id)
        
        if not docs:
            return {
                "success": True,
                "data": VerificationStatusResponse(
                    is_verified=False,
                    level="none",
                    missing_documents=["passport", "utility_bill"],
                    expires_at=None
                ).model_dump()
            }
        
        result = await service.verify_identity(user_id, docs)
        
        return {
            "success": True,
            "data": VerificationStatusResponse(
                is_verified=result.is_verified,
                level=result.verification_level,
                missing_documents=[d.value for d in result.missing_documents],
                expires_at=result.expires_at
            ).model_dump()
        }
    except Exception as e:
        logger.exception("Error triggering verification")
        return JSONResponse(status_code=500, content={"success": False, "detail": str(e)})
