import logging
from typing import Tuple, Dict

logger = logging.getLogger(__name__)

class GeofenceService:
    """
    Monitors physical location (Mocked) to enforce travel policies.
    """
    _instance = None
    
    # Mock "Home Base" (NYC)
    HOME_COORDS = (40.7128, -74.0060)
    ALLOWED_RADIUS_KM = 50.0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeofenceService, cls).__new__(cls)
            cls._instance.current_location = cls.HOME_COORDS
            cls._instance.status = "SECURE"
        return cls._instance

    def update_location(self, lat: float, lon: float) -> Dict[str, str]:
        """
        Updates device location. Triggers lockdown if impossible travel or out of bounds.
        """
        # Simple Mock Distance Check (Euclidean approx is fine for prototype logic)
        lat_diff = abs(lat - self.HOME_COORDS[0])
        lon_diff = abs(lon - self.HOME_COORDS[1])
        
        # Rough "Is far away" check
        if lat_diff > 1.0 or lon_diff > 1.0: # > ~100km
             self.status = "LOCKDOWN"
             logger.critical(f"Geofence Violated! Location: {lat}, {lon}")
             return {"status": "LOCKDOWN", "reason": "OUT_OF_BOUNDS"}
        
        self.current_location = (lat, lon)
        self.status = "SECURE"
        return {"status": "SECURE", "reason": "WITHIN_PERIMETER"}

    def check_access(self) -> bool:
        return self.status == "SECURE"

# Singleton
geofence_service = GeofenceService()
def get_geofence_service() -> GeofenceService:
    return geofence_service
