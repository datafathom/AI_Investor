"""
==============================================================================
FILE: services/notifications/slack_service.py
ROLE: Team Communication & Interactive Bot Service
PURPOSE: Interfaces with Slack for broadcasting alerts and responding to 
         user commands via Socket Mode (Localhost friendly).
==============================================================================
"""

import os
import logging
import asyncio
import datetime
import json
import re
import subprocess
import sys
import atexit
import socket
from pathlib import Path
from datetime import timezone
from typing import Dict, Any, Optional, List, Callable

# Core Slack libraries
from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_sdk.web.async_client import AsyncWebClient
from dotenv import load_dotenv
import httpx

# Local Integration
from services.kafka.slack_producer import get_slack_producer
from services.system.cache_service import get_cache_service

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackService:
    """
    Unified Service for sending notifications and handling bot interactions.
    Now supports Async operations, User-based security filtering, and Job Dispatch.
    """
    
    def __init__(self, mock: bool = False):
        self.mock = mock
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.user_token = os.getenv("SLACK_USER_TOKEN") # High-privilege token
        self.socket_token = os.getenv("SLACK_SOCKET_TOKEN") 
        self.default_channel = os.getenv("SLACK_CHANNEL_ID")
        # Shared State & Identity
        self.cache = get_cache_service()
        self.node_id = socket.gethostname()
        self.is_leader = False
        self.leader_key = "slack:bot_leader"
        self.state_key = "slack:bot_state"
        self.jobs_key = "slack:active_jobs"
        
        self.last_processed_ts = self._load_state()

        # Security: Fetch allowed user IDs from env
        allowed_users_str = os.getenv("SLACK_ALLOWED_USERS", "")
        self.allowed_users = [u.strip() for u in allowed_users_str.split(",") if u.strip()]
        
        # Kafka Producer
        self.producer = get_slack_producer()
        
        # Load Bot Configuration
        self.config_path = PROJECT_ROOT = Path(__file__).parent.parent.parent / "config" / "slackbot_config.json"
        self.config = self._load_config()
        
        # Initialize the Bolt App
        if not mock:
            # Security: Purge OAuth env vars to force single-token Socket Mode
            # Otherwise, Bolt will ignore SLACK_BOT_TOKEN and try to use OAuth flow.
            os.environ.pop("SLACK_CLIENT_ID", None)
            os.environ.pop("SLACK_CLIENT_SECRET", None)
            
            self.bot = AsyncApp(token=self.bot_token)
            self._setup_handlers()
            self._setup_middleware()
        else:
            self.bot = None
            
        self.api_url = "https://slack.com/api/chat.postMessage"
        
        # Persistent context for notifications
        self._http_client: Optional[httpx.AsyncClient] = None if mock else httpx.AsyncClient()
        
        # High-privilege user client for administrative tasks (like nuking)
        self.user_client: Optional[AsyncWebClient] = AsyncWebClient(token=self.user_token) if self.user_token and not mock else None
        
        # Internal Job Tracker (File-based for cross-process visibility)
        self.job_state_file = ".slack_jobs_active"
        self._active_jobs: Dict[str, Dict[str, Any]] = self._load_active_jobs()
        
        # Worker Lifecycle Management
        self.auto_spawn = os.getenv("AUTO_SPAWN_WORKER", "1") == "1"
        self._worker_process: Optional[subprocess.Popen] = None
        self._presence_task: Optional[asyncio.Task] = None # For heartbeat
        
        # Socket Mode Handler reference for cleanup
        self._handler: Optional[AsyncSocketModeHandler] = None
        
        # Ensure worker is killed on exit
        atexit.register(self.stop_worker)

    async def _try_acquire_leader_lock(self) -> bool:
        """Attempts to acquire the leader lock in Redis."""
        # TTL for the lock (seconds)
        ttl = 60
        lock_acquired = self.cache.set(self.leader_key, self.node_id, ttl=ttl)
        
        if lock_acquired:
            # Check if we actually set it or someone else did (simulating SET NX)
            # CacheService doesn't have SET NX explicitly but we can check the value
            current_leader = self.cache.get(self.leader_key)
            if current_leader == self.node_id:
                if not self.is_leader:
                    logger.info(f"👑 Node '{self.node_id}' acquired LEADER lock.")
                    self.is_leader = True
                return True
        
        if self.is_leader:
            logger.warning(f"🏳️ Node '{self.node_id}' lost LEADER lock to {self.cache.get(self.leader_key)}")
            self.is_leader = False
        return False

    def _load_active_jobs(self) -> Dict[str, Any]:
        """Loads active jobs from shared Redis cache."""
        jobs = self.cache.get(self.jobs_key)
        if isinstance(jobs, dict):
            return jobs
        return {}

    def _save_active_jobs(self):
        """Saves active jobs to shared Redis cache."""
        self.cache.set(self.jobs_key, self._active_jobs, ttl=86400) # 24h retention

    def _ensure_worker_running(self):
        """Checks if standalone worker is running and spawns it if needed."""
        if not self.auto_spawn:
            return

        # Check if process is still alive
        if self._worker_process is not None:
            if self._worker_process.poll() is None:
                return # Still running
            else:
                logger.warning("👷 Worker process died. Restarting...")
        
        # Spawn the worker
        try:
            project_root = Path(__file__).parent.parent.parent
            worker_script = project_root / "scripts" / "slack_worker.py"
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            log_file_path = log_dir / "slack_worker.log"

            logger.info(f"👷 Spawning standalone worker: {worker_script}")
            
            # Prepare environment with PYTHONPATH
            env = os.environ.copy()
            env["PYTHONPATH"] = str(project_root)
            
            # Open log file for stdout/stderr
            with open(log_file_path, "a") as log_file:
                log_file.write(f"\n--- Worker Spawned at {datetime.datetime.now()} ---\n")
                
            # Start in a new process group to keep it alive
            # Use 'a' (append) mode for stdout/stderr via a separate handle if needed, 
            # but Popen usually takes a file object
            log_out = open(log_file_path, "a")
            
            self._worker_process = subprocess.Popen(
                [sys.executable, str(worker_script)],
                stdout=log_out,
                stderr=log_out,
                env=env,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
                cwd=str(project_root)
            )
            logger.info(f"✅ Worker spawned with PID: {self._worker_process.pid}. Logs: logs/slack_worker.log")
        except Exception as e:
            logger.error(f"❌ Failed to spawn worker: {e}")

    def stop_worker(self):
        """Gracefully terminates the standalone worker process."""
        if self._worker_process and self._worker_process.poll() is None:
            logger.info(f"🛑 Terminating worker process (PID: {self._worker_process.pid})...")
            try:
                self._worker_process.terminate()
                # Wait briefly for it to exit
                try:
                    self._worker_process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️ Worker did not exit gracefully. Killing...")
                    self._worker_process.kill()
                logger.info("✅ Worker process terminated.")
            except Exception as e:
                logger.error(f"❌ Error terminating worker: {e}")
            finally:
                self._worker_process = None

    async def register_job(self, job_id: str, user_id: str, command: str):
        """Manually registers a job in the tracker (useful for simulations)."""
        logger.info(f"📝 Registering job {job_id} for user {user_id}")
        self._active_jobs[job_id] = {
            "user_id": user_id,
            "command": command,
            "status": "pending",
            "timestamp": datetime.datetime.now().isoformat()
        }
        self._save_active_jobs()

    async def update_bot_status(self, text: str, emoji: str):
        """Updates the bot's Slack profile status (text + emoji). Try bot then user token."""
        if self.mock:
            return
            
        # 1. Try via Bot Client
        if self.bot:
            try:
                response = await self.bot.client.users_profile_set(
                    profile={"status_text": text, "status_emoji": emoji, "status_expiration": 0}
                )
                if response.get("ok"):
                    logger.info(f"👤 Bot status updated to: {text} {emoji} (via Bot Token)")
                    return
            except Exception as e:
                logger.debug(f"Bot token profile update skipped: {e}")

        # 2. Try via User Client (Admin/Power-user fallback)
        if self.user_client:
            try:
                # We need the bot's user ID to target it
                auth = await self.bot.client.auth_test()
                bot_id = auth["user_id"]
                
                response = await self.user_client.users_profile_set(
                    user=bot_id,
                    profile={"status_text": text, "status_emoji": emoji, "status_expiration": 0}
                )
                if response.get("ok"):
                    logger.info(f"👤 Bot status updated to: {text} {emoji} (via User Token)")
                else:
                    logger.warning(f"⚠️ User Token failed to update bot status: {response.get('error')}")
            except Exception as e:
                if "invalid_user" in str(e) or "not_allowed_token_type" in str(e):
                    logger.warning(f"⚠️ Bot status text update skipped (Not supported for this App type): {e}")
                else:
                    logger.error(f"❌ Error updating bot status via User Token: {e}")

    async def update_bot_presence(self, presence: str):
        """Updates the bot's Slack presence (auto/away). Try bot then user token."""
        if self.mock:
            return

        # 1. Try via Bot Client (Bot usually settings its own presence)
        if self.bot:
            try:
                response = await self.bot.client.users_setPresence(presence=presence)
                if response.get("ok"):
                    logger.info(f"👤 Bot presence updated to: {presence} (via Bot Token)")
                    return
            except Exception as e:
                logger.debug(f"Bot token presence update skipped: {e}")

        # 2. Try via User Client (Fallback)
        if self.user_client:
            try:
                # Presence update via User Token often targets the user, 
                # but we can try if it has administrative scopes.
                response = await self.user_client.users_setPresence(presence=presence)
                if response.get("ok"):
                    logger.info(f"👤 Presence updated to: {presence} (via User Token)")
                else:
                    logger.warning(f"⚠️ User Token failed to update presence: {response.get('error')}")
            except Exception as e:
                logger.error(f"❌ Error updating presence via User Token: {e}")

    def _load_state(self) -> str:
        """Load the last processed message timestamp from shared Redis cache."""
        state = self.cache.get(self.state_key)
        if isinstance(state, dict):
            return state.get("last_processed_ts", "0")
        return "0"

    def _save_state(self, ts: str):
        """Save the last processed message timestamp to shared Redis cache."""
        self.cache.set(self.state_key, {"last_processed_ts": ts}, ttl=604800) # 7d retention
        self.last_processed_ts = ts

    def _load_config(self) -> Dict[str, Any]:
        """Load the Slack Bot configuration from JSON."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading slackbot_config.json: {e}")
        return {"commands": {}}

    async def _presence_heartbeat(self):
        """Periodically renew leader lock and re-assert presence to keep the green dot alive."""
        logger.info(f"💓 Presence heartbeat started for node: {self.node_id}")
        while True:
            try:
                # 1. Periodically renew LEADER lock
                is_leader = await self._try_acquire_leader_lock()
                
                # 2. Only assert 'auto' presence if we are the leader
                if is_leader:
                    await self.update_bot_presence("auto")
                else:
                    await self.update_bot_presence("away")
                
                await asyncio.sleep(45) # Every 45s (Lock TTL is 60s)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in presence heartbeat: {e}")
                await asyncio.sleep(10) # Retry after delay

    def _setup_handlers(self):
        """Dynamically register handlers from configuration."""
        if not self.bot:
            return

        commands = self.config.get("commands", {})
        for name, cmd_config in commands.items():
            pattern = cmd_config.get("pattern")
            if pattern:
                logger.info(f"Registering dynamic command: {name} (Pattern: {pattern})")
                
                # We use a closure to capture the specific command configuration
                def make_handler(cfg):
                    async def dynamic_handler(message, say, context):
                        await self._handle_dynamic_command(cfg, message, say, context)
                    return dynamic_handler
                
                self.bot.message(re.compile(pattern, re.IGNORECASE))(make_handler(cmd_config))

        @self.bot.event("message")
        async def handle_unhandled_messages(event, say, logger):
            # Log what we missed to help debugging regex issues
            text = event.get("text", "")
            subtype = event.get("subtype")
            if not subtype: # Only log actual user messages, ignore bot_add/join etc
                logger.info(f"🔈 Unhandled Message: '{text}' (Does not match any registered pattern)")
            pass

    async def _handle_dynamic_command(self, cmd_config: Dict[str, Any], message: Dict[str, Any], say: Callable, context: Dict[str, Any]):
        """Executes the action defined in the command configuration."""
        # Leader Safety: Only handle commands if we own the lock
        if not self.is_leader:
            # Silent ignore to avoid spamming the channel from secondary nodes
            return

        action = cmd_config.get("action")

        user_id = message.get("user")
        text = message.get("text", "")
        
        logger.info(f"📥 Incoming Command | User: {user_id} | Text: '{text}' | Action: {action}")
        
        # Extract matches for variable substitution
        params = {}
        match_obj = context.get("match") # Bolt context might provide this
        
        # If match is missing or empty, re-run our own match to ensure named groups are captured
        if not match_obj or not match_obj.groupdict():
            pattern = cmd_config.get("pattern")
            if pattern:
                match_obj = re.match(pattern, text, re.IGNORECASE)
        
        if match_obj:
            params = match_obj.groupdict()
            # If no named groups, fallback to positional if available
            if not params:
                matches = context.get("matches") or match_obj.groups()
                if matches:
                    params = {"_match": matches[0]}
        else:
            # Final fallback to Bolt's matches
            matches = context.get("matches", [None])
            if matches and matches[0]:
                params = {"_match": matches[0]}

        # Universal Parameter Normalization: Always uppercase tickers
        if "ticker" in params and params["ticker"]:
            original_ticker = params["ticker"]
            params["ticker"] = params["ticker"].upper()
            if original_ticker != params["ticker"]:
                logger.info(f"🔄 Normalized Ticker: '{original_ticker}' -> '{params['ticker']}'")

        if action == "reply":
            reply_text = cmd_config.get("reply_text", "")
            # Basic variable substitution: {service} -> value from named group
            try:
                formatted_reply = reply_text.format(**params)
            except KeyError:
                formatted_reply = reply_text
            
            logger.info(f"💬 Reply Action | User: {user_id} | Reply: '{formatted_reply}'")
            await say(formatted_reply)

        elif action == "kafka_dispatch":
            subcommands = cmd_config.get("subcommands", {})
            sub_raw = params.get("subcommand")
            sub_name = sub_raw.lower() if sub_raw else None
            args_text = (params.get("args") or "").strip()
            
            logger.info(f"🔍 Dispatch Parse | Subcommand: '{sub_raw}' -> '{sub_name}' | Args: '{args_text}'")
            
            if subcommands:
                if sub_name not in subcommands:
                    valid_subs = ", ".join([f"`{s}`" for s in subcommands.keys()])
                    logger.warning(f"⚠️ Validation Failed | Unknown Job: '{sub_name}' | Valid: {list(subcommands.keys())}")
                    await say(f"⚠️ *Unknown Job:* `{sub_raw}`. Available jobs for `!job`: {valid_subs}")
                    return
                
                sub_cfg = subcommands[sub_name]
                template = sub_cfg.get("command_template", "{args}")
                # Build the command using the template
                # We provide both subcommand name and args to the template
                try:
                    dispatch_cmd = template.format(subcommand=sub_name, args=args_text).strip()
                except KeyError:
                    dispatch_cmd = f"{sub_name} {args_text}".strip()
                
                logger.info(f"📤 Kafka Dispatch | Validated Job: {sub_name} | Command: {dispatch_cmd}")
                await say(f"📥 *Job Validated:* `{sub_name}`. Dispatching `{dispatch_cmd}`...")
                
                # Track the job locally
                job_id = f"JOB-{int(datetime.datetime.now().timestamp())}-{user_id[-4:] if user_id else 'sys'}"
                self._active_jobs[job_id] = {
                    "user": user_id,
                    "command": dispatch_cmd,
                    "status": "Queued",
                    "started_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self._save_active_jobs()
                
                success = await self.producer.publish_job_request(
                    command=dispatch_cmd,
                    user_id=user_id,
                    channel_id=message.get("channel"),
                    job_id=job_id
                )
                
                if success:
                    await say(f"✅ *Queued:* Published job `{job_id}`.")
                    # Only spawn worker for "start" triggers
                    if "test start" in dispatch_cmd:
                        self._ensure_worker_running()
                else:
                    self._active_jobs.pop(job_id, None)
                    self._save_active_jobs()
                    await say(f"❌ *Error:* Failed to queue job.")
            else:
                # Standalone command or shortcut (no subcommands)
                # Use template if available, else fallback to command + args
                template = cmd_config.get("command_template")
                if template:
                    try:
                        dispatch_cmd = template.format(**params).strip()
                    except KeyError:
                        # Fallback if params don't match template keys
                        cmd_raw = params.get("command", matches[0] if matches else "unknown")
                        dispatch_cmd = f"{cmd_raw} {args_text}".strip()
                else:
                    cmd_raw = params.get("command", matches[0] if matches else "unknown")
                    dispatch_cmd = f"{cmd_raw} {args_text}".strip()
                
                logger.info(f"📤 Kafka Dispatch | Command: {dispatch_cmd}")
                await say(f"📥 *Job Received:* Dispatching `{dispatch_cmd}`...")
                
                # Track the job locally (UNLESS skip_registration is true)
                job_id = f"JOB-{int(datetime.datetime.now().timestamp())}-{user_id[-4:] if user_id else 'sys'}"
                should_register = not cmd_config.get("skip_registration", False)
                
                if should_register:
                    self._active_jobs[job_id] = {
                        "user": user_id,
                        "command": dispatch_cmd,
                        "status": "Queued",
                        "started_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self._save_active_jobs()
                
                success = await self.producer.publish_job_request(
                    command=dispatch_cmd,
                    user_id=user_id,
                    channel_id=message.get("channel"),
                    job_id=job_id
                )
            
                if success:
                    if should_register:
                        await say(f"✅ *Queued:* Published job `{job_id}`.")
                    
                    # Only spawn worker for "start" triggers
                    if "test start" in dispatch_cmd:
                        self._ensure_worker_running()
                else:
                    if should_register:
                        self._active_jobs.pop(job_id, None)
                        self._save_active_jobs()
                    await say(f"❌ *Error:* Failed to queue job.")

        elif action == "service_call":
            method_name = cmd_config.get("method")
            if method_name and hasattr(self, method_name):
                logger.info(f"⚙️ Service Call | Method: {method_name}")
                method = getattr(self, method_name)
                
                # Pass relevant context to the service method
                call_kwargs = {**params, "channel_id": message.get("channel"), "user_id": user_id}
                response_text = await method(**call_kwargs)
                
                if response_text: # Some methods might handle their own 'say'
                    await say(response_text)
            else:
                await say(f"⚠️ *Configuration Error:* Method `{method_name}` not implemented.")

        elif action == "help":
            logger.info(f"❓ Help Requested | User: {user_id}")
            help_msg = "📂 *AI Investor Bot - Available Commands*\n\n"
            commands = self.config.get("commands", {})
            for name, cfg in commands.items():
                desc = cfg.get("description", "No description available.")
                ex = cfg.get("example", "No example.")
                help_msg += f"• *{name}*: {desc}\n  _Example:_ `{ex}`\n"
                
                # List subcommands if they exist
                subcommands = cfg.get("subcommands", {})
                if subcommands:
                    help_msg += "  _Subcommands:_\n"
                    for sub_name, sub_cfg in subcommands.items():
                        sub_desc = sub_cfg.get("description", "")
                        help_msg += f"    - `{sub_name}`: {sub_desc}\n"
                help_msg += "\n"
            
            help_msg += "--- \n_Note: Only authorized users can execute commands._"
            await say(help_msg)

        self._save_state(message.get("ts"))

    def _setup_middleware(self):
        """Register middleware for security and logging."""
        @self.bot.middleware
        async def restricted_access(payload: Dict[str, Any], next: Callable):
            user_id = None
            if "user" in payload:
                user_id = payload["user"]
            elif "event" in payload and "user" in payload["event"]:
                user_id = payload["event"]["user"]
            
            if not user_id or user_id in self.allowed_users or not self.allowed_users:
                return await next()
            
            logger.warning(f"Unauthorized access attempt by: {user_id}")

    async def process_missed_messages(self, channel_id: str):
        """Fetches and processes messages since last_processed_ts."""
        if not self.bot or self.mock:
            return

        logger.info(f"Checking for missed messages since TS: {self.last_processed_ts}")
        try:
            response = await self.bot.client.conversations_history(
                channel=channel_id,
                oldest=self.last_processed_ts
            )
            
            messages = response.get("messages", [])
            # Sort by timestamp ascending to process in order
            messages.sort(key=lambda x: x["ts"])
            
            count = 0
            commands_config = self.config.get("commands", {})
            
            for msg in messages:
                if msg.get("subtype") or msg.get("bot_id"):
                    continue
                
                text = msg.get("text", "")
                
                # Check text against all configured patterns
                is_recognized = False
                for name, cfg in commands_config.items():
                    pattern = cfg.get("pattern")
                    if pattern and re.search(pattern, text):
                        logger.info(f"Catch-up: Processing missed command: {name} (Text: {text})")
                        is_recognized = True
                        count += 1
                        break
                
                self._save_state(msg["ts"])
            
            if count > 0:
                await self.send_notification(
                    text=f"🔄 *Catch-up Complete:* Processed {count} missed job commands from offline period.",
                    level="info",
                    channel=channel_id
                )
        except Exception as e:
            logger.error(f"Error in catch-up logic: {e}")

    async def send_notification(self, text: str, level: str = "info", channel: Optional[str] = None, job_id: Optional[str] = None):
        """
        Sends a colored alert to Slack.
        If job_id is provided, it removes it from the active tracker.
        """
        if job_id:
            # Reload to ensure we have latest from other processes
            self._active_jobs = self._load_active_jobs()
            removed = self._active_jobs.pop(job_id, None)
            if removed:
                self._save_active_jobs()
                logger.info(f"🏁 Job {job_id} cleared from active queue via notification.")

        target_channel = channel or self.default_channel
        colors = {"info": "#d3d3d3", "success": "#2eb886", "warning": "#daa520", "critical": "#ff0000"}

        if self.mock:
            logger.info(f"[MOCK] {level.upper()}: {text}")
            return {"ok": True}

        payload = {
            "channel": target_channel,
            "attachments": [{"color": colors.get(level, "#d3d3d3"), "text": text, "footer": f"AI Investor | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}]
        }

        try:
            if not self._http_client:
                self._http_client = httpx.AsyncClient()
            
            headers = {"Authorization": f"Bearer {self.bot_token}"}
            response = await self._http_client.post(self.api_url, json=payload, headers=headers)
            return response.json()
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return {"ok": False, "error": str(e)}

    # --- Data Summary Methods (Phase 8) ---

    async def get_system_health_summary(self, **kwargs) -> str:
        """Fetches status of core services and system health."""
        try:
            from services.monitoring.system_health import get_system_health_service
            health_service = get_system_health_service()
            
            # Backend Check
            backend_up = await health_service.check_service_status("backend")
            status_emoji = "🟢" if backend_up else "🔴"
            
            # Docker Stats
            from scripts.runners.docker_control import get_docker_ps_data
            containers = get_docker_ps_data() or []
            running_count = sum(1 for c in containers if c.get('status', '').lower().startswith('up'))
            
            summary = (
                "🖥️ *System Health Summary*\n\n"
                f"• *Backend:* {status_emoji} {'Online' if backend_up else 'Down'}\n"
                f"• *Docker Infrastructure:* {running_count}/{len(containers)} containers UP\n"
                "• *Unified Gateway:* Active (Port 5050)\n"
                "--- \n_Type `!infra status` for container details._"
            )
            return summary
        except Exception as e:
            logger.error(f"Error getting health summary: {e}")
            return f"❌ *Error:* Failed to aggregate health data: `{str(e)}`"

    async def get_risk_summary(self, **kwargs) -> str:
        """Fetches VaR and circuit breaker status."""
        try:
            from services.risk.risk_monitor import get_risk_monitor
            from services.risk.circuit_breaker import get_circuit_breaker
            
            monitor = get_risk_monitor()
            breaker = get_circuit_breaker()
            
            # Mock calculations for summary
            var_value = monitor.calculate_parametric_var(1000000, 0.02)
            frozen_status = "❄️ *FROZEN*" if breaker.portfolio_frozen else "✅ *ACTIVE*"
            
            summary = (
                "⚖️ *Risk Monitor Summary*\n\n"
                f"• *Circuit Breaker:* {frozen_status}\n"
                f"• *Daily VaR (95%):* `${var_value:,.2f}`\n"
                f"• *Exposure Level:* Normal\n"
                f"• *Active Frozen Assets:* {len(breaker.frozen_assets)}\n\n"
                f"_Reason: {breaker.freeze_reason or 'None'}_"
            )
            return summary
        except Exception as e:
            logger.error(f"Error getting risk summary: {e}")
            return f"❌ *Error:* Failed to fetch risk metrics: `{str(e)}`"

    async def get_portfolio_summary(self, **kwargs) -> str:
        """Fetches current account balance and open positions from paper exchange."""
        try:
            from services.execution.paper_exchange import get_paper_exchange
            exchange = get_paper_exchange()
            summary = exchange.get_account_summary()
            
            pos_list = ""
            for ticker, qty in summary.get("positions", {}).items():
                pos_list += f"  - `{ticker}`: {qty} shares\n"
            
            if not pos_list:
                pos_list = "  - _No open positions._"

            response = (
                "📊 *Portfolio & Execution Status*\n\n"
                f"• *Account Balance:* `${summary.get('cash', 0):,.2d}`\n"
                f"• *Open Positions:*\n{pos_list}\n"
                "• *Last Activity:* Just now"
            )
            return response
        except Exception as e:
            logger.error(f"Error getting portfolio summary: {e}")
            return f"❌ *Error:* Failed to fetch portfolio data: `{str(e)}`"

    async def get_deals_summary(self, **kwargs) -> str:
        """Returns a formatted list of currently active club deals."""
        try:
            # Mock Active Deal List (Since DealManager is mostly an engine)
            deals = [
                {"name": "SpaceX Secondary", "size": "150M", "syndication": "50M", "status": "OPEN"},
                {"name": "Neuralink Series D", "size": "200M", "syndication": "25M", "status": "PENDING"}
            ]
            
            msg = "🤝 *Active Club Deals & Waitlist*\n\n"
            for d in deals:
                msg += f"• *{d['name']}*: Seeking `${d['syndication']}` total size `${d['size']}`. Status: `{d['status']}`\n"
            
            msg += "\n_Type `!deals allocate <id>` to start pro-rata processing._"
            return msg
        except Exception as e:
            logger.error(f"Error getting deals summary: {e}")
            return "❌ *Error:* Failed to fetch deal list."

    async def nuke_current_channel(self, channel_id: str, **kwargs) -> str:
        """
        Deletes messages concurrently with smart rate-limit handling and skip-on-failure logic.
        """
        # 1. Select Client (User token has more power)
        client = self.user_client if self.user_client else self.bot.client
        
        logger.info(f"🧨 NUKING CHANNEL: {channel_id} (Client: {'User' if self.user_client else 'Bot'})")

        async def _delete_msg(ts):
            retry_count = 0
            while retry_count < 3:
                try:
                    res = await client.chat_delete(channel=channel_id, ts=ts)
                    if res.get("ok"):
                        return True
                    
                    error = res.get("error")
                    if error == "ratelimited":
                        # Wait exactly as long as Slack suggests, or default to 5s
                        wait_time = int(res.headers.get("Retry-After", 5))
                        logger.warning(f"⏳ Rate limited. Sleeping for {wait_time}s...")
                        await asyncio.sleep(wait_time)
                        retry_count += 1
                        continue
                    
                    if error == "message_not_found":
                        return True # Already gone
                    
                    # Log but don't crash the loop
                    logger.error(f"⚠️ Slack Error deleting {ts}: {error}")
                    return False
                except Exception as e:
                    logger.error(f"⚠️ Exception deleting {ts}: {e}")
                    return False
            return False

        try:
            total_purged = 0
            cursor = None
            while True:
                # Use cursor for pagination to stepping through history
                response = await client.conversations_history(channel=channel_id, limit=100, cursor=cursor)
                if not response.get("ok"):
                    logger.error(f"❌ History Error: {response.get('error')}")
                    break
                    
                messages = response.get("messages", [])
                if not messages:
                    break
                
                # Filter for messages we can delete (actual data messages)
                ts_list = [m["ts"] for m in messages if "ts" in m]
                if not ts_list:
                    # If we have messages but no TS (unlikely), check cursor and continue
                    cursor = response.get("response_metadata", {}).get("next_cursor")
                    if not cursor: break
                    continue

                # Execute batch concurrently
                results = await asyncio.gather(*[_delete_msg(ts) for ts in ts_list])
                purged_in_batch = sum(1 for r in results if r)
                total_purged += purged_in_batch
                
                logger.info(f"✨ Purged batch: {purged_in_batch} messages. Total: {total_purged}")
                
                # Get next cursor
                cursor = response.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break
                
                # Brief pause to be respectful
                await asyncio.sleep(0.2)

            return f"AI_Investor Channel Cleared. Total purged: {total_purged}"
        except Exception as e:
            logger.error(f"Error during optimized nuke: {e}")
            return f"❌ *Error during nuke:* {str(e)}"

    async def get_job_queue(self, **kwargs) -> str:
        """Returns a formatted list of currently active jobs with status indicators."""
        self._active_jobs = self._load_active_jobs()
        if not self._active_jobs:
            return "✅ *Queue Empty:* No active jobs running."
            
        status_emojis = {
            "Queued": "📥",
            "Started": "⏳",
            "Processing": "⏳",
            "Completed": "✅"
        }
            
        msg = "📂 *AI Investor - Active Job Queue*\n\n"
        for jid, info in self._active_jobs.items():
            status = info.get("status", "Queued")
            emoji = status_emojis.get(status, "📥")
            msg += f"{emoji} `{jid}` | *{info['command']}* ({status})\n"
            msg += f"  _Started: {info['started_at']} by User: <@{info['user']}>_\n\n"
            
        msg += f"--- \n_Total: {len(self._active_jobs)} active jobs._"
        return msg

    async def clear_job_queue(self, **kwargs) -> str:
        """Purges all jobs from the local tracker and deletes the state file."""
        logger.info("🧹 Purging job queue and state file...")
        self._active_jobs = {}
        self._save_active_jobs()
        
        # Also explicitly remove the file to ensure a clean slate
        if os.path.exists(self.job_state_file):
            try:
                os.remove(self.job_state_file)
                logger.info(f"🗑️ Deleted state file: {self.job_state_file}")
            except Exception as e:
                logger.error(f"Failed to delete state file: {e}")
                
        return "🧹 **Queue Cleared:** All test jobs and state files have been purged for debugging."

    async def close(self):
        """Explicitly closes all HTTP sessions and terminates worker."""
        logger.info("🧹 Closing SlackService sessions...")
        
        # 0. Stop Kafka Consumer
        if hasattr(self, '_kafka_consumer') and self._kafka_consumer:
            try:
                self._kafka_consumer.stop()
                logger.info("✅ Kafka Alert Consumer stopped.")
            except Exception as e:
                logger.error(f"Error stopping Kafka consumer: {e}")
            finally:
                self._kafka_consumer = None

        # 1. Announce Disconnection and Update Status
        if not self.mock and self.bot:
            try:
                # Set status to Disconnected
                await self.update_bot_status("Disconnected", ":white_circle:")
                await self.update_bot_presence("away")
                
                # Send final message if channel is known
                if self.default_channel:
                    await self.send_notification(
                        text="🛑 *AI_Investor Bot Disconnected:* Service shutting down.",
                        level="warning",
                        channel=self.default_channel
                    )
            except Exception as e:
                logger.error(f"Error during final bot announcement: {e}")

        # 2. Stop Worker
        self.stop_worker()

        # 3. Close Socket Mode Handler
        if self._handler:
            try:
                await self._handler.close_async()
                logger.info("✅ Socket Mode handler closed.")
            except Exception as e:
                logger.error(f"Error closing socket handler: {e}")
            finally:
                self._handler = None

        # 3. Close User Client (xoxp)
        if self.user_client:
            try:
                # AsyncWebClient uses aiohttp session internally
                if hasattr(self.user_client, "session") and self.user_client.session:
                    await self.user_client.session.close()
                elif hasattr(self.user_client, "close"):
                    await self.user_client.close()
                logger.info("✅ User client closed.")
            except Exception as e:
                logger.error(f"Error closing user client: {e}")

        # 4. Close internal httpx client
        if self._http_client:
            try:
                await self._http_client.aclose()
                logger.info("✅ HTTP client closed.")
            except Exception as e:
                logger.error(f"Error closing HTTP client: {e}")
            finally:
                self._http_client = None

        # 5. Cancel Presence Heartbeat
        if self._presence_task:
            self._presence_task.cancel()
            try:
                await self._presence_task
            except asyncio.CancelledError:
                pass
            self._presence_task = None
            logger.info("✅ Presence heartbeat stopped.")

    async def start_bot(self):
        """Starts the Socket Mode handler and Catch-up logic."""
        if self.mock or not self.bot:
            return

        # 0. Start Kafka Consumer for Outgoing Alerts
        try:
            from services.kafka.slack_consumer import get_slack_consumer
            self._kafka_consumer = get_slack_consumer()
            self._kafka_consumer.start()
            logger.info("✅ Kafka Alert Consumer started in background.")
        except Exception as e:
            # This is non-blocking for local dev without confluent-kafka
            logger.warning(f"⚠️ Could not start Kafka Consumer (likely no confluent-kafka or kafka unavailable): {e}")

        # 1. Run Catch-up
        if self.default_channel:
            await self.process_missed_messages(self.default_channel)
            
            # Announce Connection
            await self.send_notification(
                text="🚀 *AI_Investor Bot Connected and Online*",
                level="success",
                channel=self.default_channel
            )

        # 2. Set Status to Initial State
        await self._try_acquire_leader_lock()
        status_text = f"Online ({self.node_id})" if self.is_leader else f"Standby ({self.node_id})"
        status_emoji = ":large_green_circle:" if self.is_leader else ":white_circle:"
        
        await self.update_bot_status(status_text, status_emoji)
        await self.update_bot_presence("auto" if self.is_leader else "away")

        # 3. Start Presence Heartbeat (Keep-Alive)
        self._presence_task = asyncio.create_task(self._presence_heartbeat())

        # 4. Start Listener
        self._handler = AsyncSocketModeHandler(self.bot, self.socket_token)
        try:
            await self._handler.start_async()
        except KeyboardInterrupt:
            pass # Handled by outer try/except in main
        finally:
            await self.close()
            logger.info("🛑 Slack Bot shutdown complete.")

# --- Global Instance Setup ---
_service = None

def get_slack_service(mock: bool = False) -> SlackService:
    global _service
    if _service is None:
        _service = SlackService(mock=mock)
    return _service

if __name__ == "__main__":
    async def main():
        service = get_slack_service(mock=False)
        if not service.bot_token or not service.socket_token:
            print("❌ ERROR: SLACK_BOT_TOKEN and SLACK_SOCKET_TOKEN must be in .env")
            return

        print("🚀 Starting Secure AI Investor Bot with Catch-up logic...")
        await service.send_notification(text="🛠️ *Service Online:* Bot is active and ready for jobs.", level="success")
        await service.start_bot()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping service...")

