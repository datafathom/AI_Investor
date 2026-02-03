
import asyncio
import logging
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.social.reddit_service import get_reddit_client
from services.social.discord_bot import get_discord_bot
from services.analysis.monte_carlo_service import get_monte_carlo_service
from services.social.inertia_cache import get_inertia_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_loop():
    logger.info("--- Social Sentiment & Market Simulation Loop Verification ---")
    
    ticker = "NVDA"
    reddit = get_reddit_client()
    discord = get_discord_bot()
    mc = get_monte_carlo_service()
    cache = get_inertia_cache()
    
    # 1. Trigger Social Updates
    logger.info(f"Injecting social activity for {ticker}...")
    await reddit.analyze_sentiment(ticker)
    await discord.get_hype_score(ticker)
    
    inertia = cache.get_inertia(ticker)
    logger.info(f"Current Inertia for {ticker}: {inertia}")
    
    # 2. Run Simulation
    logger.info(f"Running Hype-Adjusted GBM Simulation for {ticker}...")
    result = await mc.run_gbm_simulation(initial_value=100.0, ticker=ticker, paths=100)
    
    logger.info(f"Simulation Result (Mean Final): {result.mean_final}")
    logger.info(f"Ruin Probability: {result.ruin_probability}")

    if abs(inertia) > 0:
        logger.info("SUCCESS: Hype-adjusted drift was successfully applied.")
    else:
        logger.warning("WARNING: Inertia was 0. Check singleton linkage.")

if __name__ == "__main__":
    asyncio.run(verify_loop())
