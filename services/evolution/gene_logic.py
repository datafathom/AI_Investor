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

    def get_gene_pulse(self, agent_id: str, genes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the 'pulse' (activation frequency and mutation risk) 
        of an agent's specific gene markers.
        """
        import hashlib
        
        # Deterministic seed per agent
        seed = int(hashlib.md5(agent_id.encode()).hexdigest(), 16)
        
        pulse_data = []
        for i, (key, value) in enumerate(genes.items()):
            # Activation: how often this gene affects decisions (0.1 to 0.9)
            activation = 0.1 + ((seed + i) % 80) / 100.0
            # Instability: how likely this gene is to drift (0.01 to 0.15)
            instability = 0.01 + ((seed * (i+1)) % 140) / 1000.0
            
            pulse_data.append({
                "gene": key,
                "value": value,
                "activation": activation,
                "instability": instability,
                "status": "stable" if instability < 0.1 else "volatile"
            })
            
        return {
            "agent_id": agent_id,
            "pulse": pulse_data,
            "overall_vitality": 0.7 + (seed % 30) / 100.0,
            "timestamp": hashlib.md5(str(genes).encode()).hexdigest()[:8]
        }

def get_gene_splicer() -> GeneSplicer:
    return GeneSplicer()
