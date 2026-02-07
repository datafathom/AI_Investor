import asyncio
import os
import json
import re
import logging
from unittest.mock import AsyncMock, MagicMock, patch

# Configure logging to see output during test
logging.basicConfig(level=logging.INFO)

async def verify_slack_integration():
    print("\n--- Starting Slack Bot Verification ---\n")
    
    # Mock environment
    os.environ["SLACK_BOT_TOKEN"] = "xoxb-mock-token"
    os.environ["SLACK_SOCKET_TOKEN"] = "xapp-mock-token"
    os.environ["SLACK_ALLOWED_USERS"] = "USER_A,USER_B"
    os.environ["SLACK_CHANNEL_ID"] = "C12345"

    from services.notifications.slack_service import SlackService
    
    # 1. Test Initialization & Security Setup
    service = SlackService(mock=False)
    print(f"✅ Service Initialized. Allowed users: {service.allowed_users}")
    assert "USER_A" in service.allowed_users
    
    # 2. Test Security Middleware (Mocking Bolt Payload)
    next_called = False
    async def mock_next():
        nonlocal next_called
        next_called = True

    # Middleware is stored in service.bot._middleware_list or similar in Bolt
    # But we can test the logic directly if we extract it or wrap the call.
    # Since Bolt handles it internally, we'll mock the app invocation.
    
    # 3. Test State Persistence
    test_ts = "1700000000.123456"
    service._save_state(test_ts)
    loaded_ts = service._load_state()
    print(f"✅ State Persistence: Saved {test_ts}, Loaded {loaded_ts}")
    assert loaded_ts == test_ts
    
    # 4. Test Structured Job Dispatch Logic (Mocking Producer)
    service.producer = AsyncMock()
    service.producer.publish_job_request.return_value = True
    
    # 4.1 Valid Subcommand: run-assessment
    mock_say = AsyncMock()
    mock_message = {'text': '!job run-assessment --ticker AAPL', 'user': 'USER_A', 'channel': 'C12345', 'ts': '1700000001.000000'}
    mock_context = {
        'matches': ('run-assessment', '--ticker AAPL'),
        # We simulate the case where 'match' object is missing from context
        # to test our robust local re-match logic.
    }
    job_cfg = service.config['commands']['job']
    
    print("✅ Testing Valid Subcommand (run-assessment) via local re-match...")
    await service._handle_dynamic_command(job_cfg, mock_message, mock_say, mock_context)
    
    # Should resolve "engine assessment --ticker AAPL" from template "engine assessment {args}"
    service.producer.publish_job_request.assert_awaited_with(
        command='engine assessment --ticker AAPL',
        user_id='USER_A',
        channel_id='C12345'
    )
    print("✅ Local re-match verified: Subcommand and args correctly extracted.")

    # 4.1.1 Case-Insensitive Subcommand: Analyze
    mock_say.reset_mock()
    mock_message_caps = {'text': '!job Analyze NVDA', 'user': 'USER_A', 'channel': 'C12345', 'ts': '1700000002.000000'}
    mock_context_caps = {
        'matches': ('Analyze', 'NVDA'),
    }
    print("✅ Testing Case-Insensitive Subcommand (Analyze vs analyze) via local re-match...")
    await service._handle_dynamic_command(job_cfg, mock_message_caps, mock_say, mock_context_caps)
    # Should resolve "research analyze NVDA" from template "research analyze {args}"
    service.producer.publish_job_request.assert_awaited_with(
        command='research analyze NVDA',
        user_id='USER_A',
        channel_id='C12345'
    )
    print("✅ Case-Insensitivity verified: 'Analyze' correctly mapped to 'analyze'.")

    # 4.2 Invalid Subcommand: bogus-job
    mock_say.reset_mock()
    mock_context_invalid = {
        'matches': ['bogus-job', ''],
        'match': re.match(r"^!job\s+(?P<subcommand>[\w-]+)(?:\s+(?P<args>.*))?$", "!job bogus-job")
    }
    print("✅ Testing Invalid Subcommand (bogus-job)...")
    await service._handle_dynamic_command(job_cfg, mock_message, mock_say, mock_context_invalid)
    
    # Should reply with unknown job message and suggesting valid ones
    last_reply = mock_say.call_args[0][0]
    assert "Unknown Job" in last_reply
    assert "run-assessment" in last_reply
    print("✅ Invalid Subcommand verified: Validation error returned.")

    # 4.5 Test Simple Reply Action
    ping_cfg = service.config['commands']['ping']
    await service._handle_dynamic_command(ping_cfg, mock_message, mock_say, {'matches': ['ping']})
    mock_say.assert_called_with(ping_cfg['reply_text'])
    print("✅ Simple Reply verified: Ping responded correctly.")

    # 4.6 Test Help Command
    help_cfg = service.config['commands']['help']
    await service._handle_dynamic_command(help_cfg, mock_message, mock_say, {'matches': ['!help']})
    # Check if the help message contains known command names
    help_text = mock_say.call_args[0][0]
    assert "*ping*" in help_text
    assert "*job*" in help_text
    assert "Example:" in help_text
    print("✅ Help Command verified: Formatted list of commands and examples returned.")

    # 4.7 Test Integrated Data Commands (Service Calls)
    print("✅ Testing Integrated Data Commands...")
    
    # Mock health summary
    with patch.object(service, 'get_system_health_summary', return_value="🖥️ *System Health Summary* - Online"):
        health_cfg = service.config['commands']['health']
        await service._handle_dynamic_command(health_cfg, mock_message, mock_say, {'matches': ['!health']})
        mock_say.assert_called_with("🖥️ *System Health Summary* - Online")
    
    # Mock risk summary
    with patch.object(service, 'get_risk_summary', return_value="⚖️ *Risk Monitor Summary* - ✅ ACTIVE"):
        risk_cfg = service.config['commands']['risk']
        await service._handle_dynamic_command(risk_cfg, mock_message, mock_say, {'matches': ['!risk']})
        mock_say.assert_called_with("⚖️ *Risk Monitor Summary* - ✅ ACTIVE")

    print("✅ Service Calls verified: Health and Risk data fetched correctly.")

    # 4.8 Test Ticker Normalization (Universal Case-Insensitivity)
    print("✅ Testing Ticker Normalization...")
    
    # Standalone shortcut: !analyze aapl -> research analyze AAPL
    analyze_cfg = service.config['commands']['analyze']
    mock_context_norm = {
        'matches': ['aapl'],
        'match': re.match(r"^!analyze\s+(?P<ticker>[a-zA-Z]+)\s*$", "!analyze aapl")
    }
    await service._handle_dynamic_command(analyze_cfg, mock_message, mock_say, mock_context_norm)
    service.producer.publish_job_request.assert_awaited_with(
        command='research analyze AAPL',
        user_id='USER_A',
        channel_id='C12345'
    )
    print("✅ Standalone Normalization verified: 'aapl' -> 'AAPL'.")

    # 5. Test Catch-up Logic (Regex Based)
    service.bot.client.conversations_history = AsyncMock(return_value={
        "ok": True,
        "messages": [
            {"ts": "1700000005.000000", "user": "USER_A", "text": "!job test-missed"},
            {"ts": "1700000006.000000", "user": "USER_B", "text": "random talk"},
            {"ts": "1700000007.000000", "user": "USER_A", "text": "ping"}
        ]
    })
    
    print("✅ Testing Catch-up Logic (Scanning patterns)...")
    await service.process_missed_messages("C12345")
    # State should be updated to the latest ts
    assert service.last_processed_ts == "1700000007.000000"
    print(f"✅ Catch-up verified. Latest TS: {service.last_processed_ts}")

    print("\n--- Verification Successful! ---\n")
    
    # Cleanup
    if os.path.exists(".slack_bot_state"):
        os.remove(".slack_bot_state")

if __name__ == "__main__":
    asyncio.run(verify_slack_integration())
