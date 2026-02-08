import os
import shutil
import base64
import logging
from typing import Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

class VaultService:
    """
    Handles folder encryption and decryption using AES-256 (Fernet).
    Compresses folders into tar archives before encryption.
    """

    def __init__(self):
        self.salt = b'\x12\x34\x56\x78\x90\xab\xcd\xef' # Static salt for simplicity in this dev phase

    def _derive_key(self, passkey: str) -> bytes:
        """Derives a Fernet-compatible key from a string passkey."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(passkey.encode()))
        return key

    def lock(self, directory_path: str, passkey: str) -> Optional[str]:
        """
        Compresses and encrypts a directory.
        Returns the path to the created .vault file.
        """
        if not os.path.exists(directory_path):
            logger.error(f"Directory not found: {directory_path}")
            return None

        vault_path = f"{directory_path.rstrip(os.sep)}.vault"
        archive_name = f"{directory_path.rstrip(os.sep)}_temp"
        
        try:
            # 1. Create a tar archive of the folder
            print(f"📦 Archiving {directory_path}...")
            shutil.make_archive(archive_name, 'tar', directory_path)
            temp_tar = f"{archive_name}.tar"

            # 2. Encrypt the tar file
            print(f"🔒 Encrypting vault...")
            key = self._derive_key(passkey)
            fernet = Fernet(key)

            with open(temp_tar, 'rb') as f:
                data = f.read()

            encrypted_data = fernet.encrypt(data)

            with open(vault_path, 'wb') as f:
                f.write(encrypted_data)

            # 3. Cleanup
            os.remove(temp_tar)
            shutil.rmtree(directory_path)
            
            logger.info(f"✅ Folder locked successfully: {vault_path}")
            return vault_path

        except Exception as e:
            logger.exception(f"❌ Failed to lock vault: {e}")
            if os.path.exists(f"{archive_name}.tar"):
                os.remove(f"{archive_name}.tar")
            return None

    def unlock(self, vault_path: str, passkey: str) -> bool:
        """
        Decrypts and extracts a vault file back into a directory.
        """
        if not os.path.exists(vault_path):
            logger.error(f"Vault file not found: {vault_path}")
            return False

        directory_path = vault_path.replace(".vault", "")
        temp_tar = f"{directory_path}_temp.tar"

        try:
            # 1. Decrypt the .vault file
            print(f"🔓 Decrypting vault...")
            key = self._derive_key(passkey)
            fernet = Fernet(key)

            with open(vault_path, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            with open(temp_tar, 'wb') as f:
                f.write(decrypted_data)

            # 2. Extract the archive
            print(f"📦 Extracting files to {directory_path}...")
            if os.path.exists(directory_path):
                shutil.rmtree(directory_path)
            os.makedirs(directory_path)
            shutil.unpack_archive(temp_tar, directory_path, 'tar')

            # 3. Cleanup
            os.remove(temp_tar)
            os.remove(vault_path)
            
            logger.info(f"✅ Vault unlocked successfully: {directory_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to unlock vault. Incorrect passkey or corrupted file: {e}")
            if os.path.exists(temp_tar):
                os.remove(temp_tar)
            return False
