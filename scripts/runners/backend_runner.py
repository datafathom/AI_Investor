"""
Backend Runner
Handles all backend operations via CLI
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


class BackendRunner:
    """Manages backend operations."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
    
    def start_dev(self, port=None, host=None):
        """Start backend development server."""
        print("Starting backend development server...")
        print(f"Directory: {self.project_root}")
        if port:
            print(f"Port: {port}")
        if host:
            print(f"Host: {host}")
        print("")
        
        env = os.environ.copy()
        if port:
            env['FLASK_RUN_PORT'] = str(port)
        if host:
            env['FLASK_RUN_HOST'] = host
        
        try:
            # Try Flask development server
            subprocess.run(
                [sys.executable, "-m", "flask", "run"],
                cwd=self.project_root,
                env=env,
                check=False
            )
        except FileNotFoundError:
            # Try direct Python module
            subprocess.run(
                [sys.executable, "-m", "web.app"],
                cwd=self.project_root,
                env=env,
                check=False
            )
    
    def start_prod(self, workers=None, port=None):
        """Start backend production server with Gunicorn."""
        print("Starting backend production server...")
        print(f"Directory: {self.project_root}")
        if workers:
            print(f"Workers: {workers}")
        if port:
            print(f"Port: {port}")
        print("")
        
        workers = workers or os.getenv('GUNICORN_WORKERS', '4')
        port = port or os.getenv('PORT', '5050')
        
        cmd = [
            sys.executable, "-m", "gunicorn",
            "web.wsgi:app",
            f"--workers={workers}",
            f"--bind=0.0.0.0:{port}",
            "--worker-class=gevent",
            "--worker-connections=1000",
            "--timeout=120",
            "--keepalive=5"
        ]
        
        try:
            subprocess.run(cmd, cwd=self.project_root, check=False)
        except FileNotFoundError:
            print("Gunicorn not installed. Install with: pip install gunicorn gevent")
            sys.exit(1)
    
    def install(self):
        """Install backend dependencies."""
        print("Installing backend dependencies...")
        print(f"Directory: {self.project_root}")
        print("")
        
        requirements = self.project_root / "requirements.txt"
        if not requirements.exists():
            print("requirements.txt not found")
            sys.exit(1)
        
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements)],
            check=True
        )
        print("Dependencies installed!")
    
    def verify(self):
        """Verify backend setup."""
        print("Verifying backend setup...")
        print("")
        
        checks = []
        
        # Check Python version
        version = sys.version_info
        if version.major >= 3 and version.minor >= 11:
            checks.append(("OK", f"Python version: {version.major}.{version.minor}.{version.micro}"))
        else:
            checks.append(("WARN", f"Python version: {version.major}.{version.minor}.{version.micro} (3.11+ recommended)"))
        
        # Check requirements.txt
        requirements = self.project_root / "requirements.txt"
        if requirements.exists():
            checks.append(("OK", "requirements.txt exists"))
        else:
            checks.append(("ERROR", "requirements.txt missing"))
        
        # Check web/app.py
        app_file = self.project_root / "web" / "app.py"
        if app_file.exists():
            checks.append(("OK", "web/app.py exists"))
        else:
            checks.append(("ERROR", "web/app.py missing"))
        
        # Check if Flask is installed
        try:
            import flask
            checks.append(("OK", f"Flask installed: {flask.__version__}"))
        except ImportError:
            checks.append(("ERROR", "Flask not installed (run: cli backend install)"))
        
        # Print results
        for status, message in checks:
            print(f"[{status}] {message}")
        
        print("")
        if all(status == "OK" for status, _ in checks):
            print("Backend setup verified!")
        else:
            print("Some issues found. Fix them before running the backend.")


def run_backend_command(command: str = "dev", **kwargs):
    """Run backend command."""
    runner = BackendRunner()
    
    if command == "dev" or command == "start":
        runner.start_dev(port=kwargs.get("port"), host=kwargs.get("host"))
    elif command == "prod" or command == "production":
        runner.start_prod(workers=kwargs.get("workers"), port=kwargs.get("port"))
    elif command == "install":
        runner.install()
    elif command == "verify":
        runner.verify()
    else:
        print(f"Unknown backend command: {command}")
        print("Available commands: dev, prod, install, verify")
        sys.exit(1)
