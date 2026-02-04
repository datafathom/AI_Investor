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
    "agents": [TESTS_DIR / "agents"],
    "api": [TESTS_DIR / "api"],
    "schemas": [TESTS_DIR / "schemas"],
    "billing": [TESTS_DIR / "billing"],
    "unit": [TESTS_DIR / "unit"],
    "integration": [TESTS_DIR / "integration"],
    
    # Aggregated "Services" Category - includes all domain logic tests
    "services": [
        TESTS_DIR / "ai",
        TESTS_DIR / "ai_assistant",
        TESTS_DIR / "ai_predictions",
        TESTS_DIR / "alternative",
        TESTS_DIR / "analysis",
        TESTS_DIR / "analytics",
        TESTS_DIR / "auth",
        TESTS_DIR / "budgeting",
        TESTS_DIR / "chaos",
        TESTS_DIR / "charting",
        TESTS_DIR / "communication",
        TESTS_DIR / "community",
        TESTS_DIR / "compliance",
        TESTS_DIR / "credit",
        TESTS_DIR / "crypto",
        TESTS_DIR / "deal",
        TESTS_DIR / "education",
        TESTS_DIR / "emergency",
        TESTS_DIR / "enterprise",
        TESTS_DIR / "estate",
        TESTS_DIR / "execution",
        TESTS_DIR / "institutional",
        TESTS_DIR / "insurance",
        TESTS_DIR / "legal",
        TESTS_DIR / "market",
        TESTS_DIR / "market_data",
        TESTS_DIR / "marketplace",
        TESTS_DIR / "ml",
        TESTS_DIR / "monitoring",
        TESTS_DIR / "neo4j",
        TESTS_DIR / "news",
        TESTS_DIR / "ops",
        TESTS_DIR / "optimization",
        TESTS_DIR / "options",
        TESTS_DIR / "pe",
        TESTS_DIR / "philanthropy",
        TESTS_DIR / "planning",
        TESTS_DIR / "items", # Just in case
        TESTS_DIR / "portfolio",
        TESTS_DIR / "public_api",
        TESTS_DIR / "real_estate",
        TESTS_DIR / "reporting",
        TESTS_DIR / "research",
        TESTS_DIR / "retirement",
        TESTS_DIR / "risk",
        TESTS_DIR / "security",
        TESTS_DIR / "sfo",
        TESTS_DIR / "social_trading",
        TESTS_DIR / "strategy",
        TESTS_DIR / "system",
        TESTS_DIR / "tax",
        TESTS_DIR / "trading",
        TESTS_DIR / "treasury",
        TESTS_DIR / "trusts",
        TESTS_DIR / "utils",
        TESTS_DIR / "vc",
        TESTS_DIR / "watchlist",
        TESTS_DIR / "web",
        TESTS_DIR / "workspace"
    ],
    "web": [TESTS_DIR / "web"],
    "e2e": [TESTS_DIR / "e2e"],
    "load": [TESTS_DIR / "load"],
    "smoke": [TESTS_DIR / "smoke"],
    "system": [TESTS_DIR / "system"],
    "workspace": [TESTS_DIR / "workspace"]
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
    
    args = ["-v", "-s", "-p", "no:cacheprovider", "--tb=short"] # Detailed output, no capture to avoid I/O errors
    
    if category == "all":
        # Run everything in tests/ default recursion
        target_paths = [TESTS_DIR]
    elif category in TEST_MAPPING:
        # Filter for existing paths only
        all_paths = TEST_MAPPING[category]
        target_paths = [p for p in all_paths if p.exists()]
        
        if not target_paths:
            logger.warning(f"No valid test directories found for category: {category}")
            return 1
            
        # Log missing paths if any (for debugging)
        missing = [p for p in all_paths if not p.exists()]
        if missing:
            logger.debug(f"Skipping missing paths: {missing}")
            
    else:
        logger.error(f"Unknown test category: {category}")
        return 1
        
    for path in target_paths:
        args.append(str(path))
    
    import subprocess
    
    cmd = [sys.executable, "-m", "pytest"] + args
    
    print(f"\n🚀 Executing: {' '.join(cmd)}\n")
    
    try:
        # Run as a subprocess for better isolation and reliable collection
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        logger.error(f"Failed to run tests: {e}")
        return 1

def run_frontend_tests():
    """
    Run frontend tests using npm.
    """
    logger.info("Running frontend tests...")
    import subprocess
    import shutil
    
    # Check if npm is available
    if not shutil.which("npm"):
        logger.error("npm not found in PATH")
        sys.exit(1)
        
    frontend_dir = PROJECT_ROOT / "Frontend"
    
    if not frontend_dir.exists():
        logger.error(f"Frontend directory not found: {frontend_dir}")
        sys.exit(1)

    cmd = ["npm", "run", "test", "--", "--run"]
    # We add --run to force vitest to run once and exit, instead of watch mode
    # Assuming the package.json script is "vitest"
    
    print(f"\n🚀 Executing in {frontend_dir}: {' '.join(cmd)}\n")
    
    try:
        # Use shell=True for windows npm compatibility if needed, but shutil.which check helps
        # On windows, npm is usually npm.cmd
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        cmd[0] = npm_cmd
        
        result = subprocess.run(cmd, cwd=frontend_dir, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        logger.error(f"Failed to run frontend tests: {e}")
        sys.exit(1)

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

def run_schemas_tests():
    sys.exit(run_tests("schemas"))

def run_env_tests():
    """
    Run environment variable validation tests.
    """
    cmd = [sys.executable, "-m", "pytest", "-v", str(TESTS_DIR / "system" / "test_env_vars.py")]
    print(f"\n🚀 Executing: {' '.join(cmd)}\n")
    import subprocess
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        logger.error(f"Failed to run env tests: {e}")
        sys.exit(1)

def run_billing_tests():
    sys.exit(run_tests("billing"))

def run_web_tests():
    sys.exit(run_tests("web"))

def run_e2e_tests():
    sys.exit(run_tests("e2e"))

def run_load_tests():
    sys.exit(run_tests("load"))

def run_smoke_tests():
    sys.exit(run_tests("smoke"))

def run_system_tests():
    sys.exit(run_tests("system"))

if __name__ == "__main__":
    # verification run
    run_tests("all")
