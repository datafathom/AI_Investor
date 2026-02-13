import logging
import io
import sys
import contextlib
import traceback
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class NotebookRunner:
    """
    Executes Python code cells in a persistent stateful environment.
    """
    def __init__(self):
        self.kernels: Dict[str, Dict[str, Any]] = {}

    def get_kernel(self, kernel_id: str) -> Dict[str, Any]:
        if kernel_id not in self.kernels:
            self.kernels[kernel_id] = {
                "globals": {},
                "locals": {},
                "history": []
            }
        return self.kernels[kernel_id]

    async def execute_cell(self, kernel_id: str, code: str) -> Dict[str, Any]:
        kernel = self.get_kernel(kernel_id)
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        result = None
        error = None
        
        try:
            with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
                # We use exec/eval to run the code in the kernel's namespace
                # Check if the last line is an expression to return its value like Jupyter
                try:
                    tree = compile(code, '<string>', 'exec', flags=0, dont_inherit=True)
                except SyntaxError:
                    # Maybe it's just an expression?
                    try:
                        tree = compile(code, '<string>', 'eval', flags=0, dont_inherit=True)
                    except SyntaxError:
                        # Nope, it's a real syntax error in statements probably
                        pass
                
                # Simple execution for now: just exec
                # To support "last line expression", we'd need AST parsing, but let's stick to exec for MVP
                exec(code, kernel["globals"], kernel["locals"])
                
        except Exception:
            error = traceback.format_exc()
            # print(error, file=stderr_capture) # Optionally capture it in stderr too

        output = stdout_capture.getvalue()
        error_output = stderr_capture.getvalue()
        
        if error:
            error_output += "\n" + error

        return {
            "stdout": output,
            "stderr": error_output,
            "result": str(result) if result is not None else None
        }

    async def restart_kernel(self, kernel_id: str):
        if kernel_id in self.kernels:
            del self.kernels[kernel_id]
        return self.get_kernel(kernel_id)
