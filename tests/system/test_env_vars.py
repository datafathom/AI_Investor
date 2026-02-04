import pytest
from utils.core import config

def test_critical_env_vars_set():
    """
    Verify that all critical environment variables are set.
    """
    critical_vars = [
        ("POSTGRES_HOST", config.POSTGRES_HOST),
        ("POSTGRES_PORT", config.POSTGRES_PORT),
        ("POSTGRES_USER", config.POSTGRES_USER),
        ("POSTGRES_PASSWORD", config.POSTGRES_PASSWORD),
        ("POSTGRES_DB", config.POSTGRES_DB),
        ("NEO4J_URI", config.NEO4J_URI),
        ("NEO4J_USER", config.NEO4J_USER),
        ("NEO4J_PASSWORD", config.NEO4J_PASSWORD),
        ("KAFKA_BOOTSTRAP_SERVERS", config.KAFKA_BOOTSTRAP_SERVERS),
    ]

    missing_vars = []
    for name, value in critical_vars:
        if not value:
            missing_vars.append(name)
    
    assert not missing_vars, f"Critical environment variables missing: {', '.join(missing_vars)}"

def test_api_keys_set():
    """
    Verify that API keys are set (warn if missing, strict check options can be added later).
    """
    api_keys = [
        ("ALPHA_VANTAGE_API_KEY", config.ALPHA_VANTAGE_API_KEY),
        ("POLYGON_API_KEY", config.POLYGON_API_KEY),
        ("FRED_API_KEY", config.FRED_API_KEY),
    ]

    missing_keys = []
    for name, value in api_keys:
        if not value:
            missing_keys.append(name)
            
    # For now, we might not fail if keys are missing in dev, but the user asked to test if they have a value.
    # We will fail if they are strictly required. Assuming critical for full functionality.
    # To prevent blocking local dev without keys, we might use a warning or a soft assertion if this is confusing.
    # However, "tests env" suggests we want to know what's missing.
    
    if missing_keys:
        pytest.fail(f"Missing API Keys: {', '.join(missing_keys)}")
