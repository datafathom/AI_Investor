"""
scripts/runners/test_data_ingestion.py
Purpose: CLI command to test Phase 6 (Data Tap).
"""

import time
import logging
from services.data.alpha_vantage import AlphaVantageClient
from services.data.producer import MarketDataProducer

logger = logging.getLogger(__name__)

def run_test_ingestion(symbol: str = "SPY", **kwargs):
    """
    Test the data pipeline.
    1. Fetch quote from Alpha Vantage.
    2. Publish to Kafka.
    """
    print(f"Testing Data Ingestion for {symbol}...")
    
    # 1. Init Client
    client = AlphaVantageClient()
    if not client.api_key:
        print("Error: ALPHA_VANTAGE_API_KEY not found in env.")
        # Proceed with mock data for testing if no key
        data = {"symbol": symbol, "price": 450.00, "volume": 1000000, "change_percent": "0.5%"}
        print(f"Using MOCK data: {data}")
    else:
        data = client.get_latest_price(symbol)
        if not data:
            print("Failed to fetch data from API.")
            return False
        print(f"Fetched Data: {data}")

    # 2. Init Producer
    producer = MarketDataProducer()
    
    # 3. Publish
    if producer.producer:
        producer.publish_quote(
            symbol=data["symbol"],
            price=data["price"],
            volume=data["volume"],
            source="AlphaVantage"
        )
        print("Published to Kafka topic 'market.equity'")
    else:
        print("Skipping Kafka publish (Producer not available)")
        
    return True
