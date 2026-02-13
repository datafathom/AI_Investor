from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/strategy", tags=["Strategy Library"])

@router.get('/templates')
async def list_templates():
    """List available strategy templates."""
    return {"success": True, "data": [
        {"id": "tpl_trend_01", "name": "Moving Average Crossover", "category": "Trend", "difficulty": "Easy", "rating": 4.5},
        {"id": "tpl_mean_01", "name": "Bollinger Band Reversion", "category": "Mean Reversion", "difficulty": "Medium", "rating": 4.2},
        {"id": "tpl_ml_01", "name": "LSTM Price Predictor", "category": "ML/AI", "difficulty": "Hard", "rating": 4.8}
    ]}

@router.get('/templates/{id}')
async def get_template_code(id: str):
    """Get template code."""
    code = """
class Strategy:
    def on_data(self, data):
        if data.close > data.sma(20):
            self.buy()
        elif data.close < data.sma(20):
            self.sell()
"""
    return {"success": True, "data": {"code": code, "docs": "Simple trend following strategy."}}
