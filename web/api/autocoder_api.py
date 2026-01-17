"""
==============================================================================
FILE: web/api/autocoder_api.py
ROLE: The Developer Bridge
PURPOSE:
    Expose endpoints for AI-driven code generation, validation, and deployment.
==============================================================================
"""

from flask import Blueprint, request, jsonify
from services.analysis.autocoder import get_autocoder
import logging

logger = logging.getLogger(__name__)
autocoder_bp = Blueprint('autocoder', __name__, url_prefix='/api/v1/dev')

@autocoder_bp.route('/generate', methods=['POST'])
def generate_code():
    data = request.json or {}
    task = data.get('task', 'Default adapter')
    
    coder = get_autocoder()
    code = coder.generate_code(task)
    
    return jsonify({
        "status": "success",
        "task": task,
        "code": code
    })

@autocoder_bp.route('/validate', methods=['POST'])
def validate_code():
    data = request.json or {}
    code = data.get('code', '')
    
    coder = get_autocoder()
    is_valid = coder.validate_code(code)
    
    return jsonify({
        "status": "success" if is_valid else "error",
        "is_valid": is_valid
    })

@autocoder_bp.route('/deploy', methods=['POST'])
def deploy_module():
    data = request.json or {}
    name = data.get('name', 'temp_module')
    code = data.get('code', '')
    
    coder = get_autocoder()
    instance = coder.deploy_module(name, code)
    
    if instance:
        return jsonify({
            "status": "success",
            "message": f"Module '{name}' deployed and hot-swapped.",
            "module_name": name
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Deployment failed validation."
        }), 400

@autocoder_bp.route('/status', methods=['GET'])
def get_status():
    coder = get_autocoder()
    return jsonify({
        "status": "healthy",
        "registry_count": len(coder.registry),
        "modules": list(coder.registry.keys())
    })
