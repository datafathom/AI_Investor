"""
==============================================================================
AI Investor - Web API Gateway
==============================================================================
PURPOSE:
    Main entry point for the Flask/FastAPI backend. Exposes REST endpoints
    for the Mission Control Dashboard and orchestrates agent communication.

ARCHITECTURE:
    - Connects to Kafka for real-time event streaming
    - Interfaces with Postgres (TimescaleDB) for time-series data
    - Interfaces with Neo4j for graph-based dependency mapping
==============================================================================
"""
import os
from flask import Flask, jsonify


def create_app() -> Flask:
    """
    Application factory pattern for Flask app.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Load configuration from environment
    app.config['DEBUG'] = os.getenv('FLASK_ENV', 'development') == 'development'
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint for container orchestration."""
        return jsonify({
            'status': 'healthy',
            'service': 'ai-investor-backend'
        })
    
    @app.route('/api/v1/gap', methods=['GET'])
    def get_gap():
        """
        Returns 'The Gap' - the discrepancy between current Stock and Set Point.
        This is the primary metric for the balancing feedback loop.
        """
        # TODO: Implement actual Stock/SetPoint calculation
        return jsonify({
            'stock': 100000.00,
            'set_point': 100000.00,
            'gap': 0.00,
            'gap_percent': 0.0
        })
    
    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000, debug=True)
