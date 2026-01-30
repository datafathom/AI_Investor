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

def docker_up(profile: str = "full", build: bool = False):
    """Start Docker containers using docker-compose with a specific profile."""
    compose_file = _get_compose_file()
    
    build_msg = " and rebuilding images" if build else ""
    print(f" Starting Docker Infrastructure Containers with profile '{profile}'{build_msg}...")
    
    # Force stop first to ensure clean state
    print("🧹 Pre-flight cleanup: Stopping any running containers...")
    try:
        docker_down()
    except SystemExit:
        pass # Ignore exit from docker_down if it succeeds
        
    try:
        _load_env_to_environ()
        env_file = _get_env_file()
        cmd = ['docker', 'compose', '--env-file', env_file, '-f', compose_file, '--profile', profile, 'up', '-d', '--remove-orphans']
        if build:
            cmd.append('--build')
            
        # Run without capture_output so user sees real-time progress
        subprocess.run(
            cmd,
            check=True
        )
        
        # Get bind IP for display
        bind_ip = os.getenv("DOCKER_BIND_IP", "127.0.0.1")
        
        print(f"OK Docker Infrastructure started successfully!")
        print(f"\n Services listening on {bind_ip}:")
        print(f"   - Kafka: {bind_ip}:9092")
        print(f"   - PostgreSQL: {bind_ip}:5432")
        print(f"   - Redis: {bind_ip}:6379")
        print(f"   - Neo4j HTTP: {bind_ip}:7474")
        print(f"   - Neo4j Bolt: {bind_ip}:7687")
        print("\n👉 Remember to start Backend and Frontend on host separately.")
    except subprocess.CalledProcessError:
        print(f"ERROR Error starting containers.")
        sys.exit(1)

def docker_down(volumes: bool = False):
    """Stop Docker containers using docker-compose."""
    compose_file = _get_compose_file()
    
    print("🛑 Stopping Docker containers...")
    env_file = _get_env_file()
    cmd = ['docker', 'compose', '--env-file', env_file, '-f', compose_file, 'down']
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
            ['docker', 'ps', '--format', 'table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}'],
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
    
    cmd = ['docker', 'compose', '--env-file', env_file, '-f', compose_file, 'logs']
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
