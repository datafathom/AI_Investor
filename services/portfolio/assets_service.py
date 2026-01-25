
import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'assets.json')

class AssetsService:
    """
    Manages physical and illiquid assets (Real Estate, Art, PE, etc.).
    Persists data to a local JSON file for portability and simplicity.
    """

    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.assets: List[Dict[str, Any]] = []
        self._load_data()

    def _load_data(self):
        """Load assets from JSON file."""
        if not os.path.exists(self.data_file):
            self.assets = []
            return

        try:
            with open(self.data_file, 'r') as f:
                self.assets = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load assets from {self.data_file}: {e}")
            self.assets = []

    def _save_data(self):
        """Save assets to JSON file."""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.assets, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save assets to {self.data_file}: {e}")

    def get_all_assets(self) -> List[Dict[str, Any]]:
        """Return all registered assets."""
        return self.assets

    def get_assets_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Filter assets by category."""
        return [a for a in self.assets if a.get('category') == category]

    def add_asset(self, asset_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new asset to the registry."""
        new_asset = {
            'id': str(uuid.uuid4()),
            'name': asset_data.get('name'),
            'category': asset_data.get('category'),
            'value': float(asset_data.get('value', 0.0)),
            'location': asset_data.get('location', ''),
            'purchaseDate': asset_data.get('purchaseDate', ''),
            'notes': asset_data.get('notes', ''),
            'currency': asset_data.get('currency', 'USD'),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        self.assets.append(new_asset)
        self._save_data()
        logger.info(f"Asset added: {new_asset['name']} ({new_asset['id']})")
        return new_asset

    def update_asset(self, asset_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing asset."""
        for asset in self.assets:
            if asset['id'] == asset_id:
                # Update fields
                for key, value in updates.items():
                    if key in ['id', 'created_at']: continue # Protected fields
                    if key == 'value':
                        asset[key] = float(value)
                    else:
                        asset[key] = value
                
                asset['updated_at'] = datetime.now().isoformat()
                self._save_data()
                logger.info(f"Asset updated: {asset_id}")
                return asset
        
        logger.warning(f"Attempted to update non-existent asset: {asset_id}")
        return None

    def delete_asset(self, asset_id: str) -> bool:
        """Remove an asset from registry."""
        initial_len = len(self.assets)
        self.assets = [a for a in self.assets if a['id'] != asset_id]
        
        if len(self.assets) < initial_len:
            self._save_data()
            logger.info(f"Asset deleted: {asset_id}")
            return True
        return False

    def get_total_valuation(self) -> float:
        """Calculate total value of all illiquid assets."""
        return sum(a['value'] for a in self.assets)

# Singleton Instance
assets_service = AssetsService()
