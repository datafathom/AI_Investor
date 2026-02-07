"""
Docker Infrastructure Management

This module provides CLI commands for managing Docker containers.
"""

import subprocess
import os
import sys

def _get_compose_file():
    """Helper to get the path to docker-compose.yml"""
    compose_file = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'docker-compose.yml')
    if not os.path.exists(compose_file):
        print(f"ERROR Error: docker-compose.yml not found at {compose_file}")
        sys.exit(1)
    return compose_file

def _get_env_file():
    """Helper to get the path to the root .env file"""
    env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    if not os.path.exists(env_file):
        print(f"WARNING Warning: .env file not found at {env_file}")
    return env_file

def _load_env_to_environ():
    """Load environment variables from the root .env file into os.environ."""
    env_file = _get_env_file()
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k] = v.strip().strip('"').strip("'")

def docker_up(profile: str = "full", build: bool = False, service: str = None):
    """Start Docker containers using docker-compose. Can target a profile or a single service."""
    compose_file = _get_compose_file()
    
    target = f"service '{service}'" if service else f"profile '{profile}'"
    build_msg = " and rebuilding images" if build else ""
    print(f" Starting Docker Infrastructure {target}{build_msg}...")
    
    # Pre-flight cleanup if starting a profile (to ensure clean env)
    if not service:
        print("🧹 Pre-flight cleanup: Stopping all profile containers...")
        try:
            docker_down()
        except SystemExit:
            pass
        
    try:
        _load_env_to_environ()
        env_file = _get_env_file()
        
        cmd = ['sudo', 'docker', 'compose', '--env-file', env_file, '-f', compose_file]
        
        # If not a specific service, use the profile
        if not service:
            cmd.extend(['--profile', profile])
            
        cmd.extend(['up', '-d', '--remove-orphans'])
        
        if build:
            cmd.append('--build')
            
        if service:
            # Map user-friendly names to actual service names if needed
            service_map = {"slackbot": "slack-bot"}
            actual_service = service_map.get(service.lower(), service.lower())
            cmd.append(actual_service)
            
        subprocess.run(cmd, check=True)
        print(f"OK Docker {target} started successfully!")
    except subprocess.CalledProcessError:
        print(f"ERROR Error starting {target}.")
        sys.exit(1)

def docker_service_up(service: str, build: bool = False):
    """Entry point for starting a single service."""
    docker_up(service=service, build=build)

def docker_service_down(service: str):
    """Stop a single Docker service."""
    compose_file = _get_compose_file()
    env_file = _get_env_file()
    
    # Map names
    service_map = {"slackbot": "slack-bot"}
    actual_service = service_map.get(service.lower(), service.lower())
    
    print(f"🛑 Stopping Docker service '{actual_service}'...")
    cmd = ['sudo', 'docker', 'compose', '--env-file', env_file, '-f', compose_file, 'stop', actual_service]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"OK Service '{actual_service}' stopped.")
    except subprocess.CalledProcessError:
        print(f"ERROR Error stopping service.")
        sys.exit(1)

def docker_down(volumes: bool = False):
    """Stop Docker containers using docker-compose."""
    compose_file = _get_compose_file()
    
    print("🛑 Stopping Docker containers...")
    env_file = _get_env_file()
    cmd = ['sudo', 'docker', 'compose', '--env-file', env_file, '-f', compose_file, 'down']
    if volumes:
        print("🕯️  Pruning volumes for a clean slate...")
        cmd.append('-v')
        
    try:
        subprocess.run(
            cmd,
            check=True
        )
        print("OK Docker containers stopped successfully!")
    except subprocess.CalledProcessError as e:
        print(f"ERROR Error stopping containers.")
        sys.exit(1)

def docker_status():
    """Show status of Docker containers (alias for docker_ps)."""
    docker_ps()

def docker_ps():
    """Show status of Docker containers in a specific table format."""
    print(" Docker container status:")
    try:
        subprocess.run(
            ['sudo', 'docker', 'ps', '--format', 'table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}'],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"ERROR Error running docker ps: {e}")
        sys.exit(1)

def docker_logs(service: str = "", follow: bool = True):
    """
    View or follow Docker container logs.
    
    Args:
        service: Optional specific service name (e.g., 'backend')
        follow: Whether to stream logs (default True)
    """
    compose_file = _get_compose_file()
    env_file = _get_env_file()
    
    cmd = ['sudo', 'docker', 'compose', '--env-file', env_file, '-f', compose_file, 'logs']
    if follow:
        cmd.append('-f')
    if service:
        cmd.append(service)
        
    print(f" Fetching logs{' for ' + service if service else ''}...")
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Stopped following logs.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR Error fetching logs.")
        sys.exit(1)

def docker_lanbox_up(profile: str = "full", build: bool = False):
    """
    Shorthand to start Docker containers specifically for a LAN Node setup.
    This assumes LAN_BOX_IP or DOCKER_BIND_IP is already set in .env.
    """
    print("🚀 Starting LAN Node Docker Infrastructure...")
    
    # We can perform additional validation here if needed, 
    # e.g., checking if DOCKER_BIND_IP is set to something other than 127.0.0.1
    _load_env_to_environ()
    bind_ip = os.environ.get("DOCKER_BIND_IP", "127.0.0.1")
    
    if bind_ip == "127.0.0.1":
        print("⚠️ Warning: DOCKER_BIND_IP is still set to 127.0.0.1.")
        print("   If this is the LAN Node, you should run 'python cli.py infra set-lan-ip [IP]' first.")
    else:
        print(f"📍 Binding services to LAN IP: {bind_ip}")

    # Delegate to the main docker_up logic
    docker_up(profile=profile, build=build)

