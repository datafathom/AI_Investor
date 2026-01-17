"""
==============================================================================
FILE: tests/analysis/test_autocoder.py
ROLE: The Quality Gate
PURPOSE:
    Verify the sandbox properly restricts access and validates AI code.
==============================================================================
"""

import pytest
from services.analysis.autocoder import AutoCoder, SandboxError

class TestAutoCoder:
    
    def test_code_generation(self):
        coder = AutoCoder()
        code = coder.generate_code("Double the input")
        assert "class CustomAdapter" in code
        assert "Double the input" in code

    def test_sandbox_safety(self):
        coder = AutoCoder()
        
        # Test 1: Malicious import
        malicious_code = "import os\nos.system('echo hacked')"
        assert coder.validate_code(malicious_code) == False
        
        # Test 2: File access
        file_code = "open('secret.txt', 'w')"
        assert coder.validate_code(file_code) == False

    def test_successful_execution(self):
        coder = AutoCoder()
        valid_code = """
class MyAdapter:
    def process_data(self, val): return val + 10
def get_instance(): return MyAdapter()
"""
        assert coder.validate_code(valid_code) == True
        
        instance = coder.deploy_module("test_mod", valid_code)
        assert instance is not None
        assert instance.process_data(5) == 15

    def test_missing_interface(self):
        coder = AutoCoder()
        invalid_code = "class NoInstance: pass" # Missing get_instance
        assert coder.validate_code(invalid_code) == False
