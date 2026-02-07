import asyncio
import os
import time
from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

async def toggle_presence():
    load_dotenv()
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN missing")
        return

    client = AsyncWebClient(token=bot_token)
    
    # Get Bot Info
    auth = await client.auth_test()
    bot_id = auth["user_id"]
    print(f"🤖 Bot ID: {bot_id}")
    print(f"👀 Please watch the Bot '{auth['user']}' in your Slack Sidebar (under Apps)...")

    # Toggle Loop
    for i in range(6):
        state = "auto" if i % 2 == 0 else "away"
        icon = "🟢" if state == "auto" else "⚪"
        
        print(f"[{i+1}/6] Setting presence to: {state.upper()} {icon}")
        try:
            # Try Bot Token first (proved to work in diagnostics)
            res = await client.users_setPresence(presence=state)
            if not res["ok"]:
                print(f"   ⚠️ Failed: {res['error']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        await asyncio.sleep(5)

    print("🏁 Toggle test complete. Did you see it blink?")

if __name__ == "__main__":
    asyncio.run(toggle_presence())
