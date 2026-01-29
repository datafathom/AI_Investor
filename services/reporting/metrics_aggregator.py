import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MetricsAggregator:
    """Aggregates all risk and return metrics for the Wealth Manager dashboard."""
    
    def aggregate_portfolio_view(self, portfolio_id: str, historical_metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Policy: Summarize the latest metrics and provide trend indicators.
        """
        if not historical_metrics: return {}
        
        latest = historical_metrics[-1]
        
        logger.info(f"REPORT_LOG: Aggregating latest view for {portfolio_id}: Sharpe {latest.get('sharpe_ratio'):.2f}, Sortino {latest.get('sortino_ratio'):.2f}")
        
        return {
            "portfolio_id": portfolio_id,
            "current_sharpe": latest.get("sharpe_ratio"),
            "current_sortino": latest.get("sortino_ratio"),
            "current_alpha": latest.get("alpha"),
            "last_updated": latest.get("metric_date")
        }
