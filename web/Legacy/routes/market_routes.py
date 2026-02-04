"""
==============================================================================
FILE: web/routes/market_routes.py
ROLE: Market Data API Blueprint
PURPOSE: Exposes endpoints for financial market data analysis, specifically:
         - Fear & Greed Index (Sentiment)
         - HypeMeter (Social Sentiment)
         - Market Predictions (Future MVP)
         
ARCHITECTURE:
    - Uses Flask Blueprint for modular routing.
    - Connects to Services Layer (FearGreedService, HypeMeterService).
    - Returns JSON responses.
    
DEPENDENCIES:
    - flask
    - services.market.fear_greed_service
    - services.market.hypemeter_service
==============================================================================
"""

from datetime import datetime
from flask import Blueprint, jsonify
from services.market.fear_greed_service import fear_greed_service

# Define Blueprint
market_bp = Blueprint('market_bp', __name__, url_prefix='/api/v1/market')

@market_bp.route('/fear-greed', methods=['GET'])
async def get_fear_greed():
    """
    Get current Fear & Greed Index score and components.
    Asynchronous endpoint to allow non-blocking IO if fetching from DB/External API.
    """
    data = await fear_greed_service.get_latest()
    return jsonify(data)

@market_bp.route('/hypemeter', methods=['GET'])
async def get_hypemeter_feed():
    """
    Get social sentiment feed (HypeMeter).
    """
    from services.market.hypemeter_service import hypemeter_service
    data = await hypemeter_service.get_hype_feed()
    return jsonify(data)

@market_bp.route('/hypemeter/top', methods=['GET'])
async def get_hypemeter_top():
    """
    Get top hyped assets.
    """
    from services.market.hypemeter_service import hypemeter_service
    data = await hypemeter_service.get_top_hyped_assets()
    return jsonify(data)

@market_bp.route('/options/<symbol>', methods=['GET'])
def get_options_chain(symbol):
    """
    Get options chain for a symbol.
    """
    from services.data.options_service import OptionsFlowService
    service = OptionsFlowService(mock=True)
    chain = service.fetch_historical_options(symbol)
    
    # Add greeks to each contract in the mock chain
    for contract in chain:
        contract['greeks'] = service.get_greeks(symbol, contract['strike'], contract['type'])
        
    return jsonify(chain)

@market_bp.route('/dom/<symbol>', methods=['GET'])
def get_market_depth(symbol):
    """
    Simulate Level 2 Market Depth (DOM).
    """
    import random
    base_price = 150.0 # Mock base
    
    # Generate 10 levels of bid/ask
    bids = []
    asks = []
    
    for i in range(1, 11):
        bids.append({
            "price": round(base_price - (i * 0.05), 2),
            "size": random.randint(100, 5000)
        })
        asks.append({
            "price": round(base_price + (i * 0.05), 2),
            "size": random.randint(100, 5000)
        })
        
    return jsonify({
        "symbol": symbol,
        "base_price": base_price,
        "bids": bids,
        "asks": asks,
        "spread": 0.05,
        "timestamp": datetime.now().isoformat()
    })
