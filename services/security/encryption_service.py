"""
==============================================================================
FILE: services/security/encryption_service.py
ROLE: Security Governor
PURPOSE:
    Handle encryption and decryption of sensitive data, such as API keys.
    Ensures that credentials are never stored in plain text.
    
    1. Key Management:
       - Uses a local master key (derived from env) to encrypt/decrypt secrets.
       - Placeholder for future integration with HashiCorp Vault.
       
    2. Data Protection:
       - AES-256-GCM encryption for high security.
       
CONTEXT: 
    Part of Part VIII: Operations & Autonomy (Phase 32)
    This service is critical for "Fort Knox" level security, preventing leaks
    of broker credentials.
==============================================================================
"""

import os
import base64
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

class EncryptionService:
    def __init__(self, master_password: str = None):
        """
        Initialize the encryption service with a master password.
        Usually loaded from an environment variable.
        """
        if master_password is None:
            master_password = os.getenv("ENCRYPTION_MASTER_KEY", "default-insecure-key-replace-me")
            
        self.salt = b'ai-investor-salt' # Fixed salt for deterministic key derivation (Simulated)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = kdf.derive(master_password.encode())
        self.aesgcm = AESGCM(self.key)

    def encrypt_api_key(self, plain_text: str) -> str:
        """
        Encrypt a plain text string (e.g., an API key).
        Returns a base64 encoded string containing nonce + ciphertext.
        """
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plain_text.encode(), None)
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    def decrypt_api_key(self, encrypted_b64: str) -> str:
        """
        Decrypt a base64 encoded encrypted key.
        """
        data = base64.b64decode(encrypted_b64)
        nonce = data[:12]
        ciphertext = data[12:]
        decrypted_data = self.aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode('utf-8')

# Singleton
_instance = None

def get_encryption_service() -> EncryptionService:
    global _instance
    if _instance is None:
        _instance = EncryptionService()
    return _instance
