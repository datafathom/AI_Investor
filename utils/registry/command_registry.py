"""
==============================================================================
FILE: utils/registry/command_registry.py
ROLE: CLI Orchestrator (Registry)
PURPOSE: Maps CLI strings to specialized Python handler functions.
USAGE: registry.get_handler(['test-ingestion'])
INPUT/OUTPUT:
    - Input: JSON config file (config/cli_configuration.json)
    - Output: Callable handler function or command definition Dict.
==============================================================================
"""

import json
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

logger = logging.getLogger(__name__)


class CommandRegistry:
    """
    Registry for managing CLI commands loaded from JSON configuration.
    """
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.handler_cache: Dict[str, Callable] = {}
        self.config_path: Optional[Path] = None
    
    def load_config(self, config_path: str = "config/cli_configuration.json") -> bool:
        self.config_path = Path(config_path)
        
        if not self.config_path.exists():
            logger.error(f"Configuration file not found: {config_path}")
            return False
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False
    
    def get_command(self, command_path: List[str]) -> Optional[Dict[str, Any]]:
        if not self.config:
            return None
        
        current = self.config.get("commands", {})
        
        for i, part in enumerate(command_path):
            if part not in current:
                return None
            
            cmd_def = current[part]
            
            if i == len(command_path) - 1:
                return cmd_def
            
            if "subcommands" in cmd_def:
                current = cmd_def["subcommands"]
            else:
                return None
        
        return None
    
    def get_handler(self, command_path: List[str]) -> Optional[Callable]:
        path_str = ".".join(command_path)
        if path_str in self.handler_cache:
            return self.handler_cache[path_str]
        
        cmd_def = self.get_command(command_path)
        if not cmd_def:
            return None
        
        handler_str = cmd_def.get("handler")
        if not handler_str:
            return None
        
        try:
            handler = self._load_handler(handler_str)
            if handler:
                self.handler_cache[path_str] = handler
            return handler
        except Exception as e:
            logger.error(f"Error loading handler '{handler_str}': {e}")
            return None
    
    def _load_handler(self, handler_str: str) -> Optional[Callable]:
        try:
            if ":" not in handler_str:
                return None
            
            module_path, function_name = handler_str.split(":", 1)
            module = importlib.import_module(module_path)
            
            if not hasattr(module, function_name):
                return None
            
            return getattr(module, function_name)
        except Exception as e:
            logger.error(f"Error loading handler '{handler_str}': {e}")
            return None
    
    def list_commands(self) -> Dict[str, Dict]:
        return self.config.get("commands", {})
