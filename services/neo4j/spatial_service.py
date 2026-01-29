import math
from typing import Dict, Any, Tuple

class SpatialService:
    """
    Project Lat/Long coordinates onto a 3D sphere or plane for visualization.
    Used by SpatialAssetBubble.
    """
    def __init__(self, radius: float = 100.0):
        self.radius = radius

    def project_to_sphere(self, lat: float, lon: float) -> Tuple[float, float, float]:
        """
        Projects Lat/Long to X, Y, Z on a sphere.
        """
        # Convert degrees to radians
        phi = (90 - lat) * (math.pi / 180)
        theta = (lon + 180) * (math.pi / 180)

        x = -(self.radius * math.sin(phi) * math.cos(theta))
        z = (self.radius * math.sin(phi) * math.sin(theta))
        y = (self.radius * math.cos(phi))

        return (x, y, z)

    def project_to_plane(self, lat: float, lon: float, scale: float = 1.0) -> Tuple[float, float]:
        """
        Simple Mercator projection for 2D maps.
        """
        x = (lon + 180) * (scale / 360)
        lat_rad = lat * math.pi / 180
        merc_n = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
        y = (scale / 2) - (scale * merc_n / (2 * math.pi))
        
        return (x, y)

spatial_service = SpatialService()
