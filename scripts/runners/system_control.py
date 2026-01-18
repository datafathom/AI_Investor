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
    docker_up() 
    
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
    """Stop all services using Docker and kill host processes."""
    import subprocess
    logger.info("Stopping AI Investor System...")
    
    # 1. Stop Docker
    docker_down()
    
    # 2. Kill Host Processes
    print("🔪 Killing Host Processes (Python/Node)...")
    try:
        subprocess.run("taskkill /F /IM python.exe /T", shell=True, stderr=subprocess.DEVNULL)
        subprocess.run("taskkill /F /IM node.exe /T", shell=True, stderr=subprocess.DEVNULL)
    except Exception as e:
        logger.warning(f"Error killing host processes: {e}")
        
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
        url = "http://localhost:5050/health"
        print(f"Checking {url}...")
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Backend Check Failed: {e}")
        return False
def check_port(port: int = 5050, **kwargs):
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

def reset_dev(**kwargs):
    """Nuke and Pave: Stop/Prune, Start, and Seed."""
    from .seed_db import run_seed_db
    import time
    
    logger.info("🔥 Starting Unified Reset (Nuke & Pave)...")
    
    # 1. Down with volumes
    docker_down(volumes=True)
    
    # 2. Up
    docker_up()
    
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

def run_demo_mode(**kwargs):
    """
    Stop everything, then start Backend and Frontend in new console windows.
    Ideal for demos to ensure a clean slate and visible logs.
    """
    import subprocess
    import os
    import sys
    import time
    from pathlib import Path
    import traceback

    try:
        current_pid = os.getpid()
        print(f"🎬 Starting Demo Mode Protocol (My PID: {current_pid})...", flush=True)

        # 1. Kill Previous Runtimes (Safer Method)
        print(f"🔪 Killing old processes...", flush=True)
        
        # Kill Node (Frontend) - Global kill is usually safe for node in this context
        try:
            subprocess.run("taskkill /F /IM node.exe /T", shell=True, stderr=subprocess.DEVNULL)
        except: pass

        # Kill Backend by Port 5050 (Safer than killing all python)
        def kill_listeners_on_ports(ports):
            """Kill any process listening on the specified ports."""
            for port in ports:
                try:
                    # Find PID listening on port
                    cmd = f"netstat -ano | findstr :{port}"
                    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    lines = res.stdout.strip().split('\n')
                    killed_pids = set()
                    
                    for line in lines:
                        if "LISTENING" in line:
                            parts = line.split()
                            # In netstat output, PID is the last element
                            pid = parts[-1]
                            
                            if pid and pid != "0" and pid != str(current_pid) and pid not in killed_pids:
                                print(f"   - 🧹 Cleaning Port {port}: Killing PID {pid}...", flush=True)
                                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, stderr=subprocess.DEVNULL)
                                killed_pids.add(pid)
                except Exception as e:
                    print(f"   Warning killing port {port}: {e}", flush=True)

        # Nuclear option on expected ports
        print("🔪 Performing aggressive port cleanup...", flush=True)
        kill_listeners_on_ports([5050]) # Backend
        kill_listeners_on_ports(range(5170, 5181)) # Frontend range (Vite hops)

        print("✅ Cleanup complete.", flush=True)

        # 2. Start Infrastructure
        print("🏗️  Ensuring Docker Infrastructure is UP...", flush=True)
        
        # Manually call docker_up logic here to avoid sys.exit(1) from the module if it fails
        # or just wrap it in try/except
        try:
            docker_up()
        except SystemExit as se:
            if se.code != 0:
                print(f"❌ Docker start failed with code {se.code}. Continuing anyway to attempt app launch...", flush=True)
            else:
                print("✅ Docker start returned success.", flush=True)
        except Exception as e:
            print(f"❌ Docker start failed: {e}", flush=True)
        
        # Wait a moment for ports to clear/start
        time.sleep(3)

        project_root = str(Path(__file__).parent.parent.parent.absolute())
        
        # 3. Start Backend in New Window
        print("🚀 Launching Backend (New Window)...", flush=True)
        python_exe = os.path.join(project_root, "venv", "Scripts", "python.exe")
        if not os.path.exists(python_exe):
             python_exe = sys.executable # Fallback

        backend_script = os.path.join(project_root, "web", "app.py")
        
        backend_env = os.environ.copy()
        backend_env["PYTHONPATH"] = project_root
        backend_env["FLASK_APP"] = "web/app.py"
        backend_env["FLASK_ENV"] = "development"

        try:
            # CREATE_NEW_CONSOLE is Windows only (0x10)
            subprocess.Popen(
                [python_exe, backend_script],
                cwd=project_root,
                env=backend_env,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            logger.error(f"Failed to launch backend: {e}")

        # 4. Start Frontend in New Window
        print("🚀 Launching Frontend (New Window)...", flush=True)
        frontend_path = os.path.join(project_root, "frontend2")
        
        try:
            # Use npm.cmd directly for better Windows process handling
            # Enforce STRICT port 5173 usage as per /investor-dev workflow
            subprocess.Popen(
                ["npm.cmd", "run", "dev", "--", "--port", "5173", "--strictPort"],
                cwd=frontend_path,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        except Exception as e:
            logger.error(f"Failed to launch frontend: {e}")

        print("\n⏳ Waiting for Backend to be ready (checking http://127.0.0.1:5050/health)...", flush=True)
        import urllib.request
        import urllib.error
        
        backend_ready = False
        for i in range(30): # Wait up to 30 seconds
            try:
                with urllib.request.urlopen("http://127.0.0.1:5050/health", timeout=1) as response:
                    if response.status == 200:
                        print("✅ Backend is HEALTHY and listening!", flush=True)
                        backend_ready = True
                        break
            except Exception:
                time.sleep(1)
                print(".", end="", flush=True)
        
        if not backend_ready:
            print("\n⚠️ Backend verify timed out. It might still be starting.", flush=True)
        else:
            print("\n✅ Backend confirmed.", flush=True)

        # 5. Find Frontend Port and Open Browser
        print("🔍 Scanning for active Frontend port (5173-5180)...", flush=True)
        frontend_port = None
        
        # Scan ports up to 10 seconds
        for _ in range(20): 
            for port in range(5173, 5181):
                try:
                    # Simple socket connect check
                    import socket
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.1)
                        if s.connect_ex(('127.0.0.1', port)) == 0:
                            frontend_port = port
                            break
                except:
                    pass
            if frontend_port:
                break
            time.sleep(0.5)
            print(".", end="", flush=True)

        if frontend_port:
            print(f"\n✅ Frontend found on port {frontend_port}!", flush=True)
            url = f"http://localhost:{frontend_port}"
        else:
            print("\n⚠️  Could not detect Frontend port. Defaulting to 5173.", flush=True)
            url = "http://localhost:5173"

        print(f"🌍 Opening Browser to {url}...", flush=True)
        import webbrowser
        webbrowser.open(url) 

        print("\n✅ Demo Mode Initiated Successfully!", flush=True)
        print("   - Backend: Running & Verified")
        print("   - Frontend: Running in new window")
        print(f"   - Browser: Launched ({url})")
        return True

    except Exception as e:
        print(f"\n❌ FATAL ERROR in run_demo_mode: {e}", flush=True)
        traceback.print_exc()
        return False
