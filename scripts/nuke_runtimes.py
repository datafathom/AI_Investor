import subprocess
import os
import sys

def nuke_runtimes():
    print("🧹 Sweeping previous runtimes...")
    
    # 1. Kill Python
    print("   Killing Python processes...")
    subprocess.run("taskkill /F /IM python.exe /T", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    # 2. Kill Node
    print("   Killing Node processes...")
    subprocess.run("taskkill /F /IM node.exe /T", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    # 3. Docker Down? User didn't specify docker in the last request, but workflow says so.
    # However, dev-no-db implies we don't care about local DB. 
    # Let's just stick to runtimes as requested.
    
    print("✨ Cleanup complete (Ghost processes purged).")

if __name__ == "__main__":
    nuke_runtimes()
