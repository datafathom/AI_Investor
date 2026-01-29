import pytest
from services.reporting.metrics_aggregator import MetricsAggregator

def test_aggregation_latest():
    svc = MetricsAggregator()
    data = [
        {"metric_date": "2025-01-01", "sharpe_ratio": 1.5, "sortino_ratio": 2.0},
        {"metric_date": "2025-01-02", "sharpe_ratio": 1.6, "sortino_ratio": 2.1}
    ]
    res = svc.aggregate_portfolio_view("P123", data)
    assert res["current_sharpe"] == 1.6
    assert res["last_updated"] == "2025-01-02"

def test_aggregation_empty():
    svc = MetricsAggregator()
    assert svc.aggregate_portfolio_view("P123", []) == {}
