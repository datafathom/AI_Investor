import os
import shutil
import pytest
from services.security.vault_service import VaultService

@pytest.fixture
def temp_vault_dir(tmp_path):
    """Creates a temporary directory for testing."""
    test_dir = tmp_path / "test_folder"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("Hello World")
    (test_dir / "sub").mkdir()
    (test_dir / "sub" / "file2.txt").write_text("Secret Data")
    return str(test_dir)

def test_vault_lock_unlock_success(temp_vault_dir):
    """Verify that a folder can be locked and unlocked with the correct passkey."""
    service = VaultService()
    passkey = "super_secret_123"
    
    # 1. Lock the folder
    vault_path = service.lock(temp_vault_dir, passkey)
    assert vault_path is not None
    assert os.path.exists(vault_path)
    assert not os.path.exists(temp_vault_dir)
    
    # 2. Unlock the folder
    success = service.unlock(vault_path, passkey)
    assert success is True
    assert os.path.exists(temp_vault_dir)
    assert not os.path.exists(vault_path)
    
    # Check content
    assert (os.path.join(temp_vault_dir, "file1.txt")) != ""
    with open(os.path.join(temp_vault_dir, "file1.txt"), "r") as f:
        assert f.read() == "Hello World"
    with open(os.path.join(temp_vault_dir, "sub", "file2.txt"), "r") as f:
        assert f.read() == "Secret Data"

def test_vault_unlock_fail_wrong_key(temp_vault_dir):
    """Verify that unlocking fails with an incorrect passkey."""
    service = VaultService()
    passkey = "correct_key"
    wrong_key = "wrong_key"
    
    # 1. Lock the folder
    vault_path = service.lock(temp_vault_dir, passkey)
    
    # 2. Try to unlock with wrong key
    success = service.unlock(vault_path, wrong_key)
    assert success is False
    assert not os.path.exists(temp_vault_dir)
    assert os.path.exists(vault_path)

def test_vault_lock_missing_dir():
    """Verify that locking a non-existent directory fails."""
    service = VaultService()
    result = service.lock("non_existent_path_xyz", "pass")
    assert result is None
