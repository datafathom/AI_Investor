import logging
import json
from typing import Dict, Any, Type, Optional, Callable
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

class ToolValidationError(Exception):
    """Raised when tool arguments fail schema validation."""
    pass

class BaseTool(ABC):
    """
    Abstract base class for all agent tools.
    Encapsulates schema, validation, and execution logic.
    """
    name: str
    description: str
    args_schema: Type[BaseModel]

    def __init__(self):
        self._validate_config()

    def _validate_config(self):
        if not hasattr(self, 'name') or not self.name:
            raise ValueError("Tool must have a 'name' attribute.")
        if not hasattr(self, 'description') or not self.description:
            raise ValueError("Tool must have a 'description' attribute.")
        if not hasattr(self, 'args_schema') or not issubclass(self.args_schema, BaseModel):
            raise ValueError("Tool must have a Pydantic 'args_schema'.")

    def validate_args(self, args: Dict[str, Any]) -> BaseModel:
        """
        Validate dictionary arguments against the Pydantic schema.
        """
        try:
            return self.args_schema(**args)
        except ValidationError as e:
            raise ToolValidationError(f"Tool argument validation failed: {str(e)}")

    @abstractmethod
    def run(self, args: BaseModel) -> Any:
        """
        Execute the tool action. Must be implemented by subclasses.
        """
        pass

    async def arun(self, args: BaseModel) -> Any:
        """
        Async execution hook. Defaults to sync run if not overridden.
        """
        return self.run(args)
    
    @property
    def schema_json(self) -> Dict[str, Any]:
        """
        Returns the JSON schema for the tool arguments.
        Useful for passing to LLMs.
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.args_schema.model_json_schema()
        }

class ToolRegistry:
    """
    Singleton registry for managing available tools.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
            cls._instance.tools = {}
        return cls._instance

    def register(self, tool_cls: Type[BaseTool]):
        """Register a new tool class."""
        try:
            tool = tool_cls()
            self.tools[tool.name] = tool
            logger.info(f"Registered tool: {tool.name}")
        except Exception as e:
            logger.error(f"Failed to register tool {tool_cls}: {e}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self.tools.get(name)

    def get_all_schemas(self) -> list:
        return [t.schema_json for t in self.tools.values()]

# Singleton
tool_registry = ToolRegistry()

def get_tool_registry() -> ToolRegistry:
    return tool_registry
