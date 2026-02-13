import logging
import random
import numpy as np
from typing import List, Dict

logger = logging.getLogger(__name__)

class MonteCarloSimulator:
    async def run_simulation(self, params: Dict) -> Dict:
        """
        params: { "start_price": 100, "mu": 0.0005, "sigma": 0.02, "days": 252, "paths": 1000 }
        """
        s0 = params.get('start_price', 100)
        mu = params.get('mu', 0.0005) # Daily return
        sigma = params.get('sigma', 0.02) # Daily vol
        days = params.get('days', 252)
        n_paths = params.get('paths', 500) # Limit for performace
        
        paths = []
        final_values = []
        
        for _ in range(n_paths):
            path = [s0]
            price = s0
            for _ in range(days):
                # GBM: S_t = S_{t-1} * exp((mu - 0.5*sigma^2)*dt + sigma*W_t)
                shock = np.random.normal(0, 1)
                drift = (mu - 0.5 * sigma**2)
                diffusion = sigma * shock
                price = price * np.exp(drift + diffusion)
                path.append(price)
            
            # Downsample for frontend (e.g., every 5th point) to reduce payload
            paths.append([round(p, 2) for p in path[::5]]) 
            final_values.append(price)
            
        final_values.sort()
        
        return {
            "paths": paths[:50], # Only return first 50 paths for visualization to avoid browser lag
            "percentiles": {
                "p5": round(final_values[int(n_paths*0.05)], 2),
                "p25": round(final_values[int(n_paths*0.25)], 2),
                "p50": round(final_values[int(n_paths*0.50)], 2),
                "p75": round(final_values[int(n_paths*0.75)], 2),
                "p95": round(final_values[int(n_paths*0.95)], 2)
            }
        }
