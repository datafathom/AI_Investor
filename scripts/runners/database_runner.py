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


def run_db_command(command: str = "migrate", **kwargs):
    """Run database command."""
    runner = DatabaseRunner()
    
    if command == "migrate":
        direction = kwargs.get("direction", "up")
        migration_id = kwargs.get("migration_id")
        runner.migrate(direction=direction, migration_id=migration_id)
    elif command == "backup":
        backup_type = kwargs.get("type", "all")
        runner.backup(backup_type=backup_type)
    elif command == "restore":
        file_path = kwargs.get("file")
        if not file_path:
            print("Backup file path required (--file)")
            sys.exit(1)
        db_type = kwargs.get("type", "postgres")
        runner.restore(file_path, db_type)
    elif command == "status":
        runner.status()
    else:
        print(f"Unknown database command: {command}")
        print("Available commands: migrate, backup, restore, status")
        sys.exit(1)
