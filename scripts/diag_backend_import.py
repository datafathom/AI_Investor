
import time
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Diagnostic")

logger.info("Starting diagnostic import of web.fastapi_gateway...")
start = time.time()

try:
    from web.fastapi_gateway import app
    logger.info(f"✅ Success: 'app' imported in {time.time() - start:.2f}s")
except Exception as e:
    logger.error(f"❌ Failed to import 'app': {e}")
    sys.exit(1)

logger.info("Importing uvicorn...")
import uvicorn

logger.info("Diagnostic complete.")
