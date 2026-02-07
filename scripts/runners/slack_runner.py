"""
==============================================================================
FILE: scripts/runners/slack_runner.py
ROLE: CLI Runner for Slack Operations
PURPOSE: Handles CLI commands for sending notifications and running the bot.
==============================================================================
"""

import asyncio
import logging
from services.notifications.slack_service import get_slack_service

logger = logging.getLogger(__name__)

def send_notification(message: str, level: str = "info"):
    """
    CLI Handler: Sends a simple notification message.
    Args:
        message (str): The text message to send.
        level (str): Severity level (info, success, warning, critical)
    """
    service = get_slack_service()
    
    async def _run():
        response = await service.send_notification(text=message, level=level)
        if response.get("ok"):
            print(f"✅ Notification sent ({level.upper()})")
        else:
            print(f"❌ Failed to send notification: {response.get('error')}")

    asyncio.run(_run())

def notify_complete(task: str, summary: str):
    """
    CLI Handler: Sends a task completion alert.
    Args:
        task (str): Name of the completed task.
        summary (str): Brief summary of what was accomplished.
    """
    service = get_slack_service()
    
    # Format the message for a nice rich text block look
    formatted_message = (
        f"*✅ Task Completed: {task}*\n"
        f"--------------------------------------------------\n"
        f"{summary}\n"
        f"--------------------------------------------------"
    )

    async def _run():
        response = await service.send_notification(text=formatted_message, level="success")
        if response.get("ok"):
            print(f"✅ Completion alert sent for task: {task}")
        else:
            print(f"❌ Failed to send completion alert: {response.get('error')}")

    asyncio.run(_run())

def request_human_input(prompt: str, context: str = ""):
    """
    CLI Handler: Sends a request for human input.
    Args:
        prompt (str): The question or action required.
        context (str): Additional context or background info.
    """
    service = get_slack_service()
    
    formatted_message = (
        f"*✋ Human Input Required*\n"
        f"--------------------------------------------------\n"
        f"*{prompt}*\n"
        f"_{context}_\n"
        f"--------------------------------------------------"
    )

    async def _run():
        # Using 'warning' level (gold color) for input requests
        response = await service.send_notification(text=formatted_message, level="warning")
        if response.get("ok"):
            print(f"✅ Input request sent: {prompt}")
        else:
            print(f"❌ Failed to send input request: {response.get('error')}")

    asyncio.run(_run())


def stop_bot(silent: bool = False):
    """
    CLI Handler: Stops the Slack bot background process.
    Uses wmic to find python processes with 'slack start' in the command line.
    """
    import subprocess
    import os
    
    if not silent:
        print("search for running Slack Bot processes...")
    
    try:
        # WMIC query to find python processes with 'slack' and 'start' in command line
        # This avoids killing the current process if it was just 'python cli.py slack stop'
        # but we need to be careful not to kill ourselves if we match the query too broadly.
        # 'wmic process where "name=\'python.exe\' and commandline like \'%slack%start%\'" get processid'
        
        cmd = 'wmic process where "name=\'python.exe\' and commandline like \'%slack%start%\'" get processid'
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        
        if result.returncode != 0:
            if not silent:
                print("No running bot processes found (WMIC check failed).")
            return

        pids = [line.strip() for line in result.stdout.split('\n') if line.strip().isdigit()]
        
        # Filter out current process just in case
        current_pid = str(os.getpid())
        target_pids = [p for p in pids if p != current_pid]
        
        if not target_pids:
            if not silent:
                print("❌ No active 'slack start' processes found.")
            return

        if not silent:
            print(f"🔪 Found {len(target_pids)} process(es). Terminating...")
        
        for pid in target_pids:
            try:
                if not silent:
                    print(f"   - Killing PID {pid}...", end=" ")
                # taskkill /F /PID <pid>
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, stderr=subprocess.DEVNULL)
                if not silent:
                    print("✅")
            except Exception as e:
                if not silent:
                    print(f"❌ Error: {e}")
                
        if not silent:
            print("\n✅ Slack Bot stopped successfully.")
        
    except Exception as e:
        print(f"❌ Failed to stop bot: {e}")


def start_bot():
    """
    CLI Handler: Starts the Slack bot listener (Socket Mode).
    Integrated with Catch-up logic and Job Dispatch.
    """
    print("🚀 Starting AI Investor Bot (Socket Mode)...")
    service = get_slack_service()
    
    if not service.bot:
        print("❌ Bot not initialized. Check SLACK_BOT_TOKEN and SLACK_SOCKET_TOKEN.")
        return

    print("📡 Bot is listening for '!job', 'ping', and @mentions...")
    
    try:
        asyncio.run(service.start_bot())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user.")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
