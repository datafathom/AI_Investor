import psutil
import os
import signal

def kill_processes_by_name(name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if name.lower() in proc.info['name'].lower():
                print(f"Killing {name} process: {proc.info['pid']}")
                proc.kill()
            elif proc.info['cmdline'] and any(name.lower() in arg.lower() for arg in proc.info['cmdline']):
                 print(f"Killing {name} process based on cmdline: {proc.info['pid']}")
                 proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == "__main__":
    print("Stopping previous runtimes...")
    kill_processes_by_name("python")
    kill_processes_by_name("node")
    print("Done.")
