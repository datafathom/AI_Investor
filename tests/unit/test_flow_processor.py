import pytest
from services.funds.flow_processor import FlowProcessor

def test_flow_processor_normal():
    processor = FlowProcessor()
    data = {"ticker": "SPY", "net_flow_usd": 500000000.0} # $500M inflow
    result = processor.process_flow(data)
    assert result["significant_outflow"] == False
    assert result["net_flow"] == 500000000.0

def test_flow_processor_heavy_outflow():
    processor = FlowProcessor()
    data = {"ticker": "QQQ", "net_flow_usd": -1500000000.0} # -$1.5B outflow
    result = processor.process_flow(data)
    assert result["significant_outflow"] == True
    assert result["ticker"] == "QQQ"
