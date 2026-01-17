"""
==============================================================================
FILE: web/api/evolution_api.py
ROLE: Generative Dispatcher
PURPOSE:
    Expose the Strategy Distillery to the frontend.
    
    Endpoints:
    - POST /api/v1/evolution/start: Initialize and run evolution.
    - GET /api/v1/evolution/status: Get current generation stats.
    
CONTEXT: 
    Part of Phase 37.
==============================================================================
"""

from flask import Blueprint, jsonify, request
from services.analysis.genetic_distillery import get_genetic_distillery

evolution_bp = Blueprint('evolution', __name__, url_prefix='/api/v1/evolution')

# Global instance for demo
distillery = None

@evolution_bp.route('/start', methods=['POST'])
def start_evolution():
    global distillery
    bounds = {
        "rsi_period": (7, 30),
        "rsi_buy": (15, 45),
        "rsi_sell": (55, 85),
        "stop_loss": (0.01, 0.10)
    }
    distillery = get_genetic_distillery(bounds)
    distillery.initialize_population()
    
    # Run 5 generations immediately for demo
    def mock_fitness(genes):
        return (genes["rsi_period"] / 10.0) + (genes["rsi_buy"] / 20.0)
        
    for _ in range(5):
        distillery.evolve(mock_fitness)
        
    return jsonify({
        "status": "success",
        "message": "Evolution started",
        "current_generation": distillery.current_generation,
        "history": distillery.history
    })

@evolution_bp.route('/status', methods=['GET'])
def get_status():
    if not distillery:
        return jsonify({"status": "error", "message": "Evolution not started"}), 400
        
    return jsonify({
        "current_generation": distillery.current_generation,
        "best_performer": {
            "genes": distillery.population[0].genes,
            "fitness": distillery.population[0].fitness
        },
        "history": distillery.history
    })
