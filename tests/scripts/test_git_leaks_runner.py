import pytest
import subprocess
import shutil
from unittest.mock import patch, MagicMock
from scripts.runners.git_leaks_runner import run_gitleaks_audit

@patch("shutil.which")
def test_run_gitleaks_audit_not_installed(mock_which):
    """Test when gitleaks is not installed."""
    mock_which.return_value = None
    
    with patch("builtins.print") as mock_print:
        result = run_gitleaks_audit()
        assert result is False
        mock_print.assert_any_call("\n❌ Error: 'gitleaks' executable not found in PATH.")

@patch("shutil.which")
def test_run_gitleaks_audit_no_git(mock_which):
    """Test when .git does not exist."""
    mock_which.return_value = "/usr/bin/gitleaks"
    
    # Mock Path.exists locally within the module
    with patch("scripts.runners.git_leaks_runner.Path.exists") as mock_exists:
        # mock_exists should return False for the .git check
        mock_exists.return_value = False
        
        with patch("builtins.print") as mock_print:
            result = run_gitleaks_audit()
            assert result is False
            # Just check if ANY call starts with the error prefix
            any_found = any("❌ Error: No .git repository found" in str(call) for call in mock_print.call_args_list)
            assert any_found

@patch("shutil.which")
@patch("subprocess.run")
@patch("scripts.runners.git_leaks_runner.Path.exists")
def test_run_gitleaks_audit_success(mock_exists, mock_run, mock_which):
    """Test successful gitleaks scan."""
    mock_which.return_value = "/usr/bin/gitleaks"
    mock_exists.return_value = True
    
    # Mock subprocess success
    mock_process = MagicMock()
    mock_process.returncode = 0
    mock_run.return_value = mock_process
    
    with patch("builtins.print") as mock_print:
        result = run_gitleaks_audit()
        assert result is True
        mock_print.assert_any_call("\n✅ Gitleaks: No leaks detected.")
        
@patch("shutil.which")
@patch("subprocess.run")
@patch("scripts.runners.git_leaks_runner.Path.exists")
def test_run_gitleaks_audit_leaks_detected(mock_exists, mock_run, mock_which):
    """Test when gitleaks detects leaks (return code 1)."""
    mock_which.return_value = "/usr/bin/gitleaks"
    mock_exists.return_value = True
    
    # Mock subprocess failure (detected leaks)
    mock_process = MagicMock()
    mock_process.returncode = 1
    mock_run.return_value = mock_process
    
    with patch("builtins.print") as mock_print:
        result = run_gitleaks_audit()
        assert result is False
        mock_print.assert_any_call("\n⚠️  Gitleaks: Leaks were detected! Check the output above.")
