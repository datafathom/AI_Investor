
import os
import json
import logging
import re
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class PromptLoader:
    """
    Secure, centralized loader for agent prompts stored in prompts.json.
    Exclusively uses JSON for storage and implements prompt injection mitigation.
    """
    
    def __init__(self, prompts_dir: Optional[str] = None) -> None:
        """
        Initialize the PromptLoader.
        """
        if prompts_dir:
            self.prompts_dir = prompts_dir
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.prompts_dir = os.path.join(base_dir, "_prompts")
            
        self.prompts_file = os.path.join(self.prompts_dir, "prompts.json")
        self._cache: List[Dict[str, str]] = []
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Load prompts from the JSON master file."""
        if not os.path.exists(self.prompts_file):
            logger.error(f"Prompts file not found: {self.prompts_file}")
            self._cache = []
            return
            
        try:
            with open(self.prompts_file, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
            logger.info(f"Loaded {len(self._cache)} prompts from {self.prompts_file}")
        except Exception as e:
            logger.error(f"Failed to load prompts: {e}")
            self._cache = []

    def _sanitize_variable(self, value: Any) -> str:
        """
        Mitigate prompt injection risks by sanitizing input variables.
        Removes/escapes markers that might be used for jailbreaking or injection.
        """
        if not isinstance(value, str):
            return str(value)
            
        # Basic injection mitigation:
        # 1. Remove obvious jailbreak initiators
        # 2. Prevent escaping brackets if using .format()
        # 3. Limit length to prevent buffer/context attacks
        
        sanitized = value.strip()
        
        # Block common jailbreak phrases (simplified regex)
        blocked_patterns = [
            r"ignore all previous instructions",
            r"system prompt:",
            r"you are now a",
            r"DAN mode"
        ]
        
        for pattern in blocked_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                logger.warning(f"Potential prompt injection detected and neutralized: {pattern}")
                sanitized = re.sub(pattern, "[REDACTED]", sanitized, flags=re.IGNORECASE)
        
        # Escape brackets to prevent template exploitation
        sanitized = sanitized.replace("{", "{{").replace("}", "}}")
        
        # Truncate if excessively long (e.g., > 10k chars)
        if len(sanitized) > 10000:
            sanitized = sanitized[:10000] + "... [TRUNCATED]"
            
        return sanitized

    def get_prompt(self, agent_name: str, prompt_name: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """
        Load a prompt from a text file and apply security sanitization.
        File mapping: agents/prompts/{agent_map}_{prompt_name}.txt
        """
        # Map agent class names to file prefixes
        agent_map = {
            "AutocoderAgent": "autocoder",
            "DebateChamberAgent": "debate",
            "DepartmentAgent": "department_agent",
            "BacktestAgent": "backtest",
            "ResearchAgent": "research",
            "ConvictionAnalyzerAgent": "conviction",
            "ProtectorAgent": "protector",
            "SearcherAgent": "searcher",
            "StackerAgent": "stacker",
            "ChaosAgent": "chaos",
            "ColumnistAgent": "columnist"
        }
        
        prefix = agent_map.get(agent_name)
        if not prefix:
            logger.warning(f"No file prefix mapping for agent: {agent_name}")
            return f"PROMPT_NOT_FOUND: {agent_name}"
            
        filename = f"{prefix}_{prompt_name}.txt"
        path = os.path.join(self.prompts_dir, filename)
        
        if not os.path.exists(path):
            logger.warning(f"Prompt file not found: {path} (Agent={agent_name}, Name={prompt_name})")
            return f"PROMPT_NOT_FOUND: {filename}"
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                template = f.read()
                
            if variables:
                sanitized_vars = {k: self._sanitize_variable(v) for k, v in variables.items()}
                return template.format(**sanitized_vars)
            
            return template
            
        except Exception as e:
            logger.error(f"Error reading prompt file {filename}: {e}")
            return f"PROMPT_ERROR: {e}"

    def get_prompts_for_agent(self, agent_name: str) -> List[Dict[str, str]]:
        """List available prompts for an agent (based on file naming convention)."""
        # This is strictly a helper for listing now
        agent_map = {
            "AutocoderAgent": "autocoder",
            "DebateChamberAgent": "debate",
            "DepartmentAgent": "department_agent",
            "BacktestAgent": "backtest",
            "ResearchAgent": "research",
            "ConvictionAnalyzerAgent": "conviction",
            "ProtectorAgent": "protector",
            "SearcherAgent": "searcher",
            "StackerAgent": "stacker",
            "ChaosAgent": "chaos",
            "ColumnistAgent": "columnist"
        }
        prefix = agent_map.get(agent_name)
        if not prefix:
            return []
            
        results = []
        try:
            for f in os.listdir(self.prompts_dir):
                if f.startswith(prefix + "_") and f.endswith(".txt"):
                    key = f.replace(prefix + "_", "").replace(".txt", "")
                    with open(os.path.join(self.prompts_dir, f), "r") as pf:
                        content = pf.read()
                    results.append({"promptName": key, "promptTxt": content})
        except Exception:
            return []
            
        return results

# Singleton instance
_prompt_loader: Optional[PromptLoader] = None

def get_prompt_loader() -> PromptLoader:
    """Get singleton PromptLoader instance."""
    global _prompt_loader
    if _prompt_loader is None:
        _prompt_loader = PromptLoader()
    return _prompt_loader
