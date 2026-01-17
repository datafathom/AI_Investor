"""
==============================================================================
FILE: services/analysis/genetic_distillery.py
ROLE: Evolutionary Botanist
PURPOSE:
    Evolve trading strategies by optimizing parameters through genetic algorithms.
    
    1. Genome Representation:
       - Parameters like RSI period, thresholds, and risk levels are mapped
         as "genes" in a genome dictionary.
       
    2. Evolution Cycle:
       - Population initialization.
       - Fitness evaluation (via Backtest Engine).
       - Selection (Tournament or Elitism).
       - Crossover (Mixing parents).
       - Mutation (Random parameter tweaks).
       
CONTEXT: 
    Part of Phase 37: The Strategy Distillery.
    "Survival of the most profitable."
==============================================================================
"""

import random
import logging
import copy
from typing import Dict, List, Any, Callable

logger = logging.getLogger(__name__)

class Genome:
    """
    Represents a set of strategy parameters.
    """
    def __init__(self, genes: Dict[str, Any], fitness: float = 0.0):
        self.genes = genes
        self.fitness = fitness
        self.generation = 0
        self.lineage = [] # List of parent IDs

    def __repr__(self):
        return f"Genome(Score: {self.fitness:.4f}, Genes: {self.genes})"

class GeneticDistillery:
    def __init__(self, 
                 gene_bounds: Dict[str, tuple], 
                 population_size: int = 20, 
                 mutation_rate: float = 0.1):
        """
        gene_bounds: e.g., {"rsi_period": (7, 21), "rsi_buy": (20, 40)}
        """
        self.gene_bounds = gene_bounds
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population: List[Genome] = []
        self.current_generation = 0
        self.history = []

    def initialize_population(self):
        """
        Create the first generation of random genomes.
        """
        self.population = []
        for _ in range(self.population_size):
            genes = {}
            for name, bounds in self.gene_bounds.items():
                if isinstance(bounds[0], int):
                    genes[name] = random.randint(bounds[0], bounds[1])
                else:
                    genes[name] = round(random.uniform(bounds[0], bounds[1]), 3)
            self.population.append(Genome(genes))
        
        self.current_generation = 1

    def crossover(self, parent1: Genome, parent2: Genome) -> Genome:
        """
        Uniform crossover: randomly pick genes from either parent.
        """
        child_genes = {}
        for key in self.gene_bounds.keys():
            child_genes[key] = parent1.genes[key] if random.random() > 0.5 else parent2.genes[key]
        
        child = Genome(child_genes)
        child.generation = self.current_generation
        return child

    def mutate(self, genome: Genome) -> Genome:
        """
        Randomly tweak one or more genes within their bounds.
        """
        mutated_genes = copy.deepcopy(genome.genes)
        for key, bounds in self.gene_bounds.items():
            if random.random() < self.mutation_rate:
                if isinstance(bounds[0], int):
                    mutated_genes[key] = random.randint(bounds[0], bounds[1])
                else:
                    mutated_genes[key] = round(random.uniform(bounds[0], bounds[1]), 3)
        
        return Genome(mutated_genes)

    def evolve(self, fitness_fn: Callable[[Dict[str, Any]], float]):
        """
        Run one generation of evolution.
        1. Evaluate fitness
        2. Sort by fitness (elitism)
        3. Breed next generation
        """
        # 1. Evaluate
        for genome in self.population:
            genome.fitness = fitness_fn(genome.genes)

        # 2. Sort (Descending)
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Save history (Top fitness)
        self.history.append({
            "generation": self.current_generation,
            "best_fitness": self.population[0].fitness,
            "avg_fitness": sum(g.fitness for g in self.population) / self.population_size
        })

        # 3. Selection & Breeding
        new_population = [self.population[0]] # Elitism: Keep the best one
        
        # Select parents (Tournament Selection)
        while len(new_population) < self.population_size:
            # Pick 2 parents from top 50%
            potential_parents = self.population[:self.population_size // 2]
            p1, p2 = random.sample(potential_parents, 2)
            
            child = self.crossover(p1, p2)
            child = self.mutate(child)
            new_population.append(child)

        self.population = new_population
        self.current_generation += 1

# Factory constructor
def get_genetic_distillery(gene_bounds: Dict[str, tuple]) -> GeneticDistillery:
    return GeneticDistillery(gene_bounds)
