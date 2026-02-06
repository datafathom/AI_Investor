"""
Sovereign Signature Middleware - FastAPI Dependency
Phase 1 Implementation: The Sovereign Kernel

This middleware enforces the Zero-Trust policy: no write operation
proceeds without a valid WebAuthn signature.

ACCEPTANCE CRITERIA from Phase_1_ImplementationPlan.md:
- C1: All write-api routes (v1/ledger/*) return 401 without X-Sovereign-Signature.
"""

import logging
from typing import Any, Dict, Optional
from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader

from services.auth.sovereign_auth_service import sovereign_auth_service

logger = logging.getLogger(__name__)

# Custom header for sovereign signatures
SOVEREIGN_SIGNATURE_HEADER = "X-Sovereign-Signature"
SOVEREIGN_CHALLENGE_HEADER = "X-Sovereign-Challenge-Id"

sovereign_signature_header = APIKeyHeader(
    name=SOVEREIGN_SIGNATURE_HEADER, 
    auto_error=False
)
sovereign_challenge_header = APIKeyHeader(
    name=SOVEREIGN_CHALLENGE_HEADER, 
    auto_error=False
)


class SovereignSignatureError(HTTPException):
    """Raised when sovereign signature validation fails."""
    def __init__(self, detail: str) -> None:
        super().__init__(status_code=401, detail=detail)
        logger.warning(f"Sovereign signature rejected: {detail}")


async def require_sovereign_signature(
    request: Request,
    signature: Optional[str] = Depends(sovereign_signature_header),
    challenge_id: Optional[str] = Depends(sovereign_challenge_header),
) -> Dict[str, Any]:
    """
    FastAPI dependency that enforces sovereign signature on write operations.
    
    This should be injected into all routes that mutate financial state:
    - POST /v1/ledger/*
    - POST /v1/orders/*
    - POST /v1/payments/*
    
    Returns:
        Dict containing the validated command payload and signature metadata.
    
    Raises:
        SovereignSignatureError: If signature is missing or invalid.
    """
    if not signature:
        raise SovereignSignatureError(
            "Missing X-Sovereign-Signature header. "
            "All write operations require biometric authorization."
        )
    
    if not challenge_id:
        raise SovereignSignatureError(
            "Missing X-Sovereign-Challenge-Id header. "
            "Obtain a challenge via POST /v1/auth/challenge first."
        )

    # Parse the request body for command binding verification
    try:
        body = await request.json()
    except Exception:
        body = {}

    # Decode signature from hex
    try:
        signature_bytes = bytes.fromhex(signature)
    except ValueError:
        raise SovereignSignatureError("Invalid signature encoding. Expected hex.")

    # Verify the signature against the challenge
    is_valid, message = sovereign_auth_service.verify_signature(
        challenge_id=challenge_id,
        signature=signature_bytes,
        authenticator_data=b"",  # Placeholder for full WebAuthn impl
        client_data_json=b"",    # Placeholder for full WebAuthn impl
        command_payload=body,
    )

    if not is_valid:
        raise SovereignSignatureError(f"Signature verification failed: {message}")

    logger.info(f"Sovereign signature verified for challenge {challenge_id}")
    
    return {
        "challenge_id": challenge_id,
        "verified": True,
        "command_payload": body,
    }


def skip_sovereign_signature() -> Dict[str, Any]:
    """
    Bypass dependency for read-only endpoints or development.
    
    WARNING: Only use this for GET endpoints or during local development.
    Production write endpoints MUST use require_sovereign_signature.
    """
    return {
        "challenge_id": None,
        "verified": False,
        "command_payload": {},
        "bypass": True,
    }
