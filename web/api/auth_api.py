from flask import Blueprint, jsonify, request
import flask
from web.auth_utils import generate_token, login_required
from services.communication.email_service import get_email_service
from services.system.social_auth_service import get_social_auth_service
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    logger.info("AUTH_DEBUG: /login endpoint hit")
    try:
        try:
            data = request.get_json()
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            return jsonify({'error': 'Invalid JSON payload'}), 400

        if not data:
            return jsonify({'error': 'Email and password required'}), 400
            
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # 1. HARDCODED ADMIN FALLBACK (Development/Infrastructure-Free Mode)
        # This MUST be first to allow UI verification when DB is offline
        if email == 'admin' and password == 'makeMoney':
            logger.info("AUTH_FALLBACK_ACTIVE: Success for admin user")
            user_data = {
                "id": 0, "email": "admin@example.com", "username": "admin",
                "role": "admin", "is_verified": True
            }
            token = generate_token(user_id=user_data["id"], role=user_data["role"])
            return jsonify({
                'token': token,
                'user': user_data
            })

        social_service = get_social_auth_service()
        user_data = None
        
        # 2. Database Lookup (Standard Flow)
        try:
            with social_service.db.pg_cursor() as cur:
                cur.execute("""
                    SELECT id, email, username, role, is_verified, password_hash, organization_id 
                    FROM users WHERE username = %s OR LOWER(email) = LOWER(%s);
                """, (email, email))
                user = cur.fetchone()
                if user:
                    user_data = {
                        "id": user[0], "email": user[1], "username": user[2],
                        "role": user[3], "is_verified": user[4], "password_hash": user[5],
                        "organization_id": user[6]
                    }
        except Exception as e:
            logger.warning(f"Login DB connection unavailable: {e}")

        # 3. Standard Password Verification
        provided_hash = f"mock_hash_{password[::-1]}"
        if user_data:
            stored_hash = user_data.get("password_hash")
            if stored_hash == provided_hash:
                token = generate_token(user_id=user_data["id"], role=user_data["role"])
                return jsonify({
                    'token': token,
                    'user': {
                        'id': user_data["id"],
                        'username': user_data["username"],
                        'email': user_data["email"],
                        'role': user_data["role"],
                        'orgId': user_data.get("organization_id")
                    }
                })
        
        return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.exception(f"Unexpected error during login: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    social_service = get_social_auth_service()
    existing_user = social_service._get_user_by_email(email)
    
    if not existing_user:
        try:
            res = social_service.handle_callback(provider='email', code=f"email:{email}")
            
            # Extract user record immediately
            if 'user' in res and res['user']:
                user_record = res['user']
            else:
                user_record = social_service._get_user_by_email(email)
            
            if not user_record:
                logger.error(f"Failed to create user record for {email}")
                return jsonify({'error': 'Failed to create user'}), 500

            # CRITICAL: Verify password set success using ID
            pwd_success = social_service.set_password(email, password, user_id=user_record['id'])
            if not pwd_success:
                logger.error(f"Failed to set password for {email} (ID: {user_record['id']})")
                return jsonify({'error': 'Failed to set password'}), 500
                
        except Exception as e:
            if "duplicate key" in str(e) or "UniqueViolation" in str(e):
                return jsonify({'error': 'User already exists. Please log in.'}), 409
            
            logger.error(f"Registration failed for {email}: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        user_record = existing_user

    # At this point, user_record is guaranteed to be defined if we haven't returned
    # unless some logical branch was missed (which we check here for safety)
    if 'user_record' not in locals() or not user_record:
        return jsonify({'error': 'Internal registration error - record missing'}), 500

    # Send Verification Email
    try:
        verification_url = f"http://localhost:5050/api/auth/verify-email?email={email}&token=mock_verify_token"
        email_service = get_email_service()
        email_service.send_transactional_email(
            to=email,
            template='email_verification',
            context={'verification_url': verification_url}
        )
    except Exception as e:
        logger.error(f"Failed to send verification email to {email}: {e}")
        # We don't fail the whole registration if email fails in mock mode
        pass

    return jsonify({
        'message': 'User registered successfully. Please check your email for verification.',
        'user': {
            'id': user_record["id"],
            'username': user_record["username"],
            'email': email
        }
    })

@auth_bp.route('/verify-email', methods=['GET'])
def verify_email():
    email = request.args.get('email')
    token = request.args.get('token')
    
    if not email or token != 'mock_verify_token':
        return jsonify({"error": "Invalid verification request"}), 400
        
    success = get_social_auth_service().verify_email(email)
    if success:
        return "Email Verified! You can now log in.", 200
    return jsonify({"error": "User not found"}), 404

@auth_bp.route('/add-password', methods=['POST'])
@login_required
def add_password():
    # User must be logged in to add a password to their social account
    user_id = flask.g.user_id
    data = request.get_json()
    password = data.get('password')
    
    if not password:
        return jsonify({"error": "Password required"}), 400
        
    # Find user by ID in Postgres
    social_service = get_social_auth_service()
    user_record = social_service._get_user_by_id(user_id)
            
    if not user_record:
        return jsonify({"error": "User session invalid"}), 404
        
    success = social_service.set_password(user_record["email"], password)
    if success:
        return jsonify({"message": "Password added successfully. You can now login via email or social provider."})
    return jsonify({"error": "Failed to set password"}), 500

# --- Phase 06: MFA Endpoints ---
@auth_bp.route('/mfa/setup', methods=['POST'])
def mfa_setup():
    from services.system.totp_service import get_totp_service
    # In production, we'd load/save this secret in the DB for the user
    service = get_totp_service()
    secret = service.generate_new_secret()
    uri = service.get_provisioning_uri(secret, "admin")
    
    return jsonify({
        "secret": secret,
        "provisioning_uri": uri
    })

@auth_bp.route('/mfa/verify', methods=['POST'])
def mfa_verify():
    from services.system.totp_service import get_totp_service
    data = request.get_json()
    code = data.get('code')
    secret = data.get('secret') # In production, load from DB
    
    service = get_totp_service()
    is_valid = service.verify_code(secret, code)
    
    if is_valid:
        return jsonify({"valid": True, "message": "MFA Verified"})
    else:
        return jsonify({"valid": False, "error": "Invalid Code"}), 401
# --- Phase 13: Social/Vendor Auth Endpoints ---
@auth_bp.route('/social/login/<provider>', methods=['GET'])
def social_login(provider):
    """Initiates the OAuth flow for a vendor."""
    from services.system.social_auth_service import get_social_auth_service
    url = get_social_auth_service().initiate_auth_flow(provider)
    return jsonify({"redirect_url": url})

@auth_bp.route('/social/callback/<provider>', methods=['POST'])
def social_callback(provider):
    """Handles the OAuth callback from a vendor."""
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400
        
    try:
        from services.system.social_auth_service import get_social_auth_service
        result = get_social_auth_service().handle_callback(provider, code)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
