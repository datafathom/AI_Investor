import subprocess
import time
import os
import sys
import socket
from pathlib import Path

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_verification():
    print("[START] Starting verification of dev-no-db fix...")
    
    project_root = Path(__file__).parent.parent
    python_exe = sys.executable
    
    # Use venv if available
    venv_python = project_root / "venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        python_exe = str(venv_python)
        print(f"[VENV] Using venv: {python_exe}")
    
    cmd = [python_exe, "cli.py", "dev-no-db"]
    
    print(f"[RUN] Running command: {' '.join(cmd)}")
    
    # Start process with captured output
    process = subprocess.Popen(
        cmd,
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1, # Line buffered
        env=os.environ.copy()
    )
    
    output_lines = []
    start_time = time.time()
    max_wait = 30 # Wait up to 30 seconds
    
    backend_started = False
    frontend_started = False
    
    print("[LOGS] Capturing output (watching for real-time logs)...")
    
    try:
        while time.time() - start_time < max_wait:
            line = process.stdout.readline()
            if line:
                line = line.strip()
                print(f"   {line}")
                output_lines.append(line)
                
                if "[BACKEND]" in line:
                    backend_started = True
                if "[FRONTEND]" in line:
                    frontend_started = True
                
                # If we see both, we can check ports
                if backend_started and frontend_started:
                    print("[OK] Both logs detected. Checking ports...")
                    time.sleep(5) # Give Vite a moment
                    if check_port(5050) and check_port(5173):
                        print("[OK] Port 5050 (Backend) and 5173 (Frontend) are OPEN.")
                        process.terminate()
                        return True
                    else:
                        print("[WARN] Logs detected but ports not open yet. Continuing...")
            
            if process.poll() is not None:
                print("[ERROR] Process exited prematurely.")
                break
                
    except Exception as e:
        print(f"[ERROR] Error during capture: {e}")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()
            
    print("\n[RESULTS] Results:")
    print(f"   Backend Started: {backend_started}")
    print(f"   Frontend Started: {frontend_started}")
    print(f"   Port 5050 Open: {check_port(5050)}")
    print(f"   Port 5173 Open: {check_port(5173)}")
    
    return backend_started and frontend_started and check_port(5050) and check_port(5173)

if __name__ == "__main__":
    success = run_verification()
    if success:
        print("\n[SUCCESS] VERIFICATION SUCCESSFUL")
        sys.exit(0)
    else:
        print("\n[FAILED] VERIFICATION FAILED")
        sys.exit(1)
