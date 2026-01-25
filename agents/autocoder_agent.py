"""
==============================================================================
FILE: agents/autocoder_agent.py
ROLE: Autonomous Code Generation Agent
PURPOSE: Generates and executes Python code from natural language prompts.
         Used for trading strategy development, data analysis, and automation.

INTEGRATION POINTS:
    - OpenAIClient: Code generation via GPT-4
    - ModelManager: LLM routing and governance
    - SandboxExecutor: Secure code execution environment
    - CommandProcessor: Natural language command parsing

SECURITY:
    - All code validated with AST parsing before execution
    - Execution sandboxed in isolated subprocess
    - Restricted imports and system access
    - Code injection prevention

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import ast
import asyncio
import subprocess
import sys
import tempfile
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider, ModelConfig
from services.ai.openai_client import get_openai_client

logger = logging.getLogger(__name__)


@dataclass
class CodeExecutionResult:
    """Result of code execution"""
    success: bool
    output: str
    error: Optional[str] = None
    return_value: Any = None
    execution_time_ms: int = 0


class SandboxExecutor:
    """
    Secure sandbox for executing generated Python code.
    Uses subprocess isolation and restricted imports.
    """
    
    # Allowed imports (whitelist approach)
    ALLOWED_IMPORTS = {
        'math', 'random', 'datetime', 'json', 'collections', 'itertools',
        'numpy', 'pandas', 'scipy', 'sklearn',  # Data science libraries
        'requests', 'httpx',  # HTTP libraries (with caution)
    }
    
    # Blocked imports (security risk)
    BLOCKED_IMPORTS = {
        'os', 'sys', 'subprocess', 'eval', 'exec', 'compile', '__builtins__',
        'open', 'file', 'input', 'raw_input', 'execfile', 'reload'
    }
    
    def __init__(self, timeout_seconds: int = 30):
        """
        Initialize sandbox executor.
        
        Args:
            timeout_seconds: Maximum execution time
        """
        self.timeout = timeout_seconds
    
    def validate_code(self, code: str) -> tuple:
        """
        Validate Python code syntax and security.
        
        Args:
            code: Python code to validate
            
        Returns:
            (is_valid, error_message)
        """
        try:
            # Parse AST to check syntax
            tree = ast.parse(code)
            
            # Check for dangerous operations
            for node in ast.walk(tree):
                # Block eval/exec calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec', 'compile', '__import__']:
                            return False, f"Dangerous function call detected: {node.func.id}"
                
                # Block certain imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split('.')[0] in self.BLOCKED_IMPORTS:
                            return False, f"Blocked import detected: {alias.name}"
                
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module.split('.')[0] in self.BLOCKED_IMPORTS:
                        return False, f"Blocked import detected: {node.module}"
            
            return True, None
            
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    async def execute(self, code: str, context: Optional[Dict[str, Any]] = None) -> CodeExecutionResult:
        """
        Execute code in sandboxed environment.
        
        Args:
            code: Python code to execute
            context: Optional context variables to inject
            
        Returns:
            CodeExecutionResult with output and errors
        """
        start_time = datetime.now()
        
        # Validate code first
        is_valid, error = self.validate_code(code)
        if not is_valid:
            return CodeExecutionResult(
                success=False,
                output="",
                error=error,
                execution_time_ms=0
            )
        
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            # Inject context variables if provided
            if context:
                context_code = "\n".join([f"{k} = {repr(v)}" for k, v in context.items()])
                full_code = f"{context_code}\n\n{code}"
            else:
                full_code = code
            
            f.write(full_code)
            temp_file = f.name
        
        try:
            # Execute in subprocess with timeout
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=tempfile.gettempdir()
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return CodeExecutionResult(
                    success=False,
                    output="",
                    error=f"Execution timeout after {self.timeout} seconds",
                    execution_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
                )
            
            execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
            
            stdout_str = stdout.decode('utf-8') if stdout else ""
            stderr_str = stderr.decode('utf-8') if stderr else ""
            
            return CodeExecutionResult(
                success=process.returncode == 0,
                output=stdout_str,
                error=stderr_str if stderr_str else None,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            return CodeExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                execution_time_ms=int((datetime.now() - start_time).total_seconds() * 1000)
            )
        finally:
            # Cleanup temp file
            try:
                os.unlink(temp_file)
            except:
                pass


class AutocoderAgent(BaseAgent):
    """
    Autonomous code generation agent.
    Generates Python code from natural language and executes it safely.
    """
    
    def __init__(self):
        """Initialize Autocoder agent with OpenAI provider"""
        super().__init__("AutocoderAgent", provider=ModelProvider.OPENAI)
        self.openai_client = get_openai_client()
        self.sandbox = SandboxExecutor(timeout_seconds=30)
        logger.info("AutocoderAgent initialized")
    
    async def generate_code(
        self,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        execute: bool = True
    ) -> Dict[str, Any]:
        """
        Generate Python code from natural language prompt.
        
        Args:
            prompt: Natural language description of desired code
            context: Optional context variables for execution
            execute: Whether to execute the generated code
            
        Returns:
            Dict with 'code', 'result', 'execution_result'
        """
        system_prompt = """You are an expert Python programmer specializing in financial data analysis and trading strategies.

