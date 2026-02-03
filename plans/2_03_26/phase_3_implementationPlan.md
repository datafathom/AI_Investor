# Phase 3: Agent Architecture Clean-up
## Implementation Plan - Source of Truth

**Parent Roadmap**: [ROADMAP_2_03_26.md](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/plans/2_03_26/ROADMAP_2_03_26.md)

---

## 📋 Phase Overview

| Attribute | Value |
|-----------|-------|
| **Phase Number** | 3 |
| **Focus Area** | Agent Prompt Externalization |
| **Deliverables** | 1 (Prompt Architecture Refactor) |
| **Estimated Effort** | 2-3 days |
| **Dependencies** | None (Independent refactor) |

---

## 3.1 Prompt Externalization (App-Wide)

### Goal
Decouple ALL agent prompts from ALL Python code. No exceptions.

### Scope: The 11 Core Agents
We have verified the following agents exist in `agents/`. Each MUST have its prompt extracted to `agents/prompts/`.

| Agent File | Status | Target Prompt File |
|------------|--------|--------------------|
| `autocoder_agent.py` | ✅ Done | `prompts/autocoder_system.txt` |
| `backtest_agent.py` | ❌ Pending | `prompts/backtest_system.txt` |
| `conviction_analyzer_agent.py` | ❌ Pending | `prompts/conviction_system.txt` |
| `debate_chamber_agent.py` | ❌ Pending | `prompts/debate_system.txt` |
| `protector_agent.py` | ❌ Pending | `prompts/protector_system.txt` |
| `research_agent.py` | ❌ Pending | `prompts/research_system.txt` |
| `searcher_agent.py` | ❌ Pending | `prompts/searcher_system.txt` |
| `stacker_agent.py` | ❌ Pending | `prompts/stacker_system.txt` |
| `consensus/voting_agent.py` | ❌ Pending | `prompts/consensus/voting_system.txt` |
| `personas/bull_persona.py` | ❌ Pending | `prompts/personas/bull_system.txt` |
| `personas/bear_persona.py` | ❌ Pending | `prompts/personas/bear_system.txt` |

### Detailed Implementation

#### 1. Enhanced `PromptLoader`
We need a robust loader that handles subdirectories (for consensus/personas).
```python
# agents/prompt_loader.py
class PromptLoader:
    PROMPT_DIR = Path(__file__).parent / "prompts"

    @classmethod
    def load(cls, agent_name: str, category: str = None) -> str:
        """
        Load system prompt.
        If category is provided (e.g. 'consensus'), looks in prompts/consensus/{agent_name}_system.txt
        """
        base = cls.PROMPT_DIR / category if category else cls.PROMPT_DIR
        target = base / f"{agent_name}_system.txt"
        
        if not target.exists():
             raise FileNotFoundError(f"Missing prompt: {target}")
        return target.read_text()
```

#### 2. Migration Strategy
For *each* of the 11 agents above:
1.  **Extract**: Cut the `"""..."""` triple-quoted string from `__init__` or class constants.
2.  **Paste**: Create the corresponding `.txt` file in `agents/prompts/`.
3.  **Refactor**:
    ```python
    # agents/my_agent.py
    from agents.prompt_loader import PromptLoader
    
    class MyAgent(BaseAgent):
        def __init__(self):
            # OLD: self.system_prompt = """You are..."""
            # NEW:
            self.system_prompt = PromptLoader.load("my", category=None)
    ```

#### 3. Strict Linting Rule
We will add a "No Hardcoded Prompts" check in CI.
- **Script**: `scripts/ci/check_prompts.py`
- **Logic**: Fail if any file in `agents/*.py` contains a string literal longer than 150 characters that starts with "You are" or "Act as".

## 📊 Verification Plan
### Automated Tests
1.  **Unit Tests**: `tests/agents/test_prompt_loader.py`
    - Verify it can load *every single* prompt file listed above.
    - Verify it raises `FileNotFoundError` for missing prompts.
2.  **Agent Init Tests**: `tests/agents/test_initialization.py`
    - Import every agent class.
    - Instantiate it (mocking dependencies if needed).
    - Assert `agent.system_prompt` is not empty and matches the file content.

### Manual Verification
- **Command**: `python scripts/ci/check_prompts.py` -> Must pass.
- **Visual Check**: Browse `agents/prompts/` to ensure file names match the agent names exactly.
