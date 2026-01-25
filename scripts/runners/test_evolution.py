"""
==============================================================================
FILE: scripts/runners/test_evolution.py
ROLE: Evolutionary Stress-Tester
PURPOSE:
    Run a multi-generation strategy distillation in the terminal
    to verify convergence and genetic logic.
==============================================================================
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from services.analysis.genetic_distillery import get_genetic_distillery, Genome

def run_simulation():
    print("🧬 Starting Genetic Strategy Distillery Simulation...")
    
    bounds = {
        "rsi_period": (7, 30),
        "rsi_buy": (15, 45),
        "stop_loss": (0.01, 0.10)
    }
    
    distillery = get_genetic_distillery(bounds)
    distillery.initialize_population()
    
    # Mock fitness: Proportional to rsi_period and inversely to stop_loss
    def fitness_fn(genes):
        return (genes["rsi_period"] / 10.0) + (1.0 / genes["stop_loss"] / 100.0)
        
    print(f"{'Gen':<5} | {'Best Fitness':<15} | {'Avg Fitness':<15}")
    print("-" * 40)
    
    for i in range(20):
        distillery.evolve(fitness_fn)
        best = distillery.history[-1]["best_fitness"]
        avg = distillery.history[-1]["avg_fitness"]
        print(f"{i+1:<5} | {best:<15.4f} | {avg:<15.4f}")
        
    print("\nOK Evolution Complete!")
    print(f"Final Alpha Genome: {distillery.population[0].genes}")
    print(f"Final Fitness Score: {distillery.population[0].fitness:.4f}")

if __name__ == "__main__":
    run_simulation()
