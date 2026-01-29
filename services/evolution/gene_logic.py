"""
==============================================================================
FILE: services/evolution/gene_logic.py
ROLE: Genetic Architect
PURPOSE:
    Handle the low-level logic for gene manipulation, including crossover,
    mutation, and hybrid agent creation.
    
    Functions:
    - crossover: Combine genes from two parents.
    - mutate: Apply random variations to specific genes.
    - create_hybrid: Register a new agent based on parent genes.

CONTEXT: 
    Part of Sprint 4: Evolution Lab.
==============================================================================
"""

import random
import copy
import uuid
from typing import Dict, Any, List, Optional
from services.analysis.genetic_distillery import Genome

class GeneSplicer:
    """
    Manages the creation of hybrid agents from multiple parents.
    """
    
    @staticmethod
    def crossover(parent1_genes: Dict[str, Any], parent2_genes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs uniform crossover between two gene sets.
        """
        child_genes = {}
        all_keys = set(parent1_genes.keys()) | set(parent2_genes.keys())
        
        for key in all_keys:
            # If gene exists in both, pick randomly. Else take what's available.
            if key in parent1_genes and key in parent2_genes:
                child_genes[key] = parent1_genes[key] if random.random() > 0.5 else parent2_genes[key]
            elif key in parent1_genes:
                child_genes[key] = parent1_genes[key]
            else:
                child_genes[key] = parent2_genes[key]
                
        return child_genes

    @staticmethod
    def mutate(genes: Dict[str, Any], bounds: Dict[str, tuple], mutation_rate: float = 0.1) -> Dict[str, Any]:
        """
        Applies mutations to the gene set within specified boundaries.
        """
        mutated_genes = copy.deepcopy(genes)
        for key, value in mutated_genes.items():
            if key in bounds and random.random() < mutation_rate:
                low, high = bounds[key]
                if isinstance(low, int) and isinstance(high, int):
                    mutated_genes[key] = random.randint(low, high)
                else:
                    mutated_genes[key] = round(random.uniform(low, high), 3)
        return mutated_genes

    def splice_agents(self, 
                     parent1_id: str, 
                     parent2_id: str, 
                     parent1_genes: Dict[str, Any], 
                     parent2_genes: Dict[str, Any],
                     bounds: Dict[str, tuple]) -> Dict[str, Any]:
        """
        Creates a new hybrid "Child" agent.
        """
        # 1. Crossover
        offspring_genes = self.crossover(parent1_genes, parent2_genes)
        
        # 2. Subtle Mutation (default 5% for splicing)
        offspring_genes = self.mutate(offspring_genes, bounds, mutation_rate=0.05)
        
        # 3. Create Child Data
        child_id = f"AGENT-{uuid.uuid4().hex[:8].upper()}"
        
        return {
            "id": child_id,
            "parents": [parent1_id, parent2_id],
            "genes": offspring_genes,
            "status": "born",
            "generation": 0 # Resets for hybrid
        }

def get_gene_splicer() -> GeneSplicer:
    return GeneSplicer()
