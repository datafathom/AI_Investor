"""
==============================================================================
FILE: web/api/charting_api.py
ROLE: Charting API Endpoints
PURPOSE: REST endpoints for chart data and technical analysis.

INTEGRATION POINTS:
    - ChartingService: Chart data preparation
    - TechnicalAnalysisService: Indicator calculations
    - FrontendCharts: Chart visualization components

ENDPOINTS:
    - GET /api/charting/data/:symbol
    - GET /api/charting/indicators/:symbol
    - GET /api/charting/patterns/:symbol
    - GET /api/charting/signals/:symbol

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from services.charting.charting_service import get_charting_service
from services.analysis.technical_analysis_service import get_technical_analysis_service

logger = logging.getLogger(__name__)

charting_bp = Blueprint('charting', __name__, url_prefix='/api/charting')


@charting_bp.route('/data/<symbol>', methods=['GET'])
async def get_chart_data(symbol: str):
    """
    Get chart data for symbol.
    
    Query params:
        timeframe: Chart timeframe (default: 1day)
        chart_type: Chart type (candlestick, line, area, heikin_ashi)
        indicators: Comma-separated list of indicators
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    """
    try:
        timeframe = request.args.get('timeframe', '1day')
        chart_type = request.args.get('chart_type', 'candlestick')
        indicators_str = request.args.get('indicators', '')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        indicators = [i.strip() for i in indicators_str.split(',')] if indicators_str else None
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
        
        service = get_charting_service()
        chart_data = await service.get_chart_data(
            symbol=symbol,
            timeframe=timeframe,
            chart_type=chart_type,
            indicators=indicators,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
        
    except Exception as e:
        logger.error(f"Error getting chart data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@charting_bp.route('/indicators/<symbol>', methods=['GET'])
async def get_indicators(symbol: str):
    """
    Get technical indicators for symbol.
    
    Query params:
        indicators: Comma-separated list of indicators (RSI, MACD, SMA_20, etc.)
        timeframe: Chart timeframe (default: 1day)
    """
    try:
        indicators_str = request.args.get('indicators', 'RSI,MACD')
        timeframe = request.args.get('timeframe', '1day')
        
        indicators = [i.strip() for i in indicators_str.split(',')]
        
        # Get chart data first
        charting_service = get_charting_service()
        chart_data = await charting_service.get_chart_data(
            symbol=symbol,
            timeframe=timeframe
        )
        
        # Convert to DataFrame
        import pandas as pd
        data = pd.DataFrame(chart_data['data'])
        
        # Calculate indicators
        ta_service = get_technical_analysis_service()
        indicator_results = await ta_service.calculate_indicators(data, indicators)
        
        # Convert to serializable format
        results = {}
        for name, values in indicator_results.items():
            if isinstance(values, pd.DataFrame):
                results[name] = values.to_dict('records')
            else:
                results[name] = values.tolist()
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'timeframe': timeframe,
                'indicators': results
            }
        })
        
    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@charting_bp.route('/patterns/<symbol>', methods=['GET'])
async def get_patterns(symbol: str):
    """
    Recognize chart patterns for symbol.
    
    Query params:
        timeframe: Chart timeframe (default: 1day)
    """
    try:
        timeframe = request.args.get('timeframe', '1day')
        
        # Get chart data
        charting_service = get_charting_service()
        chart_data = await charting_service.get_chart_data(
            symbol=symbol,
            timeframe=timeframe
        )
        
        # Convert to DataFrame
        import pandas as pd
        data = pd.DataFrame(chart_data['data'])
        
        # Recognize patterns
        ta_service = get_technical_analysis_service()
        patterns = await ta_service.recognize_patterns(data)
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'timeframe': timeframe,
                'patterns': patterns
            }
        })
        
    except Exception as e:
        logger.error(f"Error recognizing patterns: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@charting_bp.route('/signals/<symbol>', methods=['GET'])
async def get_signals(symbol: str):
    """
    Generate trading signals for symbol.
    
    Query params:
        timeframe: Chart timeframe (default: 1day)
    """
    try:
        timeframe = request.args.get('timeframe', '1day')
        
        # Get chart data
        charting_service = get_charting_service()
        chart_data = await charting_service.get_chart_data(
            symbol=symbol,
            timeframe=timeframe
        )
        
        # Convert to DataFrame
        import pandas as pd
        data = pd.DataFrame(chart_data['data'])
        
        # Generate signals
        ta_service = get_technical_analysis_service()
        signals = await ta_service.generate_signals(data)
        
        return jsonify({
            'success': True,
            'data': {
                'symbol': symbol,
                'timeframe': timeframe,
                'signals': signals
            }
        })
        
    except Exception as e:
        logger.error(f"Error generating signals: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
