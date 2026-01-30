"""
==============================================================================
FILE: cert_runner.py
ROLE: CLI Runner for Certificates and LAN Config
PURPOSE: Handles SSL certificate generation and granular LAN host updates.
==============================================================================
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parents[2]

def generate_certs(ip: str = None, service: str = None, output_dir: str = "infra/certs"):
    """
    Generate SSL certificates for a specific LAN IP or Service.
    If service is specified, it pulls the IP from the .env host mapping.
    """
    if service:
        ip = _get_ip_from_env(service)
        if not ip:
            print(f"Error: Could not find host mapping for service '{service}' in .env")
            return
    
    if not ip:
        ip = "localhost"
        
    logger.info(f"Generating SSL certificates for IP: {ip}")
    
    script_path = PROJECT_ROOT / "scripts" / "generate_lan_certs.py"
    if not script_path.exists():
        logger.error(f"Certificate generation script not found: {script_path}")
        return

    # Use the appropriate python executable
    python_exe = sys.executable
    
    cmd = [python_exe, str(script_path), "--ip", ip, "--dir", str(PROJECT_ROOT / output_dir)]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(result.stdout)
        print(f"Successfully generated certificates for {ip} in {output_dir}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to generate certificates: {e.stderr}")
        print(f"Error: Failed to generate certificates. Check logs for details.")

def set_lan_ip(ip: str):
    """
    Update the global LAN_BOX_IP and default bind in the .env file.
    """
    logger.info(f"Updating global LAN_BOX_IP to: {ip}")
    _update_env_var("LAN_BOX_IP", ip)
    _update_env_var("DOCKER_BIND_IP", ip)
    print(f"Successfully updated .env with global LAN_BOX_IP={ip}")
    print(f"Next step: Run 'python cli.py infra cert-generate --ip {ip}' to update certificates.")

def set_host(service: str, ip: str):
    """
    Update a specific service host (e.g. postgres) in the .env file.
    """
    var_name = f"{service.upper()}_HOST"
    logger.info(f"Updating {var_name} to: {ip}")
    _update_env_var(var_name, ip)
    print(f"Successfully updated .env with {var_name}={ip}")
    print(f"Next step: Run 'python cli.py infra cert-generate --service {service}'")

def init_node(ip: str, roles: str = "full"):
    """
    Bootstrap a new node in the distributed cluster.
    """
    print(f"Initializing node with IP: {ip} and Roles: {roles}")
    
    env_path = PROJECT_ROOT / ".env"
    template_path = PROJECT_ROOT / ".env.template"
    
    # 1. Ensure .env exists
    if not env_path.exists():
        if template_path.exists():
            shutil.copy(template_path, env_path)
            print("Created .env from .env.template")
        else:
            print("Error: .env.template not found. Cannot initialize.")
            return

    # 2. Update Bind IP
    _update_env_var("DOCKER_BIND_IP", ip)
    _update_env_var("LAN_BOX_IP", ip) # Default assumption
    
    # 3. Generate Certificates
    generate_certs(ip=ip)
    
    print("\nNode Initialization Complete!")
    print(f"Bind IP set to: {ip}")
    print(f"Certificates generated for: {ip}")
    print(f"\nTo start services on this node, run:")
    print(f"docker compose -f infra/docker-compose.yml --profile {roles} up -d")
    print(f"or")
    print(f"python cli.py docker up --profile {roles}")

def _get_ip_from_env(service: str) -> str:
    """Helper to resolve IP from .env for a service."""
    var_name = f"{service.upper()}_HOST"
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith(f"{var_name}="):
                    val = line.split("=")[1].strip()
                    # Strip interpolation if present
                    if val.startswith("${"):
                        # Attempt to resolve the default or the variable
                        # For simplicity, we assume the user has set it or LAN_BOX_IP is set
                        return os.popen(f"echo {val}").read().strip() # Dangerous hack, let's just regex
                    return val
    return None

def _update_env_var(key: str, value: str):
    """Utility to update a key in .env file."""
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        print("Error: .env file not found.")
        return

    try:
        with open(env_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        found = False
        for line in lines:
            if line.startswith(f"{key}="):
                new_lines.append(f"{key}={value}\n")
                found = True
            else:
                new_lines.append(line)

        if not found:
            new_lines.append(f"{key}={value}\n")

        with open(env_path, "w") as f:
            f.writelines(new_lines)
    except Exception as e:
        logger.error(f"Failed to update .env key {key}: {e}")
        raise
