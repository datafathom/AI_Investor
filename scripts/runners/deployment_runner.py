"""
Deployment Runner
Handles all deployment operations via CLI
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


class DeploymentRunner:
    """Manages deployment operations."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
    
    def deploy_prod(self, env_file=None):
        """Deploy to production."""
        print("Deploying to production...")
        print("")
        
        deploy_script = self.project_root / "scripts" / "deployment" / "prod_deploy.sh"
        
        if deploy_script.exists():
            if sys.platform == "win32":
                # Use PowerShell on Windows
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(deploy_script)])
            else:
                subprocess.run(["bash", str(deploy_script)], check=True)
        else:
            print("Deployment script not found")
            print("Run: docker-compose -f infra/docker-compose.prod.yml up -d")
            sys.exit(1)
    
    def rollback(self):
        """Rollback deployment."""
        print("Rolling back deployment...")
        print("")
        
        rollback_script = self.project_root / "scripts" / "deployment" / "rollback.sh"
        
        if rollback_script.exists():
            if sys.platform == "win32":
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(rollback_script)])
            else:
                subprocess.run(["bash", str(rollback_script)], check=True)
        else:
            print("Rollback script not found")
            sys.exit(1)
    
    def build_images(self):
        """Build Docker images."""
        print("Building Docker images...")
        print("")
        
        # Build backend
        print("Building backend image...")
        subprocess.run([
            "docker", "build",
            "-f", "infra/Dockerfile.backend.prod",
            "-t", "ai-investor-backend:latest",
            "."
        ], cwd=self.project_root, check=True)
        
        # Build frontend
        print("Building frontend image...")
        subprocess.run([
            "docker", "build",
            "-f", "frontend2/Dockerfile.prod",
            "-t", "ai-investor-frontend:latest",
            "frontend2"
        ], cwd=self.project_root, check=True)
        
        print("Images built successfully!")
    
    def health_check(self):
        """Check deployment health."""
        print("Checking deployment health...")
        print("")
        
        import requests
        
        endpoints = [
            ("Backend", "http://localhost:5050/api/v1/health"),
            ("Frontend", "http://localhost:3000/health"),
        ]
        
        for name, url in endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[OK] {name}: Healthy")
                else:
                    print(f"[WARN] {name}: Status {response.status_code}")
            except Exception as e:
                print(f"[ERROR] {name}: {e}")


def run_deployment_command(command: str = "prod", **kwargs):
    """Run deployment command."""
    runner = DeploymentRunner()
    
    if command == "prod" or command == "production":
        runner.deploy_prod(env_file=kwargs.get("env"))
    elif command == "rollback":
        runner.rollback()
    elif command == "build":
        runner.build_images()
    elif command == "health":
        runner.health_check()
    else:
        print(f"Unknown deployment command: {command}")
        print("Available commands: prod, rollback, build, health")
        sys.exit(1)
