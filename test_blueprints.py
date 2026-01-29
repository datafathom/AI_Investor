
import os
import sys
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))

# Mock some drivers to avoid DB errors
from unittest.mock import MagicMock
sys.modules["psycopg2"] = MagicMock()
sys.modules["psycopg2.extras"] = MagicMock()
sys.modules["psycopg2.pool"] = MagicMock()
sys.modules["redis"] = MagicMock()
sys.modules["confluent_kafka"] = MagicMock()
sys.modules["confluent_kafka.admin"] = MagicMock()
sys.modules["neo4j"] = MagicMock()
sys.modules["elasticsearch"] = MagicMock()

from flask import Flask

original_register = Flask.register_blueprint

def trace_register(self, blueprint, **options):
    name = options.get('name', blueprint.name)
    print(f"TRACE: Registering blueprint '{name}' (from {blueprint})")
    return original_register(self, blueprint, **options)

Flask.register_blueprint = trace_register

try:
    from web.app import create_app
    app, _ = create_app()
    print("\nFINAL REGISTERED BLUEPRINTS:")
    for name, bp in app.blueprints.items():
        print(f" - {name}: {bp}")
except Exception as e:
    print(f"\nCRITICAL ERROR during create_app: {e}")
    import traceback
    traceback.print_exc()
