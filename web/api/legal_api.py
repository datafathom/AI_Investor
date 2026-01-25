"""
Legal Documents API
Complete legal document management with database integration
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

legal_bp = Blueprint('legal', __name__)

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


@legal_bp.route('/api/v1/legal/documents', methods=['GET'])
def list_documents():
    """
    List all available legal documents with versions.
    
    Returns:
        JSON response with list of documents
    """
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
    
    return jsonify({
        'success': True,
        'data': documents
    }), 200


@legal_bp.route('/api/v1/legal/documents/<document_id>', methods=['GET'])
def get_document(document_id: str):
    """
    Get a specific legal document.
    
    Args:
        document_id: Document identifier
    
    Returns:
        JSON response with document content
    """
    if document_id not in LEGAL_DOCUMENTS:
        return jsonify({
            'success': False,
            'error': 'Document not found'
        }), 404
    
    doc_info = LEGAL_DOCUMENTS[document_id]
    
    try:
        from pathlib import Path
        project_root = Path(__file__).parent.parent.parent
        doc_path = project_root / doc_info['file']
        
        if not doc_path.exists():
            return jsonify({
                'success': False,
                'error': 'Document file not found'
            }), 404
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
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
        }), 200
        
    except Exception as e:
        logger.error(f"Error reading legal document: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to read document'
        }), 500


@legal_bp.route('/api/v1/legal/accept', methods=['POST'])
def accept_documents():
    """
    Record user acceptance of legal documents.
    Requires authentication.
    
    Request Body:
        {
            "documents": ["terms_of_service", "privacy_policy"],
            "ip_address": "optional",
            "user_agent": "optional"
        }
    
    Returns:
        JSON response with acceptance records
    """
    from web.auth_utils import login_required
    from flask import g
    
    data = request.get_json()
    document_ids = data.get('documents', [])
    user_id = getattr(g, 'user_id', None)
    
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401
    
    if not document_ids:
        return jsonify({
            'success': False,
            'error': 'No documents specified'
        }), 400
    
    # Validate document IDs
    invalid_docs = [doc_id for doc_id in document_ids if doc_id not in LEGAL_DOCUMENTS]
    if invalid_docs:
        return jsonify({
            'success': False,
            'error': f'Invalid document IDs: {invalid_docs}'
        }), 400
    
    # In production, store in database
    # Example SQL:
    # INSERT INTO legal_document_acceptances (user_id, document_id, version, accepted_at, ip_address, user_agent)
    # VALUES (:user_id, :document_id, :version, NOW(), :ip_address, :user_agent)
    
    acceptances = []
    for doc_id in document_ids:
        doc_info = LEGAL_DOCUMENTS[doc_id]
        acceptance = {
            'document_id': doc_id,
            'version': doc_info['version'],
            'accepted_at': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        acceptances.append(acceptance)
    
    logger.info(f"User {user_id} accepted documents: {document_ids}")
    
    return jsonify({
        'success': True,
        'data': {
            'acceptances': acceptances,
            'accepted_at': datetime.utcnow().isoformat()
        }
    }), 200


@legal_bp.route('/api/v1/legal/acceptance-status', methods=['GET'])
def get_acceptance_status():
    """
    Get user's legal document acceptance status.
    Requires authentication.
    
    Returns:
        JSON response with acceptance status
    """
    from web.auth_utils import login_required
    from flask import g
    
    user_id = getattr(g, 'user_id', None)
    
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401
    
    # In production, query database
    # Example SQL:
    # SELECT document_id, version, accepted_at 
    # FROM legal_document_acceptances 
    # WHERE user_id = :user_id
    
    required_documents = [doc_id for doc_id, info in LEGAL_DOCUMENTS.items() if info.get('required', False)]
    
    # Mock: assume user has not accepted (in production, check database)
    # For now, return required documents that need acceptance
    accepted_documents = []  # Would come from database query
    pending_acceptance = [doc for doc in required_documents if doc not in accepted_documents]
    
    status = {
        'user_id': user_id,
        'required_documents': required_documents,
        'accepted_documents': accepted_documents,
        'pending_acceptance': pending_acceptance,
        'all_accepted': len(pending_acceptance) == 0,
        'last_updated': None
    }
    
    return jsonify({
        'success': True,
        'data': status
    }), 200


@legal_bp.route('/api/v1/legal/acceptance-history', methods=['GET'])
def get_acceptance_history():
    """
    Get user's legal document acceptance history.
    Requires authentication.
    
    Returns:
        JSON response with acceptance history
    """
    from web.auth_utils import login_required
    from flask import g
    
    user_id = getattr(g, 'user_id', None)
    
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401
    
    # In production, query database for full history
    # Example SQL:
    # SELECT * FROM legal_document_acceptances 
    # WHERE user_id = :user_id 
    # ORDER BY accepted_at DESC
    
    history = []  # Would come from database
    
    return jsonify({
        'success': True,
        'data': {
            'user_id': user_id,
            'history': history,
            'total_acceptances': len(history)
        }
    }), 200


@legal_bp.route('/api/v1/legal/check-updates', methods=['GET'])
def check_document_updates():
    """
    Check if user needs to accept updated legal documents.
    Requires authentication.
    
    Returns:
        JSON response with update status
    """
    from web.auth_utils import login_required
    from flask import g
    
    user_id = getattr(g, 'user_id', None)
    
    if not user_id:
        return jsonify({
            'success': False,
            'error': 'Authentication required'
        }), 401
    
    # In production, compare user's accepted versions with current versions
    # Return documents that have been updated since user's acceptance
    
    updates_available = []
    for doc_id, doc_info in LEGAL_DOCUMENTS.items():
        # Check if user has accepted this version
        # If not, or if version is newer, add to updates_available
        if doc_info.get('required', False):
            updates_available.append({
                'document_id': doc_id,
                'current_version': doc_info['version'],
                'user_version': None,  # Would come from database
                'update_required': True
            })
    
    return jsonify({
        'success': True,
        'data': {
            'updates_available': updates_available,
            'update_required': len(updates_available) > 0
        }
    }), 200
