"""
Database Runner
Handles all database operations via CLI
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


class DatabaseRunner:
    """Manages database operations."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent
    
    def migrate(self, direction="up", migration_id=None):
        """Run database migrations."""
        print(f"Running database migrations ({direction})...")
        print("")
        
        migrate_script = self.project_root / "scripts" / "database" / "migrate.py"
        
        if migrate_script.exists():
            if direction == "up":
                subprocess.run([sys.executable, str(migrate_script), "up"], check=True)
            elif direction == "down":
                if migration_id:
                    subprocess.run([sys.executable, str(migrate_script), "down", migration_id], check=True)
                else:
                    print("Migration ID required for rollback")
                    sys.exit(1)
            else:
                print(f"Invalid direction: {direction}. Use 'up' or 'down'")
                sys.exit(1)
        else:
            # Try migration manager
            manager_script = self.project_root / "scripts" / "database" / "migration_manager.py"
            if manager_script.exists():
                if direction == "up":
                    subprocess.run([sys.executable, str(manager_script), "migrate", "up"], check=True)
                else:
                    if migration_id:
                        subprocess.run([sys.executable, str(manager_script), "rollback", "--migration-id", migration_id], check=True)
                    else:
                        print("Migration ID required for rollback")
                        sys.exit(1)
            else:
                print("Migration scripts not found")
                sys.exit(1)
    
    def backup(self, backup_type="all"):
        """Backup database."""
        print(f"Backing up database ({backup_type})...")
        print("")
        
        backup_script = self.project_root / "scripts" / "database" / "backup.py"
        
        if backup_script.exists():
            subprocess.run([sys.executable, str(backup_script), "--type", backup_type], check=True)
        else:
            print("Backup script not found")
            sys.exit(1)
    
    def restore(self, file_path, db_type="postgres"):
        """Restore database from backup."""
        print(f"Restoring database from backup...")
        print(f"File: {file_path}")
        print(f"Type: {db_type}")
        print("")
        
        restore_script = self.project_root / "scripts" / "database" / "restore.py"
        
        if restore_script.exists():
            subprocess.run([sys.executable, str(restore_script), "--file", file_path, "--type", db_type], check=True)
        else:
            print("Restore script not found")
            sys.exit(1)
    
    def status(self):
        """Check migration status."""
        print("Checking migration status...")
        print("")
        
        manager_script = self.project_root / "scripts" / "database" / "migration_manager.py"
        
        if manager_script.exists():
            subprocess.run([sys.executable, str(manager_script), "status"], check=False)
        else:
            migrate_script = self.project_root / "scripts" / "database" / "migrate.py"
            if migrate_script.exists():
                subprocess.run([sys.executable, str(migrate_script), "status"], check=False)
            else:
                print("Migration scripts not found")
                sys.exit(1)


def db_reinit(**kwargs):
    """
    DESTRUCTIVE: Full infrastructure reset.
    1. Down with volumes (Prune)
    2. Nuke host data folders (sudo rm -rf data/postgres data/neo4j)
    3. Up with LAN IP binding
    4. Wait for PG readiness
    5. Migrate
    6. Seed
    """
    project_root = Path(__file__).parent.parent.parent
    
    print("\n" + "="*60)
    print("🔥 DESTRUCTIVE RESET: Re-initializing Database Suite")
    print("="*60)
    
    # 1. Docker Down with volumes
    from .docker_control import docker_down, docker_up
    print("\n[Stage 1/6] Stopping Docker containers and pruning volumes...")
    docker_down(volumes=True)
    
    # 2. Nuke host data folders (requires sudo for root-owned files from Docker)
    print("\n[Stage 2/6] Nuking host data folders (requires sudo)...")
    data_folders = ["data/postgres", "data/neo4j"]
    for folder in data_folders:
        full_path = project_root / folder
        if full_path.exists():
            print(f"   Deleting {folder}...")
            try:
                subprocess.run(["sudo", "rm", "-rf", str(full_path)], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to delete {folder}: {e}")
                sys.exit(1)
    
    # 3. Docker Up with LAN IP
    print("\n[Stage 3/6] Starting containers with LAN IP distribution...")
    # Load .env to get DOCKER_BIND_IP for environment
    from dotenv import load_dotenv
    load_dotenv(project_root / ".env")
    
    # Ensure current process has DOCKER_BIND_IP for subprocess calls
    os.environ["DOCKER_BIND_IP"] = os.getenv("DOCKER_BIND_IP", "127.0.0.1")
    docker_up(profile="full")
    
    # 4. Wait for PG readiness
    print("\n[Stage 4/6] Waiting for PostgreSQL readiness (Health Check)...")
    import time
    import socket
    import psycopg2
    
    pg_host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    pg_port = int(os.getenv("POSTGRES_PORT", "5432"))
    
    max_retries = 30
    retry_interval = 5
    print(f"   Checking {pg_host}:{pg_port}...")
    
    engine_ready = False
    for i in range(max_retries):
        try:
            with socket.create_connection((pg_host, pg_port), timeout=2):
                print(f"   ✅ Port {pg_port} is open. Checking database engine...")
                # Try simple connection check using psycopg2
                db_url = os.getenv("DATABASE_URL")
                conn = psycopg2.connect(db_url, connect_timeout=5)
                conn.close()
                print("   ✅ Database engine is ready!")
                engine_ready = True
                break
        except (socket.timeout, ConnectionRefusedError, psycopg2.Error):
            print(f"   [Retry {i+1}/{max_retries}] Still initializing... ({retry_interval}s)")
            time.sleep(retry_interval)
            
    if not engine_ready:
        print("❌ Database failed to stabilize in time.")
        sys.exit(1)
        
    # 5. Run Migrations
    print("\n[Stage 5/6] Running schema migrations...")
    runner = DatabaseRunner()
    runner.migrate(direction="up")
    
    # 6. Seed Database
    print("\n[Stage 6/6] Seeding data (Users, Advisors)...")
    from .seed_db import run_seed_db
    run_seed_db()
    
    print("\n" + "="*60)
    print("✨ DATABASE RESTORED SUCCESSFULLY!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # If run directly, default to migrate up
    run_db_command("migrate")
