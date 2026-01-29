import logging
import json
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class SchemaRegistryService:
    """
    Manages Avro schemas for Kafka payloads.
    In a production env, this might connect to Confluent Schema Registry.
    Here, it loads schemas from the local filesystem.
    """
    _instance = None
    _schemas: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SchemaRegistryService, cls).__new__(cls)
        return cls._instance

    def __init__(self, schema_dir: str = "schemas"):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.schema_dir = schema_dir
        self._load_local_schemas()
        logger.info("SchemaRegistryService initialized")

    def _load_local_schemas(self):
        """Loads .avsc files from the schemas directory."""
        if not os.path.exists(self.schema_dir):
            logger.warning(f"Schema directory '{self.schema_dir}' not found.")
            return

        for filename in os.listdir(self.schema_dir):
            if filename.endswith(".avsc"):
                schema_name = filename.replace(".avsc", "")
                full_path = os.path.join(self.schema_dir, filename)
                try:
                    with open(full_path, 'r') as f:
                        schema_content = json.load(f)
                        self._schemas[schema_name] = schema_content
                        logger.info(f"Loaded schema: {schema_name}")
                except Exception as e:
                    logger.error(f"Failed to load schema {filename}: {e}")

    def get_schema(self, schema_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves a loaded schema by name."""
        return self._schemas.get(schema_name)

    def validate_schema_compatibility(self, schema_name: str, payload_keys: set) -> bool:
        """
        Simple validation: checks if payload keys match schema fields.
        Does not replace full Avro serialization check but serves as a quick guard.
        """
        schema = self.get_schema(schema_name)
        if not schema:
            logger.error(f"Schema '{schema_name}' not found.")
            return False
            
        required_fields = {f['name'] for f in schema.get('fields', []) if 'default' not in f}
        # Check if all required fields are in payload_keys
        missing = required_fields - payload_keys
        if missing:
            logger.error(f"Payload missing required fields for '{schema_name}': {missing}")
            return False
            
        return True
