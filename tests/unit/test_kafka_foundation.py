import unittest
import os
import json
from services.schema_registry import SchemaRegistryService
from services.validators.kafka_validators import KafkaValidatorService

class TestKafkaFoundation(unittest.TestCase):

    def setUp(self):
        # Create a dummy schema for testing
        self.test_schema_path = "schemas/test_schema.avsc"
        with open(self.test_schema_path, "w") as f:
            json.dump({
                "type": "record",
                "name": "TestRecord",
                "fields": [{"name": "required_field", "type": "string"}]
            }, f)
            
        self.registry = SchemaRegistryService() # Will load schemas/
        self.validator = KafkaValidatorService()

    def tearDown(self):
        if os.path.exists(self.test_schema_path):
            os.remove(self.test_schema_path)

    def test_schema_loading(self):
        """Test that the registry loads schemas from disk."""
        # Reload registry to pick up the test schema created in setUp
        self.registry._load_local_schemas()
        
        schema = self.registry.get_schema("test_schema")
        self.assertIsNotNone(schema)
        self.assertEqual(schema['name'], "TestRecord")

    def test_market_telemetry_schema_exists(self):
        """Verify the critical market_telemetry schema exists."""
        schema = self.registry.get_schema("market_telemetry")
        self.assertIsNotNone(schema)
        self.assertEqual(schema['namespace'], "com.ai_investor.telemetry")

    def test_validation_success(self):
        """Test payload validation with correct fields."""
        self.registry._load_local_schemas()
        
        valid_payload = {"required_field": "some_value"}
        result = self.validator.validate_payload("test_schema", valid_payload, schema_name="test_schema")
        self.assertTrue(result)

    def test_validation_failure(self):
        """Test payload validation with missing fields."""
        self.registry._load_local_schemas()
        
        invalid_payload = {"wrong_field": "some_value"}
        result = self.validator.validate_payload("test_schema", invalid_payload, schema_name="test_schema")
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
