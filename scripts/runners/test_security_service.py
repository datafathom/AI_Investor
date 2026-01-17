"""
==============================================================================
FILE: scripts/runners/test_security_service.py
ROLE: Security Verifier
PURPOSE:
    Verify the EncryptionService can successfully encrypt and decrypt
    sensitive strings.
       
CONTEXT: 
    Part of Phase 32: Security Hardening.
==============================================================================
"""

from services.security.encryption_service import get_encryption_service

def run_test_security(args=None):
    """
    Test Phase 32 Security Service.
    """
    print("Testing Security Encryption Service...")
    
    security = get_encryption_service()
    
    test_key = "ALPHAVANTAGE_KEY_123456789"
    print(f"\nOriginal Key:  {test_key}")
    
    # 1. Encrypt
    encrypted = security.encrypt_api_key(test_key)
    print(f"Encrypted (B64): {encrypted}")
    
    # 2. Decrypt
    decrypted = security.decrypt_api_key(encrypted)
    print(f"Decrypted Key:  {decrypted}")
    
    if decrypted == test_key:
        print("\n✅ Security Logic Verified: Encryption/Decryption Successful.")
    else:
        print("\n❌ Security Logic Failed: Decryption mismatch.")
