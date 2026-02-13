"""
Execution Core API
Handles order lifecycle, submission, cancellation, and modification.
"""
from fastapi import APIRouter, HTTPException, Body, Path
from typing import List, Dict, Optional
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/v1/execution/orders", tags=["Order Execution"])

# Mock Order Database
_orders = []

@router.get("/")
async def list_orders():
    return {"success": True, "data": _orders}

@router.post("/")
async def submit_order(order: Dict = Body(...)):
    new_order = {
        "id": str(uuid.uuid4()),
        "ticker": order.get("ticker"),
        "side": order.get("side"),
        "qty": order.get("qty"),
        "type": order.get("type", "MARKET"),
        "limit_price": order.get("limit_price"),
        "status": "QUEUED",
        "filled_qty": 0,
        "avg_fill_price": 0.0,
        "submitted_at": datetime.now().isoformat(),
        "venue": "SMART"
    }
    _orders.insert(0, new_order)
    return {"success": True, "data": new_order}

@router.delete("/{order_id}")
async def cancel_order(order_id: str = Path(...)):
    for order in _orders:
        if order["id"] == order_id:
            if order["status"] in ["FILLED", "CANCELLED"]:
                raise HTTPException(status_code=400, detail="Order cannot be cancelled")
            order["status"] = "CANCELLED"
            return {"success": True, "data": order}
    raise HTTPException(status_code=404, detail="Order not found")

@router.patch("/{order_id}")
async def modify_order(order_id: str = Path(...), updates: Dict = Body(...)):
    for order in _orders:
        if order["id"] == order_id:
            if order["status"] in ["FILLED", "CANCELLED"]:
                raise HTTPException(status_code=400, detail="Order cannot be modified")
            
            if "qty" in updates: order["qty"] = updates["qty"]
            if "limit_price" in updates: order["limit_price"] = updates["limit_price"]
            
            return {"success": True, "data": order}
    raise HTTPException(status_code=404, detail="Order not found")

@router.post("/preview")
async def preview_order(order: Dict = Body(...)):
    """
    Estimates costs, impact, and slippage for a potential order.
    """
    qty = float(order.get("qty", 0))
    price = 150.00 # Mock price
    notional = qty * price
    
    return {
        "success": True,
        "data": {
            "estimated_price": price,
            "notional": notional,
            "commission": max(1.0, notional * 0.0005),
            "market_impact_bps": 2.5 if qty > 1000 else 0.5,
            "slippage_estimate": 0.02,
            "venue_allocation": {"IEX": 0.4, "NASDAQ": 0.3, "DARK": 0.3}
        }
    }
