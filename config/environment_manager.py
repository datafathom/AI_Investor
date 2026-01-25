
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AppSettings:
    """
    Application settings managed by environment variables.
    """
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME", "AI Investor")
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
        
        # Database Settings
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://investor_user:investor_password@localhost:5432/investor_db")
        self.NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        
        # Security
        self.JWT_SECRET = os.getenv("JWT_SECRET", "dev_secret_key")
        
        # External APIs
        self.FRED_API_KEY = os.getenv("FRED_API_KEY")
        self.ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.GIVINGBLOCK_API_KEY = os.getenv("GIVINGBLOCK_API_KEY")
        self.CHARITYNAV_APP_ID = os.getenv("CHARITYNAV_APP_ID")
        self.CHARITYNAV_APP_KEY = os.getenv("CHARITYNAV_APP_KEY")
        
        # Scaling
        self.WS_SCALE_ENABLED = os.getenv("WS_SCALE_ENABLED", "false").lower() == "true"
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_settings: Optional[AppSettings] = None

def get_settings() -> AppSettings:
    """Singleton getter for application settings."""
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings
