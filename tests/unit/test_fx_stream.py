import unittest
from models.fx_price import FXPrice
from services.fx_stream_producer import FXStreamProducerService
from services.fx_stream_consumer import FXStreamConsumerService

class TestFXStream(unittest.TestCase):

    def setUp(self):
        self.producer = FXStreamProducerService()
        self.consumer = FXStreamConsumerService()

    def test_fx_price_model(self):
        """Test Pydantic validation for FX Price."""
        # Valid tick
        tick = FXPrice(pair="EURUSD", bid=1.0500, ask=1.0502, mid=1.0501)
        self.assertEqual(tick.mid, 1.0501)
        
        # Invalid tick (bid > ask is physically possible but rare/crossed, 
        # but our model just checks general types and constraints > 0)
        with self.assertRaises(ValueError):
            FXPrice(pair="EURUSD", bid=-1.0, ask=1.0, mid=0.0)

    def test_producer_generation(self):
        """Test generation of simulated ticks."""
        tick = self.producer.generate_tick("GBPUSD", 1.2500)
        self.assertEqual(tick.pair, "GBPUSD")
        self.assertTrue(tick.bid < tick.ask)
        
    def test_producer_consumer_flow(self):
        """Test the end-to-end flow from producer to consumer."""
        # Produce 10 ticks
        messages = self.producer.produce_batch(count=10)
        self.assertEqual(len(messages), 10)
        
        # Consume 10 ticks
        processed = self.consumer.consume_batch(messages)
        self.assertEqual(processed, 10)

if __name__ == '__main__':
    unittest.main()
