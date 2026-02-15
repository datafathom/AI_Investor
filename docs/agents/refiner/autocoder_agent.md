# Autocoder Agent (`autocoder_agent.py`)

## Description
The `AutocoderAgent` is an autonomous code generation and execution agent. It translates natural language prompts into Python code, validates the code for security, and executes it in a sandboxed environment.

## Role in Department
This agent acts as a "Technical specialist" that can be invoked by other agents to perform data analysis, strategy development, or automation tasks that require custom code.

## Input & Output
- **Input**: Natural language prompt (e.g., "Analyze the volatility of AAPL over the last 30 days") and optional context variables.
- **Output**: A dictionary containing the generated code, execution results (stdout/stderr), and any errors encountered.

## Pipelines & Integration
- **LLM**: Uses `gpt-4o` for high-fidelity code generation.
- **Sandbox**: Integrates with `SandboxExecutor` which uses AST parsing to detect dangerous operations (like `os.system`) and executes code in an isolated subprocess.
- **Event Bus**: Listens for `code_generation_request` events on the Kafka stream.

## Security Features
- **AST Validation**: Prevents execution of dangerous functions and blocked imports.
- **Subprocess Isolation**: Code runs in a temporary environment with a set timeout.
- **Whitelist/Blacklist**: Strict control over available libraries.
