"""
==============================================================================
FILE: scripts/runners/vault_runner.py
ROLE: CLI Runner for Vault Operations
PURPOSE: Handles CLI commands for locking and unlocking encrypted vaults.
==============================================================================
"""

import os
import sys
import logging
from services.security.vault_service import VaultService

logger = logging.getLogger(__name__)

def lock_vault(path: str, passkey: str):
    """
    CLI Handler for locking a folder.
    Args:
        path (str): Path to the folder to encrypt.
        passkey (str): Secret passkey to use for encryption.
    """
    if not path or not passkey:
        print("❌ Error: Path and Passkey are required.")
        return

    service = VaultService()
    
    print(f"🔒 Locking vault: {path}...")
    vault_file = service.lock(path, passkey)
    
    if vault_file:
        print(f"✅ Success! Folder '{path}' has been encrypted into '{vault_file}'.")
        print("⚠️  The original folder has been removed. Store your passkey safely!")
    else:
        print(f"❌ Failed to lock vault '{path}'. Check logs for details.")

def unlock_vault(path: str, passkey: str):
    """
    CLI Handler for unlocking a vault.
    Args:
        path (str): Path to the .vault file to decrypt.
        passkey (str): Secret passkey to use for decryption.
    """
    if not path or not passkey:
        print("❌ Error: Path and Passkey are required.")
        return

    if not path.endswith(".vault"):
        print("❌ Error: Path must point to a '.vault' file.")
        return

    service = VaultService()
    
    print(f"🔓 Unlocking vault: {path}...")
    success = service.unlock(path, passkey)
    
    if success:
        print(f"✅ Success! Vault '{path}' has been decrypted and restored.")
    else:
        print(f"❌ Failed to unlock vault. Incorrect passkey or corrupted file.")
