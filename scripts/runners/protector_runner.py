"""
Runner for Protector commands.
"""
from agents.protector_agent import ProtectorAgent

def run_test_protector(amount: str, daily_loss: str = "0.0"):
    """
    Simulate an order validation request.
    """
    agent = ProtectorAgent()
    
    try:
        amt = float(amount)
        loss = float(daily_loss)
        
        print(f"👮 Warden: Validating Order Risk: ${amt}, Daily Loss: ${loss}")
        
        event = {
            "type": "VALIDATE_ORDER",
            "amount": amt,
            "balance": 100000.0,
            "daily_loss": loss
        }
        
        result = agent.process_event(event)
        
        if result["action"] == "APPROVE":
            print(f"✅ APPROVED: {result['reason']}")
        else:
            print(f"❌ REJECTED: {result['reason']}")
            
    except Exception as e:
        print(f"Error: {e}")
