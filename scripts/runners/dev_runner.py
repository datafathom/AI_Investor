"""
==============================================================================
FILE: scripts/runners/dev_runner.py
ROLE: Developer Mode Runner
PURPOSE: Orchestrates a Hot-Reload development environment.
         - Ensures Infra is up (lite mode).
         - Runs Backend in Debug Mode (Auto-Reload).
         - Runs Frontend in Dev Mode (HMR).
         - Manages process lifecycle (Ctrl+C kills all).
==============================================================================
"""

import subprocess
import sys
import time
import signal
import os
import threading
from pathlib import Path
import psutil

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
    print(f"🔪 Cleaning port {port}...")
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    print(f"   Found process {proc.info['name']} (PID {proc.info['pid']}) on port {port}. Killing...")
                    proc.kill()
                    proc.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue

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
                print(f"[{prefix}] {line.strip()}")
    except Exception:
        pass

def start_dev_mode(check_infra=True):
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

    # 3. Start Backend (Flask Debug)
    print("Launching Backend (Hot-Reload Enabled)...")
    
    # Robust Python Detection: Prefer Venv if it exists
    python_exe = sys.executable
    venv_python = PROJECT_ROOT / "venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
        
    if venv_python.exists():
        print(f"📦 Using virtual environment: {venv_python}")
        python_exe = str(venv_python)
    else:
        print(f"⚠️ Warning: Virtual environment not found. Using system python: {python_exe}")

    backend_env = os.environ.copy()
    backend_env["FLASK_APP"] = "web.app"
    backend_env["FLASK_ENV"] = "development"
    backend_env["FLASK_DEBUG"] = "1"
    backend_env["PYTHONIOENCODING"] = "utf-8"
    backend_env["PYTHONPATH"] = str(PROJECT_ROOT) # Ensure project root is in path
    
    backend_cmd = [
        python_exe, "web/app.py"
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

    # 4. Start Frontend (Vite)
    print("Launching Frontend (Vite HMR)...")
    frontend_dir = PROJECT_ROOT / "frontend2"
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
        print("\n🛑 Stopping Dev Mode...")
    finally:
        print("Cleaning up processes...")
        kill_proc_tree(backend_proc.pid)
        kill_proc_tree(frontend_proc.pid)
        print("Bye!")

def start_dev_full():
    """Starts Docker infrastructure AND the development environment."""
    print("🚀 Starting FULL DEV stack (Docker + Backend + Frontend)...")
    try:
        # Force Docker Up
        subprocess.run([sys.executable, "cli.py", "docker", "up", "--profile", "full"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Error starting Docker infrastructure.")
        return

    # Proceed with standard checks (which will pass since we just started it)
    start_dev_mode()

def start_dev_no_db():
    """Starts development environment WITHOUT checking infrastructure."""
    print("⚡ Starting LIGHT DEV stack (Backend + Frontend ONLY)...")
    print("   Assuming infrastructure is running elsewhere (2-Node Mode).")
    
    # We monkey-patch the check_port to always return True for this run
    # OR we just copy the logic but skip the infra check. 
    # Let's refactor start_dev_mode to accept a 'check_infra' arg.
    start_dev_mode(check_infra=False)
