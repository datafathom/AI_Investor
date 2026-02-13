from fastapi import APIRouter
import uuid
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/banking", tags=["Banking"])

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: float
    memo: str

@router.get('/accounts')
async def get_linkable_accounts():
    """Get linked bank accounts."""
    return {"success": True, "data": [
        {"id": "ba_01", "name": "Chase Operating", "mask": "**1234", "balance": 450000.00, "status": "ACTIVE"},
        {"id": "ba_02", "name": "SVB Capital", "mask": "**5678", "balance": 800000.00, "status": "ACTIVE"}
    ]}

@router.post('/transfer')
async def initiate_transfer(req: TransferRequest):
    """Initiate a funds transfer."""
    return {"success": True, "data": {"id": str(uuid.uuid4()), "status": "PENDING_APPROVAL"}}

@router.get('/history')
async def get_transfer_history():
    """Get transfer history."""
    return {"success": True, "data": [
        {"id": "tx_01", "date": "2025-02-08", "amount": 50000.00, "from": "Chase Operating", "to": "Brokerage", "status": "CLEARED"},
        {"id": "tx_02", "date": "2025-02-01", "amount": 1000.00, "from": "Chase Operating", "to": "Vendor: AWS", "status": "CLEARED"}
    ]}

@router.get('/expenses')
async def get_expenses():
    """Get expense transactions."""
    return {"success": True, "data": [
        {"id": "exp_01", "date": "2025-02-05", "vendor": "AWS Web Services", "amount": 1250.45, "category": "Infrastructure"},
        {"id": "exp_02", "date": "2025-02-04", "vendor": "Bloomberg Data", "amount": 2500.00, "category": "Data Feeds"}
    ]}

@router.post('/expenses/categorize')
async def categorize_transaction(id: str, category: str):
    """Categorize an expense."""
    return {"success": True, "data": {"status": "UPDATED"}}

@router.get('/relationships')
async def list_banks():
    """List bank relationships."""
    return {"success": True, "data": [
        {"id": "bk_01", "name": "JPMorgan Chase", "rep": "Sarah Smith", "phone": "555-0123", "fdic_coverage": 250000},
        {"id": "bk_02", "name": "Silicon Valley Bank", "rep": "Mike Jones", "phone": "555-0199", "fdic_coverage": 250000}
    ]}

@router.get('/fees/{bank_id}')
async def get_bank_fees(bank_id: str):
    """Get bank fee schedule."""
    return {"success": True, "data": [
        {"service": "Wire Transfer (Dom)", "fee": 25.00},
        {"service": "Wire Transfer (Int)", "fee": 45.00},
        {"service": "ACH Batch", "fee": 5.00}
    ]}
