import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from services.tax.tax_overlay_service import TaxOverlayService, TaxLot

def test_identify_harvest_opportunities():
    service = TaxOverlayService()
    portfolio_id = "SMA_001"
    
    # Lot with a loss
    lot_loss = TaxLot(
        lot_id="LOT_1",
        symbol="AAPL",
        quantity=Decimal("100"),
        cost_basis=Decimal("150.0"),
        acquisition_date=datetime.now() - timedelta(days=45),
        current_price=Decimal("140.0")
    )
    # 100 * (140 - 150) = -1000
    
    # Lot with a gain
    lot_gain = TaxLot(
        lot_id="LOT_2",
        symbol="MSFT",
        quantity=Decimal("50"),
        cost_basis=Decimal("200.0"),
        acquisition_date=datetime.now() - timedelta(days=60),
        current_price=Decimal("250.0")
    )
    
    service.add_lot(portfolio_id, lot_loss)
    service.add_lot(portfolio_id, lot_gain)
    
    opportunities = service.identify_harvest_opportunities(portfolio_id, Decimal("-500.0"))
    assert len(opportunities) == 1
    assert opportunities[0].lot_id == "LOT_1"
    assert opportunities[0].unrealized_p_l == Decimal("-1000.0")

def test_optimize_sma_placeholders():
    service = TaxOverlayService()
    portfolio_id = "SMA_002"
    
    lot = TaxLot(
        lot_id="LOT_X",
        symbol="TSLA",
        quantity=Decimal("10"),
        cost_basis=Decimal("800.0"),
        acquisition_date=datetime.now() - timedelta(days=100),
        current_price=Decimal("700.0")
    )
    service.add_lot(portfolio_id, lot)
    
    adjustments = service.optimize_sma(portfolio_id, {"TSLA": Decimal("10")})
    assert adjustments["TSLA"] == Decimal("-10")
    assert adjustments["TSLA_PROXY"] == Decimal("10")
