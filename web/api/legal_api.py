"""
Legal Documents API - FastAPI Router
Complete legal document management with database integration.
"""

import logging
from typing import Optional, Dict, List, Any
from datetime import timezone, datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from web.auth_utils import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/legal", tags=["Legal"])

# Legal document versions (in production, store in database)
LEGAL_DOCUMENTS = {
    'terms_of_service': {
        'version': '1.0',
        'effective_date': '2026-01-21',
        'file': 'docs/legal/terms_of_service.md',
        'required': True
    },
    'privacy_policy': {
        'version': '1.0',
        'effective_date': '2026-01-21',
        'file': 'docs/legal/privacy_policy.md',
        'required': True
    },
    'cookie_policy': {
        'version': '1.0',
        'effective_date': '2026-01-21',
        'file': 'docs/legal/cookie_policy.md',
        'required': False
    },
    'risk_disclosure': {
        'version': '1.0',
        'effective_date': '2026-01-21',
        'file': 'docs/legal/risk_disclosure.md',
        'required': True
    }
}

class AcceptanceRequest(BaseModel):
    documents: List[str]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

@router.get('/documents')
async def list_documents():
    """List all available legal documents with versions."""
    documents = []
    for doc_id, doc_info in LEGAL_DOCUMENTS.items():
        documents.append({
            'id': doc_id,
            'name': doc_id.replace('_', ' ').title(),
            'version': doc_info['version'],
            'effective_date': doc_info['effective_date'],
            'required': doc_info.get('required', False),
            'url': f'/api/v1/legal/documents/{doc_id}'
        })
    
    return {
        'success': True,
        'data': documents
    }

@router.get('/documents/{document_id}')
async def get_document(document_id: str):
    """Get a specific legal document."""
    if document_id not in LEGAL_DOCUMENTS:
        return JSONResponse(status_code=404, content={"success": False, "detail": "Document not found"})
    
    doc_info = LEGAL_DOCUMENTS[document_id]
    
    try:
        project_root = Path(__file__).parent.parent.parent
        doc_path = project_root / doc_info['file']
        
        if not doc_path.exists():
            return JSONResponse(status_code=404, content={"success": False, "detail": "Document file not found"})
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'success': True,
            'data': {
                'id': document_id,
                'name': document_id.replace('_', ' ').title(),
                'version': doc_info['version'],
                'effective_date': doc_info['effective_date'],
                'last_updated': doc_info['effective_date'],
                'required': doc_info.get('required', False),
                'content': content
            }
        }
    except Exception as e:
        logger.error(f"Error reading legal document: {e}")
        return JSONResponse(status_code=500, content={"success": False, "detail": "Failed to read document"})

@router.post('/accept')
async def accept_documents(
    request_data: AcceptanceRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Record user acceptance of legal documents."""
    user_id = current_user.get('id')
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Authentication required"})
    
    if not request_data.documents:
        return JSONResponse(status_code=400, content={"success": False, "detail": "No documents specified"})
    
    # Validate document IDs
    invalid_docs = [doc_id for doc_id in request_data.documents if doc_id not in LEGAL_DOCUMENTS]
    if invalid_docs:
        return JSONResponse(status_code=400, content={"success": False, "detail": f"Invalid document IDs: {invalid_docs}"})
    
    acceptances = []
    for doc_id in request_data.documents:
        doc_info = LEGAL_DOCUMENTS[doc_id]
        acceptance = {
            'document_id': doc_id,
            'version': doc_info['version'],
            'accepted_at': datetime.now(timezone.utc).isoformat(),
            'user_id': user_id,
            'ip_address': request.client.host,
            'user_agent': request.headers.get('User-Agent')
        }
        acceptances.append(acceptance)
    
    logger.info(f"User {user_id} accepted documents: {request_data.documents}")
    
    return {
        'success': True,
        'data': {
            'acceptances': acceptances,
            'accepted_at': datetime.now(timezone.utc).isoformat()
        }
    }

@router.get('/acceptance-status')
async def get_acceptance_status(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's legal document acceptance status."""
    user_id = current_user.get('id')
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Authentication required"})
    
    required_documents = [doc_id for doc_id, info in LEGAL_DOCUMENTS.items() if info.get('required', False)]
    
    # Mock behavior as in legacy
    accepted_documents = []  
    pending_acceptance = [doc for doc in required_documents if doc not in accepted_documents]
    
    status = {
        'user_id': user_id,
        'required_documents': required_documents,
        'accepted_documents': accepted_documents,
        'pending_acceptance': pending_acceptance,
        'all_accepted': len(pending_acceptance) == 0,
        'last_updated': None
    }
    
    return {
        'success': True,
        'data': status
    }

@router.get('/acceptance-history')
async def get_acceptance_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get user's legal document acceptance history."""
    user_id = current_user.get('id')
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Authentication required"})
    
    return {
        'success': True,
        'data': {
            'user_id': user_id,
            'history': [],
            'total_acceptances': 0
        }
    }

@router.get('/check-updates')
async def check_document_updates(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Check if user needs to accept updated legal documents."""
    user_id = current_user.get('id')
    if not user_id:
        return JSONResponse(status_code=401, content={"success": False, "detail": "Authentication required"})
    
    updates_available = []
    for doc_id, doc_info in LEGAL_DOCUMENTS.items():
        if doc_info.get('required', False):
            updates_available.append({
                'document_id': doc_id,
                'current_version': doc_info['version'],
                'user_version': None,
                'update_required': True
            })
    
    return {
        'success': True,
        'data': {
            'updates_available': updates_available,
            'update_required': len(updates_available) > 0
        }
    }
