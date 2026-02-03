
import sys
import os
from pathlib import Path

# Add project root to Python path (like app.py does)
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))

try:
    print("Importing dashboard_api...")
    from web.api.dashboard_api import dashboard_bp
    
    print("Importing communication_api...")
    from web.api.communication_api import communication_bp
    
    print("Importing politics_api...")
    from web.api.politics_api import politics_bp
    
    print("Importing evolution_api...")
    from web.api.evolution_api import evolution_bp
    
    print("Importing debate_api...")
    from web.api.debate_api import debate_bp
    
    print("Importing autocoder_api...")
    from web.api.autocoder_api import autocoder_bp
    
    print("Importing spatial_api...")
    from web.api.spatial_api import spatial_bp
    # risk_api skipped
    # assets_api skipped
    
    print("Importing attribution_api...")
    from web.api.attribution_api import attribution_bp
    
    print("Success")
except Exception as e:
    print("FAILURE")
    import traceback
    traceback.print_exc()
