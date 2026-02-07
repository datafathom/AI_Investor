import os
import asyncio
import time
import sys
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv

# Load environment variables (Bot Token)
load_dotenv()

async def nuke_channel(channel_id: str):
    """
    Deletes all messages in a specific Slack channel concurrently.
    Optimized for speed while respecting Slack rate limits.
    """
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print("❌ Error: SLACK_BOT_TOKEN not found in environment.")
        return

    # Use Bot Token or User Token if available
    user_token = os.environ.get("SLACK_USER_TOKEN")
    if user_token:
        print("💡 Found SLACK_USER_TOKEN. Using this to allow deleting messages from other users!")
        client = AsyncWebClient(token=user_token)
    else:
        print("ℹ️ Using Bot Token. Note: Bots can usually only delete their own messages.")
        client = AsyncWebClient(token=token)
    
    # Verification Ping
    try:
        auth = await client.auth_test()
        print(f"🤖 Authenticated as: {auth['user']} (ID: {auth['user_id']})")
    except Exception as e:
        print(f"❌ Auth Error: {e}")
        return

    print(f"🚀 Starting HIGH-SPEED PURGE of channel: {channel_id}")
    
    async def _delete_msg(ts):
        """Helper to delete a single message with rate-limit retry."""
        retry_count = 0
        while retry_count < 3:
            try:
                res = await client.chat_delete(channel=channel_id, ts=ts)
                if res.get("ok"):
                    return True
                
                error = res.get("error")
                if error == "ratelimited":
                    wait_time = int(res.headers.get("Retry-After", 5))
                    print(f"⏳ Rate limited. Sleeping for {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    retry_count += 1
                    continue
                
                if error == "message_not_found":
                    return True # Already deleted
                    
                if error == "cant_delete_message":
                    # This happens when a Bot tries to delete a Human's message
                    return False 
                    
                print(f"⚠️ Slack Error deleting {ts}: {error}")
                return False
            except Exception as e:
                print(f"⚠️ Exception deleting {ts}: {e}")
                return False
        return False

    total_purged = 0
    total_found = 0
    cursor = None
    while True:
        try:
            # 1. Fetch messages using cursor for pagination
            response = await client.conversations_history(channel=channel_id, limit=100, cursor=cursor)
            if not response.get("ok"):
                print(f"❌ Error fetching history: {response.get('error')}")
                break
                
            messages = response.get("messages", [])
            if not messages:
                print("✨ No more messages found.")
                break
            
            total_found += len(messages)
            ts_list = [m["ts"] for m in messages if "ts" in m]
            if not ts_list:
                # Move to next page if no deletable TS found in this batch
                cursor = response.get("response_metadata", {}).get("next_cursor")
                if not cursor: break
                continue

            print(f"🧹 Scanning batch of {len(ts_list)} messages...")
            
            # Execute batch concurrently
            results = await asyncio.gather(*[_delete_msg(ts) for ts in ts_list])
            purged_in_batch = sum(1 for r in results if r)
            total_purged += purged_in_batch
            
            print(f"✅ Purged {total_purged}/{total_found} messages scanned so far...")
            
            # Update cursor
            cursor = response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
                
            # Respectful pause
            await asyncio.sleep(0.2)
                    
        except Exception as e:
            print(f"❌ Loop Error: {e}")
            break

    print(f"🏁 Summary: Total found={total_found}, Total purged={total_purged}")

if __name__ == "__main__":
    channel = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SLACK_CHANNEL_ID")
    if not channel:
        print("❌ Error: No Channel ID provided.")
    else:
        asyncio.run(nuke_channel(channel))
