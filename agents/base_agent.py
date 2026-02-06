"""
==============================================================================
FILE: agents/base_agent.py
ROLE: Abstract Base Class
PURPOSE: Defines the interface and core logic (start/stop/health) for all agents.
USAGE: Inherit from BaseAgent and implement process_event(event).
INPUT/OUTPUT:
    - Input: Dict[str, Any] (Kafka/Event payload)
    - Output: Optional[Dict[str, Any]] (Response or action)
==============================================================================
"""
from abc import ABC, abstractmethod
import logging
import json
from typing import Any, Dict, Optional, List
from enum import Enum
from datetime import datetime, timezone
from services.infrastructure.state_manager import get_fsm_manager, AgentState

logger = logging.getLogger(__name__)


from services.system.model_manager import get_model_manager, ModelProvider, ModelConfig

# AgentState is now imported from state_manager

class BaseAgent(ABC):
    """
    Abstract base class for all AI Investor agents.
    
    Attributes:
        name (str): Unique identifier for the agent.
        is_active (bool): Whether the agent is currently processing events.
        state (AgentState): The current logical state of the agent.
        model_config (ModelConfig): The preferred LLM configuration for this agent.
        parent_job_id (str): Associated worker job ID.
        step_id (str): Current execution step ID.
    """
    
    def __init__(self, name: str, provider: ModelProvider = ModelProvider.GEMINI) -> None:
        """
        Initialize the base agent.
        
        Args:
            name: Unique identifier for this agent instance.
            provider: The preferred LLM provider (defaults to Gemini/Free-tier).
        """
        self.name = name
        self.is_active = False
        self.state = AgentState.INIT
        self.parent_job_id = None
        self.step_id = "0"
        self.fsm = get_fsm_manager()
        self.model_manager = get_model_manager()
        
        # Default model assignment (Agnostic setup)
        model_map = {
            ModelProvider.OPENAI: "gpt-4o",
            ModelProvider.ANTHROPIC: "claude-3-5-sonnet-20240620",
            ModelProvider.GEMINI: "gemini-1.5-flash",
            ModelProvider.PERPLEXITY: "llama-3-sonar-large-32k-online"
        }
        
        self.model_config = ModelConfig(
            provider=provider,
            model_id=model_map.get(provider, "mock-model")
        )
        
        logger.info(f"Agent '{self.name}' initialized with {provider.value} ({self.model_config.model_id})")
    
    async def transition_to(self, new_state: AgentState, reason: str = "") -> None:
        """Managed state transition with deterministic FSM validation."""
        old_state = self.state
        
        if not self.fsm.validate_transition(old_state, new_state):
            logger.warning(f"Invalid state transition attempted for {self.name}: {old_state.value} -> {new_state.value}")
            # Enforce security halt on invalid transition
            await self.emit_trace(
                label="SECURITY_HALT",
                content=f"Invalid transition {old_state.value} -> {new_state.value} BLOCKED.",
                type="error"
            )
            self.state = AgentState.SECURITY_HALT
            raise RuntimeError(f"FSM Security Violation: {old_state.value} -> {new_state.value} is not allowed.")

        self.state = new_state
        
        # Persist full context for potential resume
        context_snapshot = {
            "reason": reason,
            "step_id": self.step_id,
            "parent_job_id": self.parent_job_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.fsm.save_state(self.name, self.state, context_snapshot)
        
        await self.emit_trace(
            label="STATE_TRANSITION",
            content=f"Transition: {old_state.value} -> {new_state.value}. Reason: {reason}",
            type="state_transition",
            metadata=context_snapshot
        )
        logger.info(f"Agent {self.name} transitioned: {old_state.value} -> {new_state.value}")

    async def load_saved_state(self) -> bool:
        """
        Attempt to restore agent state from Redis.
        Returns True if state was restored.
        """
        saved = self.fsm.load_state(self.name)
        if saved:
            try:
                self.state = AgentState(saved["state"])
                ctx = saved.get("context", {})
                self.step_id = ctx.get("step_id", self.step_id)
                self.parent_job_id = ctx.get("parent_job_id", self.parent_job_id)
                
                logger.info(f"Restored agent {self.name} to state {self.state.value}")
                await self.emit_trace("STATE_RESTORED", f"Resumed from {self.state.value}", type="info")
                return True
            except Exception as e:
                logger.error(f"Failed to parse saved state for {self.name}: {e}")
        return False

    async def emit_trace(self, label: str, content: str, type: str = "info", metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Emit a trace event for live observability (Socket.io + Postgres).
        """
        from services.system.socket_manager import get_socket_manager
        from utils.database_manager import get_database_manager
        
        socket = get_socket_manager()
        db = get_database_manager()
        
        trace_payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": self.name,
            "parent_job_id": self.parent_job_id,
            "step_id": self.step_id,
            "label": label,
            "content": content,
            "type": type,
            "state": self.state.value,
            "metadata": metadata or {}
        }
        
        # 1. Emit to Socket.io for Live HUD
        socket.emit_event(f"TRACE_{self.name}", trace_payload)
        
        # 2. Persist to Postgres for Auditing
        try:
            with db.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO agent_traces (agent_id, parent_job_id, step_id, label, content, type, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (self.name, self.parent_job_id, self.step_id, label, content, type, json.dumps(metadata or {})))
        except Exception:
            logger.exception("Failed to persist trace to database")
        
        # 3. Log to Python Logger
        log_msg = f"[{self.name}] [{label}] {content}"
        if type == "error":
            logger.error(log_msg)
        else:
            logger.debug(log_msg)

    async def get_completion(self, prompt: str, system_message: Optional[str] = None, use_cache: bool = True) -> str:
        """
        LLM Agnostic completion interface for agents with built-in caching.
        """
        from services.infrastructure.cache_service import get_agent_cache
        cache = get_agent_cache()
        
        sys_msg = system_message or f"You are the {self.name} agent in the AI Investor platform."
        
        # 1. Check Cache
        if use_cache:
            cached_resp = cache.get(self.name, prompt, sys_msg)
            if cached_resp:
                return cached_resp
        
        # 2. Get fresh completion
        response = await self.model_manager.get_completion(
            prompt=prompt,
            config=self.model_config,
            system_message=sys_msg
        )
        
        # 3. Store in Cache
        if use_cache:
            cache.set(self.name, prompt, response, sys_msg)
            
        return response

    async def execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Any:
        """
        Execute a registered tool with Pydantic validation, full tracing, AND SECTOR ISOLATION.
        """
        from agents.tools_registry import get_tool_registry, ToolValidationError
        
        # --- SECTOR ISOLATION CHECK ---
        # Assuming current mission context available, or we enforce restricted tool sets per agent role.
        # For Phase 4, we verify that "Wealth" sector missions cannot use "Shadow" tools.
        # This implementation assumes tool registry has metadata about restricted sectors.
        
        registry = get_tool_registry()
        tool = registry.get_tool(tool_name)
        
        if not tool:
            error_msg = f"Tool '{tool_name}' not found."
            await self.emit_trace("TOOL_ERROR", error_msg, type="error")
            return f"Error: {error_msg}"

        # Logic: If tool has a 'sector' attribute and it doesn't match mission sector, blocking.
        # For MVP, we can mock this check or check metadata.
        # Let's add a hook for the permission check.
        if not self._check_tool_permissions(tool, tool_name):
             error_msg = f"Security Violation: Tool '{tool_name}' access denied for agent '{self.name}'."
             await self.emit_trace("SECURITY_VIOLATION", error_msg, type="error")
             return f"Error: {error_msg}"

        # Trace Tool Invocation
        await self.emit_trace(
            label="TOOL_CALL",
            content=f"Invoking tool: {tool_name}\nArgs: {json.dumps(tool_args, indent=2)}",
            type="tool_call",
            metadata={"tool": tool_name, "args": tool_args}
        )
            
        try:
            # Validate
            validated_args = tool.validate_args(tool_args)
            
            # Execute
            result = await tool.arun(validated_args)
            
            # Trace Result
            await self.emit_trace(
                label="TOOL_RESULT",
                content=f"Tool {tool_name} returned:\n{json.dumps(result, default=str, indent=2)}",
                type="tool_result",
                metadata={"tool": tool_name, "result": result}
            )
            return result
            
        except ToolValidationError as e:
            await self.emit_trace("TOOL_VALIDATION_ERROR", str(e), type="error")
            return f"Validation Error: {str(e)}"
        except Exception as e:
            logger.exception(f"Tool execution failed: {tool_name}")
            await self.emit_trace("TOOL_EXECUTION_ERROR", str(e), type="error")
            return f"Execution Error: {str(e)}"

    def _check_tool_permissions(self, tool, tool_name) -> bool:
        """
        Verify if the agent is authorized to use the tool based on Sector Isolation rules.
        """
        # Hardcoded Example Rule: "Shadow" tools only for "Shadow" agents or missions.
        # In a real system, this would check 'self.current_mission.sector'.
        
        # If tool name starts with 'shadow_' and agent role is not 'Shadow' -> Block
        if tool_name.startswith("shadow_") and "shadow" not in self.name.lower():
            return False
            
        return True


    async def request_help(self, agent_id: str, sub_task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Delegate a sub-task to another agent in the federation.
        """
        from services.agent_orchestration_service import get_orchestration_service
        orchestrator = get_orchestration_service()
        
        logger.info(f"Agent '{self.name}' requesting help from '{agent_id}' for task: {sub_task}")
        payload = {
            "action": sub_task,
            "data": context or {},
            "requester": self.name
        }
        
        return await orchestrator.invoke_agent(agent_id, payload)

    @abstractmethod
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process an incoming event from the Kafka stream.
        
        Args:
            event: The event payload to process.
            
        Returns:
            Optional response/action to take, or None if no action needed.
        """
        pass
    
    def start(self) -> None:
        """Activate the agent for event processing."""
        self.is_active = True
        logger.info(f"Agent '{self.name}' started")
    
    def stop(self) -> None:
        """Deactivate the agent."""
        self.is_active = False
        logger.info(f"Agent '{self.name}' stopped")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Return the agent's current health status.
        Used by the Watchdog/Heartbeat monitor.
        """
        return {
            'agent': self.name,
            'active': self.is_active,
            'status': 'healthy' if self.is_active else 'inactive'
        }
