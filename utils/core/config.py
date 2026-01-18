"""
==============================================================================
FILE: utils/core/config.py
ROLE: Central Nervous System (Config)
PURPOSE: Loads, validates, and exposes environment variables and secrets.
USAGE: from utils.core.config import [VAR_NAME]
INPUT/OUTPUT:
    - Input: .env file
    - Output: Strongly typed configuration constants.
==============================================================================
"""

import os
from pathlib import Path
from typing import Optional

# Detection for resource-constrained environments
LITE_MODE = os.getenv("LITE_MODE", "false").lower() in ("true", "1", "yes")

from dotenv import load_dotenv

# Load .env file from project root
_project_root = Path(__file__).parent.parent.parent
_env_file = _project_root / ".env"
load_dotenv(_env_file)


def get_env(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable {key} is not set")
    return value


def get_env_int(key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
    value = get_env(key, default=str(default) if default is not None else None, required=required)
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        if required:
            raise ValueError(f"Environment variable {key} must be an integer")
        return default


def get_env_bool(key: str, default: Optional[bool] = None, required: bool = False) -> bool:
    value = get_env(key, default=str(default).lower() if default is not None else None, required=required)
    if value is None:
        return default if default is not None else False
    return value.lower() in ("true", "1", "yes", "on")


# Logging
LOG_LEVEL = get_env("LOG_LEVEL", "INFO")
LOGS_DIR = get_env("LOGS_DIR", str(_project_root / "logs"))

# Database Configuration
POSTGRES_HOST = get_env("POSTGRES_HOST", "localhost")
POSTGRES_PORT = get_env_int("POSTGRES_PORT", 5432)
POSTGRES_USER = get_env("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = get_env("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = get_env("POSTGRES_DB", "ai_investor")

# Neo4j Configuration
NEO4J_URI = get_env("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = get_env("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = get_env("NEO4J_PASSWORD", "password")

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = get_env("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Market Data Providers
ALPHA_VANTAGE_API_KEY = get_env("ALPHA_VANTAGE_API_KEY")
POLYGON_API_KEY = get_env("POLYGON_API_KEY")

# Reddit Integration (Phase 8)
REDDIT_CLIENT_ID = get_env("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = get_env("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = get_env("REDDIT_USER_AGENT", "ai_investor_v1")

# Robinhood Integration (Phase 24)
ROBINHOOD_USERNAME = get_env("ROBINHOOD_USERNAME")
ROBINHOOD_PASSWORD = get_env("ROBINHOOD_PASSWORD")
ROBINHOOD_TOTP = get_env("ROBINHOOD_TOTP")

# Macro Data Integration (Phase 10)
FRED_API_KEY = get_env("FRED_API_KEY")

