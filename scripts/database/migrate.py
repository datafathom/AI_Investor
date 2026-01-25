#!/usr/bin/env python3
"""
Database Migration Runner
Automates database migrations for production deployments
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional
import json
from datetime import datetime

# Add project root to path
_project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_project_root))

from utils.database_manager import get_database_manager
from utils.core.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB


MIGRATIONS_DIR = _project_root / "migrations"
METADATA_FILE = MIGRATIONS_DIR / ".migration_metadata.json"


class MigrationRunner:
    """Manages database migrations."""
    
    def __init__(self):
        self.db = get_database_manager()
        self._ensure_migration_table()
    
    def _ensure_migration_table(self):
        """Create migration tracking table if it doesn't exist."""
        with self.db.pg_cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMPTZ DEFAULT NOW(),
                    description TEXT
                )
            """)
            self.db.pg_conn.commit()
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions."""
        with self.db.pg_cursor() as cur:
            cur.execute("SELECT version FROM schema_migrations ORDER BY applied_at")
            return [row[0] for row in cur.fetchall()]
    
    def get_pending_migrations(self) -> List[Path]:
        """Get list of pending migration files."""
        applied = set(self.get_applied_migrations())
        migrations = sorted(MIGRATIONS_DIR.glob("*.sql"))
        return [m for m in migrations if m.stem not in applied]
    
    def apply_migration(self, migration_file: Path) -> bool:
        """Apply a single migration file."""
        print(f"📝 Applying migration: {migration_file.name}")
        
        try:
            # Read migration SQL
            with open(migration_file, 'r') as f:
                sql = f.read()
            
            # Execute migration
            with self.db.pg_cursor() as cur:
                cur.execute(sql)
                self.db.pg_conn.commit()
            
            # Record migration
            with self.db.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO schema_migrations (version, description)
                    VALUES (%s, %s)
                """, (migration_file.stem, migration_file.name))
                self.db.pg_conn.commit()
            
            print(f"✅ Migration applied: {migration_file.name}")
            return True
            
        except Exception as e:
            print(f"❌ Migration failed: {migration_file.name}")
            print(f"   Error: {e}")
            self.db.pg_conn.rollback()
            return False
    
    def migrate_up(self, target_version: Optional[str] = None) -> bool:
        """Apply all pending migrations."""
        pending = self.get_pending_migrations()
        
        if not pending:
            print("✅ No pending migrations")
            return True
        
        print(f"📋 Found {len(pending)} pending migration(s)")
        
        for migration in pending:
            if target_version and migration.stem > target_version:
                break
            
            if not self.apply_migration(migration):
                return False
        
        print("✅ All migrations applied successfully")
        return True
    
    def migrate_down(self, target_version: str) -> bool:
        """Rollback to a specific version."""
        applied = self.get_applied_migrations()
        
        if target_version not in applied:
            print(f"❌ Version {target_version} not found in applied migrations")
            return False
        
        # Find rollback file
        rollback_file = MIGRATIONS_DIR / f"{target_version}_rollback.sql"
        
        if not rollback_file.exists():
            print(f"⚠️  Rollback file not found: {rollback_file.name}")
            print("   Manual rollback required")
            return False
        
        print(f"🔄 Rolling back to: {target_version}")
        
        try:
            with open(rollback_file, 'r') as f:
                sql = f.read()
            
            with self.db.pg_cursor() as cur:
                cur.execute(sql)
                self.db.pg_conn.commit()
            
            # Remove migration record
            with self.db.pg_cursor() as cur:
                cur.execute("DELETE FROM schema_migrations WHERE version = %s", (target_version,))
                self.db.pg_conn.commit()
            
            print(f"✅ Rollback completed: {target_version}")
            return True
            
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            self.db.pg_conn.rollback()
            return False
    
    def status(self):
        """Show migration status."""
        applied = self.get_applied_migrations()
        pending = self.get_pending_migrations()
        
        print("\n📊 Migration Status:")
        print(f"   Applied: {len(applied)}")
        print(f"   Pending: {len(pending)}")
        
        if applied:
            print("\n✅ Applied Migrations:")
            for version in applied:
                print(f"   - {version}")
        
        if pending:
            print("\n⏳ Pending Migrations:")
            for migration in pending:
                print(f"   - {migration.name}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration Runner')
    parser.add_argument('command', choices=['up', 'down', 'status'], help='Migration command')
    parser.add_argument('--target', help='Target version for up/down')
    
    args = parser.parse_args()
    
    runner = MigrationRunner()
    
    if args.command == 'up':
        success = runner.migrate_up(args.target)
        sys.exit(0 if success else 1)
    elif args.command == 'down':
        if not args.target:
            print("❌ --target required for rollback")
            sys.exit(1)
        success = runner.migrate_down(args.target)
        sys.exit(0 if success else 1)
    elif args.command == 'status':
        runner.status()
        sys.exit(0)


if __name__ == '__main__':
    main()
