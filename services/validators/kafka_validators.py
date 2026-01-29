import logging
from typing import Dict, Any
from services.schema_registry import SchemaRegistryService

logger = logging.getLogger(__name__)

class KafkaValidatorService:
    """
    Validates message payloads before they are sent to Kafka.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(KafkaValidatorService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.registry = SchemaRegistryService()
        logger.info("KafkaValidatorService initialized")

    def validate_payload(self, topic: str, payload: Dict[str, Any], schema_name: str = None) -> bool:
        """
        Validates a dictionary payload against the schema.
        If schema_name is not provided, tries to infer from topic.
        """
        if not schema_name:
            # Simple inference: topic 'market-telemetry' -> schema 'market_telemetry'
            schema_name = topic.replace("-", "_")
            
        schema = self.registry.get_schema(schema_name)
        if not schema:
            logger.warning(f"No schema found for topic '{topic}' (inferred '{schema_name}'). Skipping strict validation.")
            return True # Allow unknown topics or enforce strictness? enforcing strictness is better but let's warn for now.
            
        # Check keys
        payload_keys = set(payload.keys())
        is_valid = self.registry.validate_schema_compatibility(schema_name, payload_keys)
        
        if is_valid:
            logger.debug(f"Payload for '{topic}' passed validation via '{schema_name}'.")
        else:
            logger.error(f"Payload for '{topic}' FAILED validation via '{schema_name}'.")
            
        return is_valid
