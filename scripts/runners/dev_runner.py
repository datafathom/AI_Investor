# scripts/runners/dev_runner.py

import subprocess
import sys
import time
import signal
import os
import threading
from pathlib import Path
import psutil

# Fix Windows console encoding for emojis and prevent stalling
if sys.platform == 'win32':
    import io
    try:
        # Python 3.7+ supports reconfigure for better line buffering control
        sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
        sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
    except (AttributeError, io.UnsupportedOperation):
        # Fallback for environments where reconfigure might fail or isn't available
        if not isinstance(sys.stdout, io.TextIOWrapper):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
        if not isinstance(sys.stderr, io.TextIOWrapper):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)


# Configuration
BACKEND_PORT = 5050
FRONTEND_PORT = 5173
PROJECT_ROOT = Path(__file__).parent.parent.parent

def check_port(port):
    """Check if a port is in use."""
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False

def kill_port(port):
    """Forcefully kill any process listening on the given port."""
    print(f"[KILL] Cleaning port {port}...", flush=True)
    try:
        if sys.platform == "win32":
            # Use netstat to find PID
            cmd = f"netstat -ano | findstr :{port}"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in res.stdout.strip().split('\n'):
                if "LISTENING" in line:
                    pid = line.strip().split()[-1]
                    if pid and pid != "0":
                        print(f"   Found process on port {port} (PID {pid}). Killing...", flush=True)
                        subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, stderr=subprocess.DEVNULL)
        else:
            # Unix/macOS
            subprocess.run(f"fuser -k {port}/tcp", shell=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"   Warning cleaning port {port}: {e}", flush=True)

def kill_proc_tree(pid, including_parent=True):
    """Kill a process tree (including children)."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.kill()
            except psutil.NoSuchProcess:
                pass
        if including_parent:
            try:
                parent.kill()
            except psutil.NoSuchProcess:
                pass
    except psutil.NoSuchProcess:
        pass

def stream_output(process, prefix):
    """Reads stdout from a subprocess and prints with prefix."""
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{prefix}] {line.strip()}", flush=True)
    except Exception:
        pass

def start_dev_mode(check_infra: bool = True, slackbot: bool = True):
    """Main Entry Point for Dev Mode."""
    print("Starting AI Investor DEV MODE (Hot Reload)...")
    
    # 1. Check Infra
    if check_infra:
        print("Checking Infrastructure...")
        # Very basic check: Is Docker Postgres running?
        # Ideally reuse scripts/runners/docker_control.py but we keep it simple here.
        # We assume 'python cli.py start-infra' was run or we run it now?
        # Let's try to verify ports.
        if not check_port(5432) or not check_port(9092) or not check_port(6379): # Postgres, Kafka, Redis
            print("Warning: Infrastructure ports not open. Attempting to start Docker containers...")
            try:
                subprocess.run([sys.executable, "cli.py", "docker", "up"], check=True)
            except subprocess.CalledProcessError:
                print("Error: Failed to start infrastructure. Please run 'python cli.py docker up' manually.")
                return

    # 2. Cleanup Ports
    kill_port(BACKEND_PORT)
    kill_port(FRONTEND_PORT)
    time.sleep(1) # Brief pause for OS to release pins

    # 3. Start Backend (FastAPI Gateay - Hot-Reload Enabled)
    print("Launching Backend (FastAPI Gateway - Hot-Reload Enabled)...")
    
    # Robust Python Detection: Prefer Venv if it exists
    python_exe = sys.executable
    venv_python = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
        
    if venv_python.exists():
        print(f"[VENV] Using virtual environment: {venv_python}")
        python_exe = str(venv_python)
    else:
        print(f"[WARN] Warning: Virtual environment not found. Using system python: {python_exe}")

    backend_env = os.environ.copy()
    backend_env["PYTHONIOENCODING"] = "utf-8"
    backend_env["PYTHONUNBUFFERED"] = "1"
    backend_env["PYTHONPATH"] = str(PROJECT_ROOT)
    
    backend_cmd = [
        python_exe, "-u", "-m", "uvicorn", "web.fastapi_gateway:app",
        "--host", "127.0.0.1",
        "--port", str(BACKEND_PORT),
        "--reload",
        "--reload-dir", "web"
    ]

    
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(PROJECT_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=backend_env,
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )
    
    # Start Backend Output Thread
    t_backend = threading.Thread(target=stream_output, args=(backend_proc, "BACKEND"))
    t_backend.daemon = True
    t_backend.start()

    # BRIEF DELAY: Ensure backend has a head start on port 5050
    print("Waiting for backend to bind to port...", flush=True)
    time.sleep(5)


    # 4. Start Frontend (Vite)
    print("Launching Frontend (Vite HMR)...", flush=True)

    frontend_dir = PROJECT_ROOT / "frontend"
    frontend_cmd = ["npm", "run", "dev", "--", "--port", str(FRONTEND_PORT)]
    # Windows needs shell=True for npm usually
    
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(frontend_dir),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
    )

    # Start Frontend Output Thread
    t_frontend = threading.Thread(target=stream_output, args=(frontend_proc, "FRONTEND"))
    t_frontend.daemon = True
    t_frontend.start()
    
    # 5. Start Slack Bot (Optional)
    slack_proc = None
    if slackbot:
        from scripts.runners.slack_runner import stop_bot
        stop_bot(silent=True)
        
        print("Launching Slack Bot (Catch-up & Dispatch Enabled)...")
        slack_cmd = [python_exe, "cli.py", "slack", "start"]
        slack_proc = subprocess.Popen(
            slack_cmd,
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=backend_env,
            text=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )

        t_slack = threading.Thread(target=stream_output, args=(slack_proc, "SLACK"))
        t_slack.daemon = True
        t_slack.start()
    else:
        print(">>> Skipping Slack Bot startup (--slackbot false).")

    print(f"\nDEV MODE ACTIVE. Press Ctrl+C to stop.")
    print(f"   API: http://localhost:{BACKEND_PORT}")
    print(f"   GUI: http://localhost:{FRONTEND_PORT}\n")

    # 5. Monitoring Loop
    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("ERROR Backend process died.")
                break
            # Frontend via npm shell=True is harder to poll accurately on Windows but we try
    except KeyboardInterrupt:
        print("\n[STOP] Stopping Dev Mode...")
    finally:
        print("Cleaning up processes...")
        kill_proc_tree(backend_proc.pid)
        kill_proc_tree(frontend_proc.pid)
        if slack_proc:
            kill_proc_tree(slack_proc.pid)
        print("Bye!")

def start_dev_full(slackbot: bool = True):
    """Starts Docker infrastructure AND the development environment."""
    print("[START] Starting FULL DEV stack (Docker + Backend + Frontend)...")
    try:
        # Force Docker Up
        subprocess.run([sys.executable, "cli.py", "docker", "up", "--profile", "full"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Error starting Docker infrastructure.")
        return

    # Proceed with standard checks (which will pass since we just started it)
    start_dev_mode(check_infra=True, slackbot=slackbot)

def start_dev_no_db(slackbot: bool = True):
    """Starts development environment WITHOUT checking infrastructure."""
    print("Starting LIGHT DEV stack (Backend + Frontend ONLY)...")
    print("   Assuming infrastructure is running elsewhere (2-Node Mode).")
    
    # Force Mock Modes for services that check ports
    os.environ["NEO4J_MODE"] = "MOCK"
    os.environ["STORAGE_MODE"] = "MOCK"
    os.environ["SQL_MODE"] = "MOCK"
    
    start_dev_mode(check_infra=False, slackbot=slackbot)

