# Phase 3: AI Agent Integration

> **Duration**: 3 Weeks  
> **Status**: [ ] Not Started  
> **Dependencies**: Phase 1, Phase 2  
> **Owner**: TBD  

---

## Phase Overview

Implement the 84+ AI agent system with invocation capabilities, status monitoring, performance tracking, and configuration management. Each department has 6 specialized agents that can be invoked on-demand.

---

## Deliverables Checklist

### 3.1 Agent Definition Registry
- [ ] JSON schema complete (84+ agents)
- [ ] Validation script passes
- [ ] CLI commands implemented

### 3.2 Agent Service Layer
- [ ] Singleton service implemented
- [ ] Async invocation working
- [ ] Circuit breaker active
- [ ] Timeout handling verified

### 3.3 Agent Panel Component
- [ ] UI component complete
- [ ] Real-time status updates
- [ ] Invoke modal functional

### 3.4 Agent API Endpoints
- [ ] All endpoints implemented
- [ ] Rate limiting active
- [ ] Integration tests pass

---

## Deliverable 3.1: Agent Definition Registry

### File Location
`config/agent_definitions.json`

### Schema Structure

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "departments": {
      "type": "object",
      "patternProperties": {
        "^[1-9]|1[0-8]$": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "agents": {
              "type": "array",
              "items": {
                "type": "object",
                "required": ["id", "name", "role", "inputs", "outputs"],
                "properties": {
                  "id": { "type": "string", "pattern": "^[a-z_]+$" },
                  "name": { "type": "string" },
                  "role": { "type": "string" },
                  "inputs": { "type": "array", "items": { "type": "string" } },
                  "processing": { "type": "string" },
                  "outputs": { "type": "array", "items": { "type": "string" } },
                  "llm_model": { "type": "string", "default": "gemini-pro" },
                  "timeout_seconds": { "type": "integer", "default": 60 },
                  "requires_confirmation": { "type": "boolean", "default": false }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Complete Agent Roster (Sample Entries)

```json
{
  "departments": {
    "1": {
      "name": "Orchestrator",
      "agents": [
        {
          "id": "synthesizer",
          "name": "The Synthesizer",
          "role": "Chief of Staff",
          "inputs": ["kafka_streams", "net_worth_delta", "system_health"],
          "processing": "Aggregates multi-role data into unified snapshot; detects cross-department contradictions",
          "outputs": ["morning_briefing", "cross_role_notifications"],
          "llm_model": "gemini-pro",
          "timeout_seconds": 120
        },
        {
          "id": "command_interpreter",
          "name": "The Command Interpreter",
          "role": "NLP Interface",
          "inputs": ["natural_language_text", "voice_command"],
          "processing": "Parses intent; maps to API calls; confirms action",
          "outputs": ["api_calls", "action_confirmation"],
          "llm_model": "gemini-pro",
          "timeout_seconds": 30
        },
        {
          "id": "traffic_controller",
          "name": "The Traffic Controller",
          "role": "Kafka Architect",
          "inputs": ["kafka_topic_metrics", "consumer_lag"],
          "processing": "Monitors message flow; adjusts partitioning; alerts on bottlenecks",
          "outputs": ["routing_decisions", "performance_alerts"],
          "llm_model": null,
          "timeout_seconds": 10
        },
        {
          "id": "layout_morphologist",
          "name": "The Layout Morphologist",
          "role": "UX Agent",
          "inputs": ["user_focus", "active_widgets", "screen_resolution"],
          "processing": "Adapts UI layout based on current user focus and data importance",
          "outputs": ["layout_config", "widget_priority"],
          "llm_model": "gemini-pro",
          "timeout_seconds": 15
        },
        {
          "id": "red_team_sentry",
          "name": "The Red-Team Sentry",
          "role": "Internal Auditor",
          "inputs": ["agent_outputs", "api_responses"],
          "processing": "Cross-validates agent claims; flags hallucinations or inconsistencies",
          "outputs": ["validation_report", "hallucination_flags"],
          "llm_model": "gemini-pro",
          "timeout_seconds": 60
        },
        {
          "id": "context_weaver",
          "name": "The Context Weaver",
          "role": "State Manager",
          "inputs": ["user_session", "conversation_history", "active_context"],
          "processing": "Maintains coherent context across agent interactions",
          "outputs": ["context_object", "memory_updates"],
          "llm_model": "gemini-pro",
          "timeout_seconds": 30
        }
      ]
    },
    "5": {
      "name": "Trader",
      "agents": [
        {
          "id": "sniper",
          "name": "The Sniper",
          "role": "Execution Agent",
          "inputs": ["order_params", "market_conditions", "liquidity_data"],
          "processing": "Finds optimal execution price; splits orders to minimize impact",
          "outputs": ["fill_report", "execution_metrics"],
          "llm_model": null,
          "timeout_seconds": 5,
          "requires_confirmation": true
        },
        {
          "id": "exit_manager",
          "name": "The Exit Manager",
          "role": "Stop-Loss Guardian",
          "inputs": ["open_positions", "price_feed", "volatility"],
          "processing": "Manages trailing stops; triggers exits on risk thresholds",
          "outputs": ["exit_orders", "position_updates"],
          "llm_model": null,
          "timeout_seconds": 3
        },
        {
          "id": "arbitrageur",
          "name": "The Arbitrageur",
          "role": "Cross-Market Scanner",
          "inputs": ["multi_exchange_prices", "fee_structures"],
          "processing": "Identifies arbitrage opportunities across exchanges",
          "outputs": ["arb_opportunities", "execution_plan"],
          "llm_model": null,
          "timeout_seconds": 10
        },
        {
          "id": "liquidity_scout",
          "name": "The Liquidity Scout",
          "role": "Market Depth Analyst",
          "inputs": ["order_book_snapshots", "historical_volume"],
          "processing": "Assesses market depth; estimates slippage for order sizes",
          "outputs": ["liquidity_report", "slippage_estimate"],
          "llm_model": null,
          "timeout_seconds": 5
        },
        {
          "id": "position_sizer",
          "name": "The Position Sizer",
          "role": "Risk Calculator",
          "inputs": ["portfolio_state", "risk_params", "opportunity_score"],
          "processing": "Calculates optimal position size based on Kelly criterion and risk limits",
          "outputs": ["position_recommendation", "risk_metrics"],
          "llm_model": null,
          "timeout_seconds": 5
        },
        {
          "id": "flash_crash_circuit_breaker",
          "name": "Flash-Crash Circuit Breaker",
          "role": "Emergency Guardian",
          "inputs": ["price_velocity", "volume_spike", "correlation_break"],
          "processing": "Detects flash crash conditions; halts all execution",
          "outputs": ["halt_signal", "incident_report"],
          "llm_model": null,
          "timeout_seconds": 1,
          "requires_confirmation": false
        }
      ]
    }
  }
}
```

### CLI Commands

```bash
# List all agents
python cli.py agents list

# List agents for specific department
python cli.py agents list --dept 5

# Show agent details
python cli.py agents show sniper

# Invoke agent (dry-run)
python cli.py agents invoke sniper --params '{"ticker":"TSLA"}' --dry-run

# Validate agent definitions
python cli.py validate-agent-definitions
```

---

## Deliverable 3.2: Agent Service Layer

### File Location
`services/agent_orchestration_service.py`

### Implementation

```python
"""
Agent Orchestration Service

Manages the lifecycle, invocation, and monitoring of all 84+ department agents.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum

from services.kafka_service import KafkaService
from services.llm_service import LLMService
from utils.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"
    TIMEOUT = "timeout"
    CIRCUIT_OPEN = "circuit_open"


@dataclass
class AgentExecutionResult:
    agent_id: str
    department_id: int
    status: AgentStatus
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: int = 0
    tokens_used: int = 0


class AgentOrchestrationService:
    """
    Singleton service for agent orchestration.
    
    Features:
    - Async agent invocation
    - Circuit breaker for LLM calls
    - Timeout handling
    - Kafka event publishing
    - Performance tracking
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._agent_definitions = self._load_agent_definitions()
        self._agent_status: Dict[str, AgentStatus] = {}
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._kafka = KafkaService()
        self._llm = LLMService()
        
        logger.info("AgentOrchestrationService initialized")
    
    def _load_agent_definitions(self) -> Dict:
        """Load agent definitions from config."""
        try:
            with open("config/agent_definitions.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("agent_definitions.json not found")
            return {"departments": {}}
    
    def _get_circuit_breaker(self, agent_id: str) -> CircuitBreaker:
        """Get or create circuit breaker for agent."""
        if agent_id not in self._circuit_breakers:
            self._circuit_breakers[agent_id] = CircuitBreaker(
                failure_threshold=5,
                recovery_timeout=30,
                name=f"agent_{agent_id}"
            )
        return self._circuit_breakers[agent_id]
    
    def get_agent_definition(
        self, 
        department_id: int, 
        agent_id: str
    ) -> Optional[Dict]:
        """Get agent definition from registry."""
        dept = self._agent_definitions.get("departments", {}).get(str(department_id))
        if not dept:
            return None
        
        for agent in dept.get("agents", []):
            if agent["id"] == agent_id:
                return agent
        return None
    
    async def invoke_agent(
        self,
        department_id: int,
        agent_id: str,
        parameters: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> AgentExecutionResult:
        """
        Invoke a specific agent with parameters.
        
        Args:
            department_id: Department ID (1-18)
            agent_id: Agent slug (e.g., 'sniper')
            parameters: Dict of input parameters
            user_id: Optional user ID for audit
            
        Returns:
            AgentExecutionResult with status and output
        """
        start_time = datetime.now(timezone.utc)
        
        # Get agent definition
        agent_def = self.get_agent_definition(department_id, agent_id)
        if not agent_def:
            return AgentExecutionResult(
                agent_id=agent_id,
                department_id=department_id,
                status=AgentStatus.ERROR,
                error=f"Agent {agent_id} not found in department {department_id}"
            )
        
        # Check circuit breaker
        circuit_breaker = self._get_circuit_breaker(agent_id)
        if not circuit_breaker.allow_request():
            logger.warning(f"Circuit open for agent {agent_id}")
            return AgentExecutionResult(
                agent_id=agent_id,
                department_id=department_id,
                status=AgentStatus.CIRCUIT_OPEN,
                error="Circuit breaker open - too many recent failures"
            )
        
        # Update status to processing
        self._agent_status[agent_id] = AgentStatus.PROCESSING
        await self._publish_status_event(department_id, agent_id, AgentStatus.PROCESSING)
        
        try:
            # Execute with timeout
            timeout = agent_def.get("timeout_seconds", 60)
            output = await asyncio.wait_for(
                self._execute_agent(agent_def, parameters),
                timeout=timeout
            )
            
            execution_time = int((datetime.now(timezone.utc) - start_time).total_seconds() * 1000)
            
            # Record success
            circuit_breaker.record_success()
            self._agent_status[agent_id] = AgentStatus.COMPLETE
            
            result = AgentExecutionResult(
                agent_id=agent_id,
                department_id=department_id,
                status=AgentStatus.COMPLETE,
                output=output,
                execution_time_ms=execution_time,
                tokens_used=output.get("_tokens_used", 0)
            )
            
            await self._publish_status_event(department_id, agent_id, AgentStatus.COMPLETE)
            await self._log_invocation(result, user_id)
            
            return result
            
        except asyncio.TimeoutError:
            circuit_breaker.record_failure()
            self._agent_status[agent_id] = AgentStatus.TIMEOUT
            
            logger.error(f"Agent {agent_id} timed out after {timeout}s")
            
            return AgentExecutionResult(
                agent_id=agent_id,
                department_id=department_id,
                status=AgentStatus.TIMEOUT,
                error=f"Agent timed out after {timeout} seconds"
            )
            
        except Exception as e:
            circuit_breaker.record_failure()
            self._agent_status[agent_id] = AgentStatus.ERROR
            
            logger.exception(f"Agent {agent_id} failed: {e}")
            
            return AgentExecutionResult(
                agent_id=agent_id,
                department_id=department_id,
                status=AgentStatus.ERROR,
                error=str(e)
            )
    
    async def _execute_agent(
        self, 
        agent_def: Dict, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute agent logic based on definition."""
        llm_model = agent_def.get("llm_model")
        
        if llm_model:
            # LLM-powered agent
            prompt = self._build_agent_prompt(agent_def, parameters)
            response = await self._llm.generate(
                model=llm_model,
                prompt=prompt,
                max_tokens=2048
            )
            return {
                "response": response.text,
                "_tokens_used": response.usage.total_tokens
            }
        else:
            # Rule-based agent - delegate to specific handler
            handler = self._get_agent_handler(agent_def["id"])
            return await handler(parameters)
    
    def _build_agent_prompt(
        self, 
        agent_def: Dict, 
        parameters: Dict[str, Any]
    ) -> str:
        """Build LLM prompt from agent definition and parameters."""
        return f"""You are {agent_def['name']}, a specialized AI agent.
        
Role: {agent_def['role']}
Processing: {agent_def.get('processing', 'Perform your specialized task')}

Expected inputs: {', '.join(agent_def.get('inputs', []))}
Expected outputs: {', '.join(agent_def.get('outputs', []))}

Current parameters:
{json.dumps(parameters, indent=2)}

Perform your task and return structured JSON output."""
    
    def _get_agent_handler(self, agent_id: str):
        """Get handler function for rule-based agents."""
        handlers = {
            "sniper": self._handle_sniper,
            "exit_manager": self._handle_exit_manager,
            # ... other handlers
        }
        return handlers.get(agent_id, self._handle_generic)
    
    async def _handle_sniper(self, params: Dict) -> Dict:
        """Handler for Sniper agent."""
        # Implementation for order execution
        return {"status": "executed", "fill_price": params.get("limit_price")}
    
    async def _handle_exit_manager(self, params: Dict) -> Dict:
        """Handler for Exit Manager agent."""
        return {"stops_updated": True}
    
    async def _handle_generic(self, params: Dict) -> Dict:
        """Generic handler for unimplemented agents."""
        return {"status": "ok", "message": "Agent executed (stub)"}
    
    async def get_agent_status(
        self, 
        department_id: int, 
        agent_id: str
    ) -> AgentStatus:
        """Get current status of an agent."""
        return self._agent_status.get(agent_id, AgentStatus.IDLE)
    
    async def broadcast_to_department(
        self, 
        department_id: int, 
        message: Dict
    ) -> None:
        """Send message to all agents in a department via Kafka."""
        topic = f"dept.{department_id}.events"
        await self._kafka.produce(topic, message)
    
    async def _publish_status_event(
        self, 
        department_id: int, 
        agent_id: str, 
        status: AgentStatus
    ) -> None:
        """Publish agent status update to Kafka."""
        await self._kafka.produce(
            f"dept.{department_id}.agents",
            {
                "agent_id": agent_id,
                "status": status.value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
    
    async def _log_invocation(
        self, 
        result: AgentExecutionResult, 
        user_id: Optional[str]
    ) -> None:
        """Log agent invocation to audit table."""
        # Implementation for audit logging
        pass
```

### Unit Tests

`tests/services/test_agent_orchestration.py`

```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from services.agent_orchestration_service import (
    AgentOrchestrationService,
    AgentStatus,
    AgentExecutionResult
)


@pytest.fixture
def agent_service():
    # Reset singleton for testing
    AgentOrchestrationService._instance = None
    return AgentOrchestrationService()


class TestAgentOrchestrationService:
    
    def test_singleton_pattern(self, agent_service):
        service2 = AgentOrchestrationService()
        assert agent_service is service2
    
    def test_get_agent_definition_valid(self, agent_service):
        agent = agent_service.get_agent_definition(5, "sniper")
        assert agent is not None
        assert agent["id"] == "sniper"
    
    def test_get_agent_definition_invalid_dept(self, agent_service):
        agent = agent_service.get_agent_definition(99, "sniper")
        assert agent is None
    
    def test_get_agent_definition_invalid_agent(self, agent_service):
        agent = agent_service.get_agent_definition(5, "nonexistent")
        assert agent is None
    
    @pytest.mark.asyncio
    async def test_invoke_agent_success(self, agent_service):
        with patch.object(agent_service, '_execute_agent', new_callable=AsyncMock) as mock:
            mock.return_value = {"status": "ok"}
            
            result = await agent_service.invoke_agent(5, "sniper", {"ticker": "TSLA"})
            
            assert result.status == AgentStatus.COMPLETE
            assert result.output == {"status": "ok"}
    
    @pytest.mark.asyncio
    async def test_invoke_agent_timeout(self, agent_service):
        async def slow_execution(*args):
            import asyncio
            await asyncio.sleep(100)
        
        with patch.object(agent_service, '_execute_agent', side_effect=slow_execution):
            with patch.object(agent_service, 'get_agent_definition') as mock_def:
                mock_def.return_value = {"id": "test", "timeout_seconds": 0.1}
                
                result = await agent_service.invoke_agent(5, "test", {})
                
                assert result.status == AgentStatus.TIMEOUT
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_opens(self, agent_service):
        # Simulate 5 failures
        with patch.object(agent_service, '_execute_agent', side_effect=Exception("fail")):
            for _ in range(5):
                await agent_service.invoke_agent(5, "sniper", {})
        
        # Next call should be blocked
        result = await agent_service.invoke_agent(5, "sniper", {})
        assert result.status == AgentStatus.CIRCUIT_OPEN
```

---

## Deliverable 3.3: Agent Panel Component

### File Location
`frontend/src/components/Departments/AgentPanel.jsx`

### Implementation

```jsx
import React, { useState, useCallback } from 'react';
import { useDepartmentStore } from '@/stores/departmentStore';
import { DEPT_REGISTRY } from '@/config/departmentRegistry';
import { agentService } from '@/services/agentService';
import { Icon } from '@/components/UI/Icon';
import { Modal } from '@/components/UI/Modal';
import styles from './AgentPanel.module.css';

const STATUS_COLORS = {
  idle: '#6b7280',
  processing: '#f59e0b',
  complete: '#22c55e',
  error: '#ef4444',
  timeout: '#dc2626'
};

export const AgentPanel = ({ departmentId, agents }) => {
  const [invokeModal, setInvokeModal] = useState(null);
  const [invoking, setInvoking] = useState(null);
  const config = DEPT_REGISTRY[departmentId];
  
  const handleInvoke = useCallback(async (agentId, params) => {
    setInvoking(agentId);
    try {
      const result = await agentService.invokeAgent(departmentId, agentId, params);
      setInvokeModal(null);
      // Show result toast
    } catch (error) {
      console.error('Agent invocation failed:', error);
    } finally {
      setInvoking(null);
    }
  }, [departmentId]);
  
  return (
    <div className={styles.panel}>
      <h3 className={styles.title}>
        <Icon name="users" />
        Agents ({agents?.length || config.agents.length})
      </h3>
      
      <div className={styles.agentList}>
        {(config.agents || []).map((agentId, index) => {
          const agentData = agents?.find(a => a.id === agentId) || {};
          const status = agentData.status || 'idle';
          
          return (
            <div key={agentId} className={styles.agentCard}>
              <div className={styles.agentHeader}>
                <span 
                  className={styles.statusDot}
                  style={{ background: STATUS_COLORS[status] }}
                />
                <span className={styles.agentName}>
                  Agent {index + 1}
                </span>
                <span className={styles.agentId}>{agentId}</span>
              </div>
              
              <div className={styles.agentMeta}>
                {agentData.lastInvocation && (
                  <span className={styles.lastRun}>
                    Last: {new Date(agentData.lastInvocation).toLocaleTimeString()}
                  </span>
                )}
                <span className={styles.score}>
                  Score: {agentData.performanceScore?.toFixed(1) || '50.0'}%
                </span>
              </div>
              
              <button
                className={styles.invokeBtn}
                onClick={() => setInvokeModal(agentId)}
                disabled={status === 'processing' || invoking === agentId}
              >
                {invoking === agentId ? (
                  <><Icon name="loader" spin /> Running...</>
                ) : (
                  <><Icon name="play" /> Invoke</>
                )}
              </button>
            </div>
          );
        })}
      </div>
      
      {/* Invoke Modal */}
      {invokeModal && (
        <AgentInvokeModal
          agentId={invokeModal}
          departmentId={departmentId}
          onInvoke={handleInvoke}
          onClose={() => setInvokeModal(null)}
        />
      )}
    </div>
  );
};

const AgentInvokeModal = ({ agentId, departmentId, onInvoke, onClose }) => {
  const [params, setParams] = useState('{}');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    try {
      const parsed = JSON.parse(params);
      onInvoke(agentId, parsed);
    } catch (error) {
      alert('Invalid JSON parameters');
    }
  };
  
  return (
    <Modal title={`Invoke ${agentId}`} onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <label>Parameters (JSON):</label>
        <textarea
          value={params}
          onChange={(e) => setParams(e.target.value)}
          rows={6}
          className={styles.paramInput}
        />
        <div className={styles.modalActions}>
          <button type="button" onClick={onClose}>Cancel</button>
          <button type="submit" className={styles.submitBtn}>
            <Icon name="zap" /> Execute
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default AgentPanel;
```

---

## Deliverable 3.4: Agent API Endpoints

### File Location
`web/api/agents_api.py`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/agents` | List all agents |
| GET | `/api/v1/agents/{id}` | Agent details |
| POST | `/api/v1/agents/{id}/invoke` | Invoke agent |
| GET | `/api/v1/agents/{id}/status` | Current status |
| GET | `/api/v1/agents/{id}/history` | Invocation history |

### E2E Definition of Done

1. **List agents**: `GET /api/v1/agents` returns 84+ agents
2. **Invoke agent**: `POST /api/v1/agents/sniper/invoke` returns job ID
3. **Status check**: `GET /api/v1/agents/sniper/status` shows current state
4. **Rate limiting**: 11th request within 1 minute returns 429

---

## Phase Sign-Off Checklist

- [ ] All 84+ agents defined in JSON
- [ ] Agent service handles invocation/timeout/circuit breaker
- [ ] Agent panel UI functional
- [ ] API endpoints tested
- [ ] No console errors
