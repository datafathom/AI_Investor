
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Mock environment
os.environ['FLASK_ENV'] = 'development'
os.environ['POSTGRES_HOST'] = 'localhost'
os.environ['NEO4J_HOST'] = 'localhost'
os.environ['KAFKA_BOOTSTRAP_SERVERS'] = 'localhost:9092'

try:
    print("Attempting to import and create_app...")
    from web.app import create_app
    app, socketio = create_app()
    print("Success! App created.")
    
    print("\nRoutes found:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule} [{rule.methods}]")
        
except Exception as e:
    print(f"Failed to create app: {e}")
    import traceback
    traceback.print_exc()
