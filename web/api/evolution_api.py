"""
==============================================================================
FILE: web/api/evolution_api.py
ROLE: Generative Dispatcher
PURPOSE:
    Expose the Strategy Distillery to the frontend.
    
    Endpoints:
    - POST /api/v1/evolution/start: Initialize and run evolution.
    - GET /api/v1/evolution/status: Get current generation stats.
    - POST /api/v1/evolution/splice: Combine two agents into a hybrid.
    - POST /api/v1/evolution/playback: Re-run historical data for a genome.
    
CONTEXT: 
    Part of Phase 37.
==============================================================================
"""

from flask import Blueprint, jsonify, request
from services.analysis.genetic_distillery import get_genetic_distillery
from services.evolution.gene_logic import get_gene_splicer
from services.evolution.playback_service import get_playback_service
import logging

logger = logging.getLogger(__name__)

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

@evolution_bp.route('/splice', methods=['POST'])
def splice_agents():
    """
    Splicing two agents into a new hybrid.
    """
    try:
        data = request.json
        p1_id = data.get('parent1_id')
        p2_id = data.get('parent2_id')
        p1_genes = data.get('parent1_genes')
        p2_genes = data.get('parent2_genes')
        bounds = data.get('bounds', {
            "rsi_period": (7, 30),
            "rsi_buy": (15, 45),
            "rsi_sell": (55, 85),
            "stop_loss": (0.01, 0.10)
        })

        if not all([p1_id, p2_id, p1_genes, p2_genes]):
            return jsonify({"status": "error", "message": "Missing parent data"}), 400

        splicer = get_gene_splicer()
        child = splicer.splice_agents(p1_id, p2_id, p1_genes, p2_genes, bounds)

        return jsonify({
            "status": "success",
            "data": child
        })
    except Exception as e:
        logger.exception("Splicing failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@evolution_bp.route('/playback', methods=['POST'])
def genomic_playback():
    """
    Re-run historical data for a given genome.
    """
    try:
        data = request.json
        genes = data.get('genes')
        price_data = data.get('price_data') # In production, this might be fetched from DB

        if not genes or not price_data:
            return jsonify({"status": "error", "message": "Missing genes or price_data"}), 400

        service = get_playback_service()
        result = service.run_playback(genes, price_data)

        return jsonify({
            "status": "success",
            "data": {
                "final_value": result.final_value,
                "total_return": result.total_return,
                "trades": result.trades_executed,
                "history": result.history
            }
        })
    except Exception as e:
        logger.exception("Playback failed")
        return jsonify({"status": "error", "message": str(e)}), 500


@evolution_bp.route('/pulse/<agent_id>', methods=['POST'])
def get_gene_pulse(agent_id: str):
    """
    Sprint 6: Micro-view of gene activation and instability.
    """
    try:
        data = request.json
        genes = data.get('genes')
        if not genes:
            return jsonify({"status": "error", "message": "Missing genes"}), 400
            
        splicer = get_gene_splicer()
        pulse = splicer.get_gene_pulse(agent_id, genes)
        return jsonify({"status": "success", "data": pulse})
    except Exception as e:
        logger.exception("Pulse fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