Generate clean, efficient Python code that:
1. Uses standard libraries (math, datetime, json, collections) and data science libraries (numpy, pandas)
2. Avoids dangerous operations (no eval, exec, file I/O, system calls)
3. Includes clear comments
4. Returns results via print() or return statements

Generate ONLY the Python code, no explanations or markdown formatting."""

        user_prompt = f"""Write Python code to: {prompt}

Requirements:
- Use standard libraries and data science tools
- No file I/O or system operations
- Return results via print() statements
- Include helpful comments"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            # Generate code using OpenAI
            response = await self.openai_client.chat_completion(
                messages=messages,
                model="gpt-4o",
                temperature=0.3,  # Lower temperature for more deterministic code
                max_tokens=2000
            )
            
            code = response.content.strip()
            
            # Remove markdown code blocks if present
            if code.startswith("```python"):
                code = code[9:]
            if code.startswith("```"):
                code = code[3:]
            if code.endswith("```"):
                code = code[:-3]
            code = code.strip()
            
            result = {
                "code": code,
                "model": response.model,
                "tokens_used": response.usage.total_tokens,
                "execution_result": None
            }
            
            # Execute code if requested
            if execute:
                exec_result = await self.sandbox.execute(code, context)
                result["execution_result"] = {
                    "success": exec_result.success,
                    "output": exec_result.output,
                    "error": exec_result.error,
                    "execution_time_ms": exec_result.execution_time_ms
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return {
                "code": None,
                "error": str(e),
                "execution_result": None
            }
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process incoming event from Kafka stream.
        Autocoder listens for 'code_generation_request' events.
        """
        if event.get("type") == "code_generation_request":
            prompt = event.get("prompt", "")
            context = event.get("context", {})
            
            # Generate code asynchronously
            asyncio.create_task(self._handle_code_request(prompt, context, event.get("request_id")))
            return {"status": "processing", "request_id": event.get("request_id")}
        
        return None
    
    async def _handle_code_request(self, prompt: str, context: Dict, request_id: Optional[str]):
        """Handle code generation request asynchronously"""
        result = await self.generate_code(prompt, context, execute=True)
        logger.info(f"Code generation completed for request {request_id}")


# Singleton instance
_autocoder_agent: Optional[AutocoderAgent] = None


def get_autocoder_agent() -> AutocoderAgent:
    """Get singleton Autocoder agent instance"""
    global _autocoder_agent
    if _autocoder_agent is None:
        _autocoder_agent = AutocoderAgent()
    return _autocoder_agent
