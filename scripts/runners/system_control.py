"""
scripts/runners/system_control.py
Purpose: Top-level system control handlers.
"""

import logging

logger = logging.getLogger(__name__)

from .docker_control import docker_up, docker_down

def start_all(**kwargs):
    """Start all services (Host for app, Docker for infra)."""
    logger.info("Starting AI Investor System...")
    
    # 1. Start Infrastructure (Postgres, etc)
    docker_up(lite=True) # Default to lite for memory savings
    
    # 2. Start Backend (Non-blocking ideally, but system_control functions usually block)
    # Since we can't easily run multiple blocking commands in one thread without backgrounding,
    # we'll tell the user how to run them or implement a background runner.
    # For now, let's keep it simple and provide individual commands in the summary.
    print("\n✅ Infrastructure started.")
    print("👉 To start the full system, run these in separate terminals:")
    print("   1. python cli.py start-backend")
    print("   2. python cli.py start-frontend")
    
    return True

def stop_all(**kwargs):
    """Stop all services using Docker."""
    logger.info("Stopping AI Investor System...")
    docker_down()
    return True

def verify_pipeline(**kwargs):
    """Verify data pipeline."""
    logger.info("Verifying Pipeline...")
    print("Pipeline verification running (Placeholder).")
    return True

def check_backend(**kwargs):
    """Quickly check backend health using requests."""
    import requests
    try:
        url = "http://localhost:5000/health"
        print(f"Checking {url}...")
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Backend Check Failed: {e}")
        return False
def check_port(port: int = 5000, **kwargs):
    """Check if a specific port is listening on the host."""
    import subprocess
    import platform
    
    print(f"🔍 Checking if port {port} is listening...")
    
    try:
        if platform.system() == "Windows":
            cmd = f"netstat -ano | findstr :{port}"
            # Use shell=True for findstr pipe on Windows
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        else:
            cmd = f"lsof -i :{port}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
        if result.stdout:
            print(f"✅ Port {port} is ACTIVE:")
            print(result.stdout)
            return True
        else:
            print(f"❌ Port {port} is NOT LISTENING.")
            return False
    except Exception as e:
        print(f"Error checking port: {e}")
        return False

def reset_dev(lite: bool = False, **kwargs):
    """Nuke and Pave: Stop/Prune, Start, and Seed."""
    from .seed_db import run_seed_db
    import time
    
    logger.info("🔥 Starting Unified Reset (Nuke & Pave)...")
    
    # 1. Down with volumes
    docker_down(volumes=True)
    
    # 2. Up (Lite or Full)
    docker_up(lite=lite)
    
    # 3. Wait for Postgres (simple sleep for now, could be more robust)
    print("⏳ Waiting for database to stabilize (10s)...")
    time.sleep(10)
    
    # 4. Seed
    run_seed_db()
    
    print("\n✨ Reset complete! You are ready to develop.")
    return True

def start_backend(**kwargs):
    """Start the backend on the host with necessary environment variables."""
    import subprocess
    import os
    import sys
    from pathlib import Path

    logger.info("🚀 Starting Backend on Host...")
    
    # Get project root
    project_root = str(Path(__file__).parent.parent.parent.absolute())
    
    # Setup environment
    env = os.environ.copy()
    env["PYTHONPATH"] = project_root
    env["FLASK_APP"] = "web/app.py"
    env["FLASK_ENV"] = "development"
    
    # Path to venv python
    python_exe = os.path.join(project_root, "venv", "Scripts", "python.exe")
    if not os.path.exists(python_exe):
        # Fallback for non-Windows or different venv structure
        python_exe = os.path.join(project_root, "venv", "bin", "python")
    
    if not os.path.exists(python_exe):
        logger.error(f"❌ Virtual environment not found at {python_exe}")
        return False

    cmd = [python_exe, "web/app.py"]
    
    try:
        # Run in a way that output is shown but potentially doesn't block if handled as background
        # For now, we'll let the user run it and see logs
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd, env=env, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Backend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("🛑 Backend stopped by user.")
        return True
    except Exception as e:
        logger.exception(f"❌ Unexpected error starting backend: {e}")
        return False
def start_frontend(**kwargs):
    """Start the frontend React app on the host."""
    import subprocess
    import os
    from pathlib import Path

    logger.info("🚀 Starting Frontend on Host...")
    
    project_root = str(Path(__file__).parent.parent.parent.absolute())
    frontend_path = os.path.join(project_root, "frontend2")
    
    if not os.path.exists(frontend_path):
        logger.error(f"❌ Frontend directory not found at {frontend_path}")
        return False

    # Check if node_modules exists
    if not os.path.exists(os.path.join(frontend_path, "node_modules")):
        logger.info("📦 node_modules missing. Running npm install...")
        subprocess.run("npm install", cwd=frontend_path, shell=True, check=True)

    cmd = ["npm", "run", "dev"]
    
    try:
        print(f"Running: {' '.join(cmd)} in {frontend_path}")
        # Run in a way that output is shown
        subprocess.run(cmd, cwd=frontend_path, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Frontend failed to start: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("🛑 Frontend stopped by user.")
        return True
    except Exception as e:
        logger.exception(f"❌ Unexpected error starting frontend: {e}")
        return False
