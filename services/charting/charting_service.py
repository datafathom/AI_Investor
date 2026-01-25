"""
==============================================================================
FILE: services/charting/charting_service.py
ROLE: Advanced Charting Engine
PURPOSE: Provides chart data preparation, indicator calculations, and
         multi-timeframe support for professional-grade technical analysis.

INTEGRATION POINTS:
    - MarketDataService: Historical and real-time price data
    - IndicatorService: Technical indicator calculations
    - ChartingAPI: Chart data endpoints
    - FrontendCharts: Chart visualization components

FEATURES:
    - Multiple chart types (candlestick, line, area, Heikin-Ashi)
    - Multiple timeframes (1min to 1year)
    - Indicator overlay support
    - Custom study creation

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from services.data.alpha_vantage import AlphaVantageClient
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class ChartType:
    """Chart type constants."""
    CANDLESTICK = "candlestick"
    LINE = "line"
    AREA = "area"
    HEIKIN_ASHI = "heikin_ashi"


class Timeframe:
    """Timeframe constants."""
    MIN_1 = "1min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    HOUR_1 = "1hr"
    HOUR_4 = "4hr"
    DAY_1 = "1day"
    WEEK_1 = "1week"
    MONTH_1 = "1month"
    YEAR_1 = "1year"


class ChartingService:
    """
    Service for chart data preparation and multi-timeframe support.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.market_data_client = AlphaVantageClient()
        self.cache_service = get_cache_service()
        
    async def get_chart_data(
        self,
        symbol: str,
        timeframe: str = "1day",
        chart_type: str = "candlestick",
        indicators: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """
        Get chart data for symbol with optional indicators.
        
        Args:
            symbol: Stock symbol
            timeframe: Chart timeframe
            chart_type: Type of chart (candlestick, line, area, heikin_ashi)
            indicators: List of indicators to overlay
            start_date: Optional start date
            end_date: Optional end date
            
        Returns:
            Chart data dictionary with OHLCV and indicators
        """
        logger.info(f"Getting chart data for {symbol} with timeframe {timeframe}")
        
        # Check cache
        cache_key = f"chart:{symbol}:{timeframe}:{chart_type}:{start_date}:{end_date}"
        cached_result = self.cache_service.get(cache_key)
        if cached_result:
            logger.info(f"Cache hit for chart data")
            return cached_result
        
        # Get price data
        price_data = await self._get_price_data(symbol, timeframe, start_date, end_date)
        
        # Transform based on chart type
        if chart_type == ChartType.HEIKIN_ASHI:
            price_data = self._convert_to_heikin_ashi(price_data)
        elif chart_type == ChartType.LINE:
            price_data = self._convert_to_line(price_data)
        elif chart_type == ChartType.AREA:
            price_data = self._convert_to_area(price_data)
        
        # Calculate indicators if requested
        indicators_data = {}
        if indicators:
            from services.analysis.technical_analysis_service import get_technical_analysis_service
            ta_service = get_technical_analysis_service()
            indicators_data = await ta_service.calculate_indicators(
                price_data, indicators
            )
        
        result = {
            'symbol': symbol,
            'timeframe': timeframe,
            'chart_type': chart_type,
            'data': price_data.to_dict('records') if isinstance(price_data, pd.DataFrame) else price_data,
            'indicators': indicators_data,
            'metadata': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None,
                'data_points': len(price_data) if isinstance(price_data, pd.DataFrame) else len(price_data)
            }
        }
        
        # Cache result (5 minutes for intraday, 1 hour for daily+)
        ttl = 300 if timeframe in [Timeframe.MIN_1, Timeframe.MIN_5, Timeframe.MIN_15] else 3600
        self.cache_service.set(cache_key, result, ttl=ttl)
        
        return result
    
    async def aggregate_timeframe(
        self,
        data: pd.DataFrame,
        source_timeframe: str,
        target_timeframe: str
    ) -> pd.DataFrame:
        """
        Aggregate data from one timeframe to another.
        
        Args:
            data: Source DataFrame with OHLCV data
            source_timeframe: Source timeframe
            target_timeframe: Target timeframe
            
        Returns:
            Aggregated DataFrame
        """
        if source_timeframe == target_timeframe:
            return data
        
        # Define aggregation rules
        agg_rules = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        
        # Resample based on target timeframe
        if target_timeframe == Timeframe.MIN_5:
            freq = '5T'
        elif target_timeframe == Timeframe.MIN_15:
            freq = '15T'
        elif target_timeframe == Timeframe.MIN_30:
            freq = '30T'
        elif target_timeframe == Timeframe.HOUR_1:
            freq = '1H'
        elif target_timeframe == Timeframe.HOUR_4:
            freq = '4H'
        elif target_timeframe == Timeframe.DAY_1:
            freq = '1D'
        elif target_timeframe == Timeframe.WEEK_1:
            freq = '1W'
        elif target_timeframe == Timeframe.MONTH_1:
            freq = '1M'
        else:
            return data
        
        # Ensure datetime index
        if not isinstance(data.index, pd.DatetimeIndex):
            if 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data = data.set_index('date')
            else:
                data.index = pd.date_range(start='2024-01-01', periods=len(data), freq='1D')
        
        aggregated = data.resample(freq).agg(agg_rules).dropna()
        
        return aggregated
    
    def _convert_to_heikin_ashi(self, data: pd.DataFrame) -> pd.DataFrame:
        """Convert OHLC data to Heikin-Ashi."""
        ha_data = data.copy()
        
        ha_data['ha_close'] = (data['open'] + data['high'] + data['low'] + data['close']) / 4
        ha_data['ha_open'] = 0.0
        
        for i in range(len(ha_data)):
            if i == 0:
                ha_data.iloc[i, ha_data.columns.get_loc('ha_open')] = (data.iloc[i]['open'] + data.iloc[i]['close']) / 2
            else:
                ha_data.iloc[i, ha_data.columns.get_loc('ha_open')] = (
                    ha_data.iloc[i-1]['ha_open'] + ha_data.iloc[i-1]['ha_close']
                ) / 2
        
        ha_data['ha_high'] = ha_data[['high', 'ha_open', 'ha_close']].max(axis=1)
        ha_data['ha_low'] = ha_data[['low', 'ha_open', 'ha_close']].min(axis=1)
        
        # Replace original OHLC with Heikin-Ashi values
        ha_data['open'] = ha_data['ha_open']
        ha_data['high'] = ha_data['ha_high']
        ha_data['low'] = ha_data['ha_low']
        ha_data['close'] = ha_data['ha_close']
        
        return ha_data.drop(columns=['ha_open', 'ha_high', 'ha_low', 'ha_close'], errors='ignore')
    
    def _convert_to_line(self, data: pd.DataFrame) -> pd.DataFrame:
        """Convert to line chart (close prices only)."""
        return data[['close']].rename(columns={'close': 'value'})
    
    def _convert_to_area(self, data: pd.DataFrame) -> pd.DataFrame:
        """Convert to area chart (close prices)."""
        return data[['close']].rename(columns={'close': 'value'})
    
    async def _get_price_data(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[datetime],
        end_date: Optional[datetime]
    ) -> pd.DataFrame:
        """Get price data for symbol."""
        # In production, fetch from market data service
        # For now, generate mock data
        dates = pd.date_range(
            start=start_date or datetime.now() - timedelta(days=365),
            end=end_date or datetime.now(),
            freq='1D'
        )
        
        np.random.seed(42)
        base_price = 100.0
        returns = np.random.normal(0.001, 0.02, len(dates))
        prices = base_price * (1 + returns).cumprod()
        
        data = pd.DataFrame({
            'date': dates,
            'open': prices * (1 + np.random.normal(0, 0.005, len(dates))),
            'high': prices * (1 + abs(np.random.normal(0, 0.01, len(dates)))),
            'low': prices * (1 - abs(np.random.normal(0, 0.01, len(dates)))),
            'close': prices,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        })
        
        return data


# Singleton instance
_charting_service: Optional[ChartingService] = None


def get_charting_service() -> ChartingService:
    """Get singleton charting service instance."""
    global _charting_service
    if _charting_service is None:
        _charting_service = ChartingService()
    return _charting_service
