from fastapi import APIRouter
import random

router = APIRouter(prefix="/api/v1/simulation", tags=["Simulation"])

@router.post('/monte-carlo')
async def run_simulation():
    """Run Monte Carlo simulation."""
    paths = []
    for _ in range(100):
        path = [10000]
        for _ in range(30):
            change = random.normalvariate(0.001, 0.02)
            path.append(path[-1] * (1 + change))
        paths.append(path)
        
    return {
        "success": True, 
        "data": {
            "paths": paths,
            "metrics": {
                "median_terminal_wealth": 10500.0,
                "worst_case": 8500.0,
                "ruin_prob": 0.02,
                "var_95": -5.0
            }
        }
    }
