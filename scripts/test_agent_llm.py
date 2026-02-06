
import asyncio
import logging
from agents.department_agent import DepartmentAgent
from services.system.model_manager import ModelProvider

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_agent_invoke():
    print("--- Starting Agent LLM Test ---")
    
    # Create an agent (using MOCK provider to avoid API costs/errors during test)
    # In production/dev-full, this would use the configured provider
    agent = DepartmentAgent(
        name="test_analyst", 
        dept_id=99, 
        role="Senior Market Analyst"
    )
    
    # Payload simulating a frontend request
    payload = {
        "action": "analyze_market",
        "data": {"symbol": "AAPL", "context": "Earnings report released"}
    }
    
    print(f"\n[Invoking Agent] {agent.name} ({agent.role})...")
    result = await agent.invoke(payload)
    
    print("\n[Result Received]")
    print(f"Status: {result['status']}")
    print(f"Response: {result['response']}")
    if 'metadata' in result:
        print(f"Metadata: {result['metadata']}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_agent_invoke())
