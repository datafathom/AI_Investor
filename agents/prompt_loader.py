
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
            self.prompts_dir = os.path.join(base_dir, "prompts")
            
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
        Exclusively load a prompt from JSON and apply security sanitization.
        
        Args:
            agent_name: Name of the agent (agentThatUses)
            prompt_name: Name of the specific prompt
            variables: Dict of variables to inject securely
        """
        # Find the prompt in cache
        prompt_data = next((p for p in self._cache if p.get("agentThatUses") == agent_name and p.get("promptName") == prompt_name), None)
        
        if not prompt_data:
            logger.warning(f"Prompt not found: Agent={agent_name}, Name={prompt_name}")
            return f"PROMPT_NOT_FOUND: {agent_name}.{prompt_name}"
            
        template = prompt_data.get("promptTxt", "")
        
        if variables:
            sanitized_vars = {k: self._sanitize_variable(v) for k, v in variables.items()}
            try:
                # Use standard format but we must be careful. 
                # Since we escaped { and } in sanitized_vars, we can now safely inject into the template
                # which HAS standard {keys}.
                return template.format(**sanitized_vars)
            except KeyError as e:
                logger.error(f"Missing variable for prompt '{prompt_name}': {e}")
                return template
            except Exception as e:
                logger.error(f"Formatting error for prompt '{prompt_name}': {e}")
                return template
                
        return template

    def get_prompts_for_agent(self, agent_name: str) -> List[Dict[str, str]]:
        """Return all prompts registered for a specific agent."""
        return [p for p in self._cache if p.get("agentThatUses") == agent_name]

# Singleton instance
_prompt_loader: Optional[PromptLoader] = None

def get_prompt_loader() -> PromptLoader:
    """Get singleton PromptLoader instance."""
    global _prompt_loader
    if _prompt_loader is None:
        _prompt_loader = PromptLoader()
    return _prompt_loader
