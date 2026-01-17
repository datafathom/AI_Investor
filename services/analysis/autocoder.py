"""
==============================================================================
FILE: services/analysis/autocoder.py
ROLE: The Architect
PURPOSE:
    Enable AI agents to write and validate their own code adapters.
    
    1. Code Generation: Prompting LLMs for modular code.
    2. Sandbox Execution: Running code in a restricted scope.
    3. Hot Swapping: Injecting validated modules into the runtime.
    
CONTEXT: 
    Phase 39: Auto-Coder (Self-Improving Agents).
==============================================================================
"""

import logging
import inspect
from typing import Dict, Any, Optional, Type
import sys
import importlib.util
import os

logger = logging.getLogger(__name__)

class SandboxError(Exception):
    """Raised when code violates sandbox constraints."""
    pass

class AutoCoder:
    """
    Orchestrates the lifecycle of self-generated code.
    """
    
    def __init__(self):
        self.registry = {}
        self.sandbox_globals = {
            "__name__": "autocoder_sandbox",
            "__doc__": None,
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "enumerate": enumerate,
                "zip": zip,
                "any": any,
                "all": all,
                "bool": bool,
                "set": set,
                "tuple": tuple,
                "__build_class__": __build_class__,
                "Exception": Exception,
                "ValueError": ValueError,
                "TypeError": TypeError,
                "KeyError": KeyError,
                "IndexError": IndexError,
                "StopIteration": StopIteration,
            }
        }

    def generate_code(self, task_description: str) -> str:
        """
        Mocked code generation. In a real scenario, this calls GPT-4/Claude.
        """
        logger.info(f"Generating code for task: {task_description}")
        
        # Example generated code template
        code = f'''
class CustomAdapter:
    """Auto-generated adapter for: {task_description}"""
    def __init__(self):
        self.name = "AutoAdapter"
    
    def process_data(self, value):
        # Basic logic simulation
        return {{"status": "success", "processed": value * 2, "task": "{task_description}"}}

def get_instance():
    return CustomAdapter()
'''
        return code.strip()

    def validate_code(self, code_str: str) -> bool:
        """
        Executes code in a restricted sandbox to check for syntax and basic safety.
        """
        # Use a single scope for globals and locals to avoid NameError issues with classes
        scope = self.sandbox_globals.copy()
        try:
            # Check for forbidden keywords before execution
            forbidden = ["import os", "import sys", "subprocess", "eval(", "exec(", "open("]
            for f in forbidden:
                if f in code_str:
                    raise SandboxError(f"Forbidden statement detected: {f}")
            
            exec(code_str, scope)
            
            # Verify interface
            if "get_instance" not in scope:
                raise SandboxError("Generated code must implement 'get_instance()'")
                
            logger.info("Code validation successful.")
            return True
        except Exception as e:
            logger.error(f"Sandbox Validation Failed: {str(e)}")
            return False

    def deploy_module(self, name: str, code_str: str) -> Optional[Any]:
        """
        Saves and dynamically loads the module.
        """
        if not self.validate_code(code_str):
            return None
            
        # Use the same validated scope
        scope = self.sandbox_globals.copy()
        exec(code_str, scope)
        instance = scope["get_instance"]()
        
        self.registry[name] = instance
        logger.info(f"Module '{name}' deployed successfully.")
        return instance

# Singleton instance
_autocoder = None

def get_autocoder() -> AutoCoder:
    global _autocoder
    if _autocoder is None:
        _autocoder = AutoCoder()
    return _autocoder
