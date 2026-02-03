import pytest
import asyncio
import time
from agents.base_agent import BaseAgent
from services.system.model_manager import ModelProvider, get_model_manager

class ResearchAgent(BaseAgent):
    def process_event(self, event):
        return None

class SummaryAgent(BaseAgent):
    def process_event(self, event):
        return None

@pytest.mark.asyncio
async def test_agent_model_routing():
    # 1. Setup agents with different model preferences
    researcher = ResearchAgent("Researcher", provider=ModelProvider.PERPLEXITY)
    summarizer = SummaryAgent("Summarizer", provider=ModelProvider.GEMINI)
    
    # 2. Verify model assignment
    assert researcher.model_config.provider == ModelProvider.PERPLEXITY
    assert researcher.model_config.model_id == "llama-3-sonar-large-32k-online"
    
    assert summarizer.model_config.provider == ModelProvider.GEMINI
    assert summarizer.model_config.model_id == "gemini-1.5-flash"
    
    # 3. Test completion routing (using mocked responses from ModelManager)
    res_resp = await researcher.get_completion("Latest NVDA news")
    sum_resp = await summarizer.get_completion("Summarize NVDA news")
    
    assert "Perplexity" in res_resp
    assert "Gemini" in sum_resp

@pytest.mark.asyncio
async def test_llm_governance_throttling():
    manager = get_model_manager()
    governor = manager.governor
    # Set a tiny limit for OpenAI to trigger throttling
    governor.LIMITS["OPENAI"] = {"per_minute": 1, "per_day": 10}
    
    agent = ResearchAgent("ProAgent", provider=ModelProvider.OPENAI)
    
    # Fill slot
    await agent.get_completion("Task 1")
    
    # Second call should throttle
    start = time.time()
    wait_task = asyncio.create_task(agent.get_completion("Task 2"))
    
    # Wait a bit to ensure it's stuck
    await asyncio.sleep(1)
    assert not wait_task.done()
    
    # Simulate time passing by clearing minute stats
    stats = governor._get_stats("OPENAI")
    stats["minute"] = [] # Clear slots
    
    await asyncio.wait_for(wait_task, timeout=5.0)
    end = time.time()
    
    assert end - start >= 1.0 # Waited at least 1s
    assert wait_task.done()
