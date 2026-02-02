"""
scripts/runners/git_leaks_runner.py
Purpose: Handler for gitleaks audit command.
"""

import subprocess
import logging
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

def run_gitleaks_audit(**kwargs) -> bool:
    """
    Run the gitleaks audit tool for the .git repo in the project.
    Shows gitleaks output to the terminal.
    """
    logger.info("Starting Gitleaks scan...")
    
    # Check if gitleaks is installed
    gitleaks_path = shutil.which("gitleaks")
    
    # On Windows, winget adds it to a path that might need a shell restart
    # Let's check common WinGet link location explicitly for a better UX
    if not gitleaks_path and sys.platform == "win32":
        winget_path = Path(sys.executable).parent.parent.parent / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / "gitleaks.exe"
        # Fallback to absolute home path if sys.executable logic is weird
        if not winget_path.exists():
            winget_path = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links" / "gitleaks.exe"
            
        if winget_path.exists():
            gitleaks_path = str(winget_path)

    if not gitleaks_path:
        print("\n❌ Error: 'gitleaks' executable not found in PATH.")
        print("\nTo install gitleaks:")
        print("  - Windows:  'winget install gitleaks' or download from https://github.com/gitleaks/gitleaks/releases")
        print("  - MacOS:    'brew install gitleaks'")
        print("  - Linux:    Download the binary from the releases page.")
        print("\nAfter installation, ensure it's in your PATH and try again.\n")
        return False

    project_root = Path(__file__).parent.parent.parent.absolute()
    
    # Check if .git exists
    if not (project_root / ".git").exists():
        print(f"❌ Error: No .git repository found at {project_root}")
        return False

    print(f"🔍 Running Gitleaks detect on {project_root}...")
    
    try:
        # --source . : scan the current directory
        # -v         : verbose output
        # --no-banner: skip gitleaks banner
        cmd = [gitleaks_path, "detect", "--source", ".", "-v", "--no-banner"]
        
        # We use subprocess.run without capture_output to stream directly to terminal
        result = subprocess.run(cmd, cwd=str(project_root))
        
        if result.returncode == 0:
            print("\n✅ Gitleaks: No leaks detected.")
            return True
        elif result.returncode == 1:
            print("\n⚠️  Gitleaks: Leaks were detected! Check the output above.")
            return False
        else:
            print(f"\n❌ Gitleaks exited with error code {result.returncode}")
            return False
            
    except Exception as e:
        logger.exception(f"Unexpected error running gitleaks: {e}")
        print(f"❌ Error running Gitleaks: {e}")
        return False

if __name__ == "__main__":
    # For quick manual testing
    run_gitleaks_audit()
