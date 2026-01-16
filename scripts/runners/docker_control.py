"""
Docker Infrastructure Management

This module provides CLI commands for managing Docker containers.
"""

import subprocess
import os
import sys

def docker_up():
    """Start Docker containers using docker-compose."""
    compose_file = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'docker-compose.yml')
    
    if not os.path.exists(compose_file):
        print(f"❌ Error: docker-compose.yml not found at {compose_file}")
        sys.exit(1)
    
    print("🚀 Starting Docker containers...")
    try:
        result = subprocess.run(
            ['docker-compose', '-f', compose_file, 'up', '-d'],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("✅ Docker containers started successfully!")
        print("\n📊 Services running on localhost:")
        print("   - Kafka: 127.0.0.1:9092")
        print("   - PostgreSQL: 127.0.0.1:5432")
        print("   - Neo4j HTTP: 127.0.0.1:7474")
        print("   - Neo4j Bolt: 127.0.0.1:7687")
        print("   - Backend API: 127.0.0.1:5000")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting containers: {e.stderr}")
        sys.exit(1)

def docker_down():
    """Stop Docker containers using docker-compose."""
    compose_file = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'docker-compose.yml')
    
    if not os.path.exists(compose_file):
        print(f"❌ Error: docker-compose.yml not found at {compose_file}")
        sys.exit(1)
    
    print("🛑 Stopping Docker containers...")
    try:
        result = subprocess.run(
            ['docker-compose', '-f', compose_file, 'down'],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print("✅ Docker containers stopped successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error stopping containers: {e.stderr}")
        sys.exit(1)

def docker_status():
    """Show status of Docker containers."""
    compose_file = os.path.join(os.path.dirname(__file__), '..', '..', 'infra', 'docker-compose.yml')
    
    if not os.path.exists(compose_file):
        print(f"❌ Error: docker-compose.yml not found at {compose_file}")
        sys.exit(1)
    
    print("📊 Docker container status:")
    try:
        result = subprocess.run(
            ['docker-compose', '-f', compose_file, 'ps'],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error checking status: {e.stderr}")
        sys.exit(1)
