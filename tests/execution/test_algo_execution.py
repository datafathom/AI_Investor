
import pytest
from services.execution.algo_execution import AlgoEngine

class TestAlgoEngine:
    
    def test_vwap_schedule(self):
        engine = AlgoEngine()
        
        # Total: 1000
        # Profile: [0.1, 0.9] -> Expect [100, 900]
        profile = [0.1, 0.9]
        schedule = engine.generate_vwap_schedule(1000, profile)
        
        assert len(schedule) == 2
        assert schedule[0] == 100
        assert schedule[1] == 900
        assert sum(schedule) == 1000
        
    def test_twap_schedule(self):
        engine = AlgoEngine()
        
        # Total: 100
        # Batches: 3
        # 100 / 3 = 33 r 1
        # Expect [34, 33, 33]
        schedule = engine.generate_twap_schedule(100, 3)
        
        assert len(schedule) == 3
        assert sum(schedule) == 100
        assert schedule[0] == 34
        assert schedule[1] == 33
        assert schedule[2] == 33
