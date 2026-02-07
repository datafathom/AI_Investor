# Backend Service: Social (The Crowd Radar)

## Overview
The **Social Service** monitors online communities for trading sentiment and ticker mentions. It scrapes Discord, Reddit, StockTwits, Facebook, and YouTube to quantify "hype" and detect emerging momentum plays before they hit mainstream news.

## Core Components

### 1. Discord Bot (`discord_bot.py`)
- **Channel Monitoring**: Listens to configurable channels for ticker mentions.
- **Hype Scoring**: Calculates velocity (mentions/hour) and growth percentage.
- **Sentiment Tagging**: Labels messages as Bullish/Bearish/Neutral.

### 2. StockTwits Client (`stocktwits_client.py`)
- Fetches message streams and sentiment ratios for tickers.

### 3. Reddit Service (`reddit_service.py`)
- Monitors subreddits like r/wallstreetbets for unusual activity.

### Other Modules
- `facebook_hype_service.py`: Tracks public investment groups.
- `youtube_client.py`: Monitors financial YouTuber mentions.
- `inertia_cache.py`: Shared cache for cross-platform sentiment aggregation.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Social Sentiment** | Discord Feed | `discord_bot.get_recent_mentions()` | **Implemented** (`StockTwitsFeed.jsx`) |
| **Community Dashboard** | Hype Leaderboard | `discord_bot.get_hype_score()` | **Partially Implemented** |

## Usage Example

```python
from services.social.discord_bot import get_discord_bot
import asyncio

bot = get_discord_bot()

async def main():
    await bot.connect()
    mentions = await bot.get_recent_mentions("NVDA")
    for msg in mentions:
        print(f"[{msg['channel']}] {msg['author']}: {msg['content']}")

asyncio.run(main())
```
