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
        cmd = ['docker-compose', '-f', compose_file, '--profile', profile, 'up', '-d', '--remove-orphans']
        if build:
            cmd.append('--build')
            
        # Run without capture_output so user sees real-time progress
        subprocess.run(
            cmd,
            check=True
        )
        print("OK Docker Infrastructure started successfully!")
        print("\n Services running on localhost:")
        print("   - Kafka: 127.0.0.1:9092")
        print("   - PostgreSQL: 127.0.0.1:5432")
        print("   - Redis: 127.0.0.1:6379")
        print("   - Neo4j HTTP: 127.0.0.1:7474")
        print("   - Neo4j Bolt: 127.0.0.1:7687")
        print("\n👉 Remember to start Backend and Frontend on host separately.")
    except subprocess.CalledProcessError:
        print(f"ERROR Error starting containers.")
        sys.exit(1)

def docker_down(volumes: bool = False):
    """Stop Docker containers using docker-compose."""
    compose_file = _get_compose_file()
    
    print("🛑 Stopping Docker containers...")
    cmd = ['docker-compose', '-f', compose_file, 'down']
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
    
    cmd = ['docker-compose', '-f', compose_file, 'logs']
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
