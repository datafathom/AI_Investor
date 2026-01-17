"""
==============================================================================
FILE: tests/analysis/test_genetic_logic.py
ROLE: Evolutionary Auditor
PURPOSE:
    Ensure the GeneticDistillery correctly handles population initialization,
    crossover, mutation, and selection.
==============================================================================
"""

import pytest
from services.analysis.genetic_distillery import GeneticDistillery, Genome

class TestGeneticLogic:
    
    @pytest.fixture
    def distillery(self):
        gene_bounds = {
            "rsi_period": (7, 21),
            "rsi_buy": (20, 40),
            "stop_loss": (0.01, 0.05)
        }
        return GeneticDistillery(gene_bounds, population_size=10, mutation_rate=1.0) # High mutation for test

    def test_initialization(self, distillery):
        distillery.initialize_population()
        assert len(distillery.population) == 10
        assert distillery.current_generation == 1
        
        genome = distillery.population[0]
        assert 7 <= genome.genes["rsi_period"] <= 21
        assert 0.01 <= genome.genes["stop_loss"] <= 0.05

    def test_crossover(self, distillery):
        # Create 2 distinct parents
        p1 = Genome({"rsi_period": 10, "rsi_buy": 25, "stop_loss": 0.02})
        p2 = Genome({"rsi_period": 20, "rsi_buy": 35, "stop_loss": 0.04})
        
        child = distillery.crossover(p1, p2)
        
        # Child genes must come from one of the parents
        for key in ["rsi_period", "rsi_buy", "stop_loss"]:
            assert child.genes[key] in [p1.genes[key], p2.genes[key]]

    def test_mutation(self, distillery):
        # Create a genome
        genome = Genome({"rsi_period": 10, "rsi_buy": 25, "stop_loss": 0.02})
        distillery.mutation_rate = 1.0 # Force mutation
        
        mutated = distillery.mutate(genome)
        
        # At high mutation rate, at least one gene should differ (very likely)
        # Note: Since it picks new values from bounds, it might pick the same one, 
        # but for test we assume it changes.
        diff = any(mutated.genes[k] != genome.genes[k] for k in genome.genes)
        assert diff is True

    def test_evolution_step(self, distillery):
        distillery.initialize_population()
        initial_best = distillery.population[0]
        
        # Dummy fitness function (Higher rsi_period is better)
        def fitness_fn(genes):
            return float(genes["rsi_period"])
            
        distillery.evolve(fitness_fn)
        
        assert distillery.current_generation == 2
        assert len(distillery.history) == 1
        assert distillery.history[0]["best_fitness"] >= 7
