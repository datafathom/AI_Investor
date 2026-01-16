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
from flask import Flask, jsonify, request

from services.analysis import get_fear_greed_service
from web.api.dashboard_api import dashboard_bp
from web.api.communication_api import communication_bp


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
    
    @app.route('/api/v1/market/fear-greed', methods=['GET'])
    def get_fear_greed_index():
        """
        Phase 12: Fear & Greed Composite Index.
        
        Query params:
            symbols (optional): Comma-separated list of tickers (default: SPY,QQQ,AAPL,TSLA,NVDA)
            mock (optional): Use mock data (default: true for now)
        
        Returns:
            {
                "score": 45.5,
                "label": "FEAR",
                "timestamp": "...",
                "components": {...},
                "signal": "BUY" | "HOLD" | "SELL",
                "recommendation": "..."
            }
        """
        symbols_param = request.args.get('symbols', 'SPY,QQQ,AAPL,TSLA,NVDA')
        symbols = [s.strip().upper() for s in symbols_param.split(',')]
        mock = request.args.get('mock', 'true').lower() == 'true'
        
        service = get_fear_greed_service(mock=mock)
        result = service.get_fear_greed_index(symbols=symbols)
        
        return jsonify(result)

    @app.route('/api/v1/market/predict', methods=['GET'])
    def get_market_prediction():
        """
        Get directional prediction for a symbol.
        Params:
            symbol: string (default SPY)
        """
        symbol = request.args.get('symbol', 'SPY').upper()
        # In a real scenario, we would fetch data for 'symbol' here.
        # For now, we utilize the mock/synthetic data generation within the endpoint or service wrapper
        # to demonstrate feasibility, as fetching live OHLCV might require the ingestion pipeline (Phase 6).
        
        from services.analysis.prediction_service import get_prediction_service
        import pandas as pd
        import numpy as np
        
        # Mock Data Generation for Prediction
        # TODO: Replace with fetch from MarketDataService when linked
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='1D')
        df = pd.DataFrame(index=dates)
        df['open'] = 100 + np.random.randn(100).cumsum()
        df['high'] = df['open'] + 1
        df['low'] = df['open'] - 1
        df['close'] = df['open'] + np.random.randn(100) * 0.5
        df['volume'] = 1000
        
        service = get_prediction_service()
        
        # Ensure model is trained (for demo purposes, train on fly if needed)
        try:
            if service.model is None:
                 service.train_model(df)
                 
            result = service.predict_direction(df)
            result['symbol'] = symbol
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(communication_bp)
    
    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000, debug=True)
