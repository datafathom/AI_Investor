import logging
import json
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ChartEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChartEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.drawings_db: Dict[str, List[Dict]] = {} # schema: { chart_id: [drawing_objects] }
        self.layouts_db: Dict[str, Dict] = {} # schema: { layout_id: layout_config }
        self._initialized = True

    async def save_drawings(self, chart_id: str, drawings: List[Dict]) -> Dict:
        """Save drawings for a specific chart instance."""
        self.drawings_db[chart_id] = drawings
        return {"success": True, "count": len(drawings)}

    async def get_drawings(self, chart_id: str) -> List[Dict]:
        """Retrieve drawings for a specific chart."""
        return self.drawings_db.get(chart_id, [])

    async def save_layout(self, name: str, config: Dict) -> Dict:
        """Save a chart layout configuration."""
        layout_id = str(uuid.uuid4())
        layout = {
            "id": layout_id,
            "name": name,
            "config": config,
            "updated_at": datetime.now().isoformat()
        }
        self.layouts_db[layout_id] = layout
        return layout

    async def get_layouts(self) -> List[Dict]:
        """List all saved layouts."""
        return list(self.layouts_db.values())

    async def get_layout(self, layout_id: str) -> Optional[Dict]:
        """Get specific layout."""
        return self.layouts_db.get(layout_id)
