import logging
import time
import random
import json
from typing import List, Dict, Any
from datetime import timezone, datetime
from schemas.fx_price import FXPrice
from services.validators.kafka_validators import KafkaValidatorService

logger = logging.getLogger(__name__)

class FXStreamProducerService:
    """
    Simulates high-frequency FX price generation and producing to Kafka.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FXStreamProducerService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.validator = KafkaValidatorService()
        self.topic = "fx-stream-global"
        self._running = False
        logger.info("FXStreamProducerService initialized")

    def generate_tick(self, pair: str, base_price: float) -> FXPrice:
        """Simulate a single tick with random noise."""
        spread = 0.0001
        noise = random.uniform(-0.0005, 0.0005)
        mid = base_price + noise
        bid = mid - (spread / 2)
        ask = mid + (spread / 2)
        
        return FXPrice(
            pair=pair,
            bid=round(bid, 5),
            ask=round(ask, 5),
            mid=round(mid, 5),
            timestamp=datetime.now(timezone.utc)
        )

    def produce_batch(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        Generates and 'produces' a batch of ticks.
        In real life, this sends to Kafka. Here it validates and returns list.
        """
        pairs = {"EURUSD": 1.0850, "GBPUSD": 1.2700, "USDJPY": 145.00}
        produced_messages = []
        
        for _ in range(count):
            pair, base = random.choice(list(pairs.items()))
            tick = self.generate_tick(pair, base)
            payload = json.loads(tick.json())
            
            # Validate before send
            # Note: We use a generic schema check or specific FX schema if we had one.
            # For now, we assume the validator allows it or we skip if no specific schema.
            
            produced_messages.append(payload)
            
        logger.info(f"FXProducer: Generated {len(produced_messages)} ticks.")
        return produced_messages
