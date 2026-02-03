"""
Test Runner Script

Executes project tests using pytest with simplified CLI commands.
Maps CLI arguments (agents, api, etc.) to specific test directories.
"""
import pytest
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
TESTS_DIR = PROJECT_ROOT / "tests"

# Map CLI subcommands to test directories
TEST_MAPPING = {
    "agents": TESTS_DIR / "agents",
    "api": TESTS_DIR / "api",
    "services": TESTS_DIR / "services",
    "models": TESTS_DIR / "models",
    "billing": TESTS_DIR / "billing",
    "unit": TESTS_DIR / "unit",
    "integration": TESTS_DIR / "integration",
    # Add more mappings as verified
}

def run_tests(category: str = "all") -> int:
    """
    Run tests for a specific category or all tests.
    
    Args:
        category: The test category (e.g., 'agents', 'api', 'all')
        
    Returns:
        Exit code from pytest
    """
    logger.info(f"Running tests for category: {category}")
    
    args = ["-v"] # Default detailed output
    
    if category == "all":
        target_path = TESTS_DIR
    elif category in TEST_MAPPING:
        target_path = TEST_MAPPING[category]
        if not target_path.exists():
            logger.warning(f"Test directory not found: {target_path}")
            print(f"Directory {target_path} does not exist yet. Run 'cli.py tests all' to see available tests.")
            return 1
    else:
        logger.error(f"Unknown test category: {category}")
        return 1
        
    args.append(str(target_path))
    
    print(f"\n🚀 Executing: pytest {' '.join(args)}\n")
    
    try:
        # invoke pytest directly
        result = pytest.main(args)
        return result
    except Exception as e:
        logger.error(f"Failed to run tests: {e}")
        return 1

# CLI Handlers
def run_all_tests():
    sys.exit(run_tests("all"))

def run_agent_tests():
    sys.exit(run_tests("agents"))

def run_api_tests():
    sys.exit(run_tests("api"))

def run_service_tests():
    sys.exit(run_tests("services"))
    
def run_unit_tests():
    sys.exit(run_tests("unit"))

def run_integration_tests():
    sys.exit(run_tests("integration"))

if __name__ == "__main__":
    # verification run
    run_tests("all")
