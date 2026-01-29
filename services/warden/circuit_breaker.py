"""
Circuit Breaker Logic (The Warden).
Halts trading when thresholds are breached.
"""
from services.risk_manager import RiskManager

class CircuitBreaker:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CircuitBreaker, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if self.initialized:
            return
        self.is_tripped = False
        self.risk_manager = RiskManager()
        self.initialized = True

    def check_circuit(self, balance: float, daily_loss: float) -> bool:
        """
        Check if the circuit breaker should trip.
        Returns True if TRIPPED (Trade Halt).
        """
        if self.is_tripped:
            return True
            
        should_freeze = self.risk_manager.check_portfolio_freeze(balance, daily_loss)
        
        if should_freeze:
            self.trip_circuit("Daily Loss Limit Exceeded")
            return True
            
        return False

    def trip_circuit(self, reason: str):
        """
        Trip the circuit breaker.
        """
        self.is_tripped = True
        print(f"🚨 CIRCUIT BREAKER TRIPPED: {reason}")
        # In real system, this would emit an event to Kafka

    def reset_circuit(self):
        """
        Manual override to reset circuit.
        """
        self.is_tripped = False
        print("✅ Circuit Breaker Reset")
