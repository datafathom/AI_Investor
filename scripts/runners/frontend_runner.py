"""
Frontend Runner
Handles all frontend operations via CLI
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class FrontendRunner:
    """Manages frontend operations."""
    
    def __init__(self):
        self.frontend_dir = Path(__file__).parent.parent.parent / "frontend2"
    
    def start_dev(self, port=None):
        """Start frontend development server."""
        os.chdir(self.frontend_dir)
        
        env = os.environ.copy()
        if port:
            env['VITE_PORT'] = str(port)
        
        print(f"Starting frontend dev server...")
        print(f"Directory: {self.frontend_dir}")
        if port:
            print(f"Port: {port}")
        print(f"Open http://localhost:{port or 5173} in your browser")
        print("")
        
        try:
            subprocess.run([sys.executable, "-m", "npm", "run", "dev"], env=env, check=False)
        except FileNotFoundError:
            # Try direct npm
            subprocess.run(["npm", "run", "dev"], env=env, check=False)
    
    def build(self):
        """Build frontend for production."""
        os.chdir(self.frontend_dir)
        
        print("Building frontend for production...")
        print(f"Directory: {self.frontend_dir}")
        print("")
        
        try:
            result = subprocess.run(
                ["npm", "run", "build"],
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            print("Build successful!")
            print(f"Output: {self.frontend_dir / 'dist'}")
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")
            if e.stderr:
                print(e.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("npm not found. Please install Node.js and npm.")
            sys.exit(1)
    
    def preview(self):
        """Preview production build."""
        os.chdir(self.frontend_dir)
        
        print("Starting preview server...")
        print(f"Directory: {self.frontend_dir}")
        print("")
        
        try:
            subprocess.run(["npm", "run", "serve"], check=False)
        except FileNotFoundError:
            print("ERROR npm not found. Please install Node.js and npm.")
            sys.exit(1)
    
    def install(self):
        """Install frontend dependencies."""
        os.chdir(self.frontend_dir)
        
        print("Installing frontend dependencies...")
        print(f"Directory: {self.frontend_dir}")
        print("")
        
        try:
            subprocess.run(["npm", "install", "--legacy-peer-deps"], check=True)
            print("Dependencies installed!")
        except FileNotFoundError:
            print("npm not found. Please install Node.js and npm.")
            sys.exit(1)
    
    def lint(self):
        """Run frontend linter."""
        os.chdir(self.frontend_dir)
        
        print("Running linter...")
        print("")
        
        try:
            subprocess.run(["npm", "run", "lint"], check=False)
        except FileNotFoundError:
            print("ERROR npm not found. Please install Node.js and npm.")
            sys.exit(1)
    
    def verify(self):
        """Verify frontend setup."""
        print("Verifying frontend setup...")
        print("")
        
        checks = []
        
        # Check directory
        if self.frontend_dir.exists():
            checks.append(("OK", "Frontend directory exists"))
        else:
            checks.append(("ERROR", "Frontend directory missing"))
            return
        
        # Check package.json
        package_json = self.frontend_dir / "package.json"
        if package_json.exists():
            checks.append(("OK", "package.json exists"))
        else:
            checks.append(("ERROR", "package.json missing"))
        
        # Check node_modules
        node_modules = self.frontend_dir / "node_modules"
        if node_modules.exists():
            checks.append(("OK", "Dependencies installed"))
        else:
            checks.append(("WARN", "Dependencies not installed (run: cli frontend install)"))
        
        # Check entry point
        entry_points = ["src/main.jsx", "src/main.js", "src/index.jsx", "src/index.js"]
        found_entry = False
        for entry in entry_points:
            if (self.frontend_dir / entry).exists():
                checks.append(("OK", f"Entry point found: {entry}"))
                found_entry = True
                break
        if not found_entry:
            checks.append(("ERROR", "Entry point missing"))
        
        # Check App component
        if (self.frontend_dir / "src/App.jsx").exists() or (self.frontend_dir / "src/App.js").exists():
            checks.append(("OK", "App component exists"))
        else:
            checks.append(("ERROR", "App component missing"))
        
        # Print results
        for status, message in checks:
            print(f"[{status}] {message}")
        
        print("")
        if all(status == "OK" for status, _ in checks):
            print("Frontend setup verified!")
        else:
            print("Some issues found. Fix them before running the frontend.")


def run_frontend_command(command: str, **kwargs):
    """Run frontend command."""
    runner = FrontendRunner()
    
    if command == "dev" or command == "start":
        runner.start_dev(port=kwargs.get("port"))
    elif command == "build":
        runner.build()
    elif command == "preview":
        runner.preview()
    elif command == "install":
        runner.install()
    elif command == "lint":
        runner.lint()
    elif command == "verify":
        runner.verify()
    else:
        print(f"Unknown frontend command: {command}")
        print("Available commands: dev, build, preview, install, lint, verify")
        sys.exit(1)
