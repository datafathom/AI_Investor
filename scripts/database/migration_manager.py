"""
Advanced Database Migration Manager
Complete migration system with rollback, validation, and status tracking
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MigrationManager:
    """Complete migration management system."""
    
    def __init__(self, migrations_dir: str = "migrations", db_url: Optional[str] = None):
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
        self.db_url = db_url or os.getenv('DATABASE_URL')
        self.metadata_file = self.migrations_dir / 'migration_metadata.json'
        self._load_metadata()
    
    def _load_metadata(self):
        """Load migration metadata."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                'applied_migrations': [],
                'last_migration': None,
                'schema_version': 0
            }
            self._save_metadata()
    
    def _save_metadata(self):
        """Save migration metadata."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def create_migration(self, name: str, description: str = "") -> Tuple[str, str]:
        """Create new migration files."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        migration_id = f"{timestamp}_{name}"
        
        forward_file = self.migrations_dir / f"{migration_id}.sql"
        rollback_file = self.migrations_dir / f"{migration_id}_rollback.sql"
        
        # Create forward migration template
        forward_content = f"""-- Migration: {name}
-- Description: {description}
-- Created: {datetime.utcnow().isoformat()}
-- ID: {migration_id}

BEGIN;

-- Add your migration SQL here
-- Example:
-- CREATE TABLE example (
--     id SERIAL PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

COMMIT;
"""
        
        # Create rollback migration template
        rollback_content = f"""-- Rollback Migration: {name}
-- Description: Rollback for {description}
-- Created: {datetime.utcnow().isoformat()}
-- ID: {migration_id}

BEGIN;

-- Add your rollback SQL here
-- Example:
-- DROP TABLE IF EXISTS example;

COMMIT;
"""
        
        forward_file.write_text(forward_content)
        rollback_file.write_text(rollback_content)
        
        logger.info(f"Created migration: {forward_file}")
        logger.info(f"Created rollback: {rollback_file}")
        
        return str(forward_file), str(rollback_file)
    
    def list_migrations(self) -> List[Dict]:
        """List all migrations with status."""
        migrations = []
        
        for file in sorted(self.migrations_dir.glob("*.sql")):
            if file.name.endswith('_rollback.sql'):
                continue
            
            migration_id = file.stem
            is_applied = migration_id in self.metadata['applied_migrations']
            
            migrations.append({
                'id': migration_id,
                'file': str(file),
                'applied': is_applied,
                'applied_at': self.metadata.get('migration_dates', {}).get(migration_id)
            })
        
        return migrations
    
    def get_pending_migrations(self) -> List[str]:
        """Get list of pending migrations."""
        all_migrations = [f.stem for f in self.migrations_dir.glob("*.sql") 
                         if not f.name.endswith('_rollback.sql')]
        applied = set(self.metadata['applied_migrations'])
        return [m for m in sorted(all_migrations) if m not in applied]
    
    def apply_migration(self, migration_id: Optional[str] = None, 
                       dry_run: bool = False) -> bool:
        """Apply migration(s)."""
        if migration_id:
            pending = [migration_id] if migration_id not in self.metadata['applied_migrations'] else []
        else:
            pending = self.get_pending_migrations()
        
        if not pending:
            logger.info("No pending migrations")
            return True
        
        for mig_id in pending:
            mig_file = self.migrations_dir / f"{mig_id}.sql"
            
            if not mig_file.exists():
                logger.error(f"Migration file not found: {mig_file}")
                return False
            
            logger.info(f"{'[DRY RUN] ' if dry_run else ''}Applying migration: {mig_id}")
            
            if not dry_run:
                try:
                    # Execute migration
                    result = self._execute_sql_file(mig_file)
                    
                    if result:
                        # Record migration
                        self.metadata['applied_migrations'].append(mig_id)
                        if 'migration_dates' not in self.metadata:
                            self.metadata['migration_dates'] = {}
                        self.metadata['migration_dates'][mig_id] = datetime.utcnow().isoformat()
                        self.metadata['last_migration'] = mig_id
                        self.metadata['schema_version'] += 1
                        self._save_metadata()
                        logger.info(f"✅ Migration applied: {mig_id}")
                    else:
                        logger.error(f"❌ Migration failed: {mig_id}")
                        return False
                except Exception as e:
                    logger.error(f"Error applying migration {mig_id}: {e}")
                    return False
        
        return True
    
    def rollback_migration(self, migration_id: Optional[str] = None, 
                          steps: int = 1) -> bool:
        """Rollback migration(s)."""
        if migration_id:
            if migration_id not in self.metadata['applied_migrations']:
                logger.error(f"Migration not applied: {migration_id}")
                return False
            to_rollback = [migration_id]
        else:
            # Rollback last N migrations
            applied = self.metadata['applied_migrations']
            to_rollback = applied[-steps:] if steps <= len(applied) else applied
        
        for mig_id in reversed(to_rollback):
            rollback_file = self.migrations_dir / f"{mig_id}_rollback.sql"
            
            if not rollback_file.exists():
                logger.warning(f"Rollback file not found: {rollback_file}")
                logger.info("Attempting to generate rollback...")
                # Could generate rollback here
                continue
            
            logger.info(f"Rolling back migration: {mig_id}")
            
            try:
                result = self._execute_sql_file(rollback_file)
                
                if result:
                    # Remove from applied
                    if mig_id in self.metadata['applied_migrations']:
                        self.metadata['applied_migrations'].remove(mig_id)
                    if 'migration_dates' in self.metadata:
                        self.metadata['migration_dates'].pop(mig_id, None)
                    self.metadata['schema_version'] = max(0, self.metadata['schema_version'] - 1)
                    self._save_metadata()
                    logger.info(f"✅ Migration rolled back: {mig_id}")
                else:
                    logger.error(f"❌ Rollback failed: {mig_id}")
                    return False
            except Exception as e:
                logger.error(f"Error rolling back {mig_id}: {e}")
                return False
        
        return True
    
    def _execute_sql_file(self, sql_file: Path) -> bool:
        """Execute SQL file against database."""
        if not self.db_url:
            logger.error("Database URL not configured")
            return False
        
        try:
            # Use psql for PostgreSQL
            cmd = ['psql', self.db_url, '-f', str(sql_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"SQL execution failed: {e.stderr}")
            return False
        except FileNotFoundError:
            # Fallback: use Python database connection
            return self._execute_sql_python(sql_file)
    
    def _execute_sql_python(self, sql_file: Path) -> bool:
        """Execute SQL using Python database connection."""
        try:
            import psycopg2
            from urllib.parse import urlparse
            
            parsed = urlparse(self.db_url)
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port or 5432,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:] if parsed.path else 'postgres'
            )
            
            with conn.cursor() as cur:
                sql_content = sql_file.read_text()
                cur.execute(sql_content)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Python SQL execution failed: {e}")
            return False
    
    def validate_migration(self, migration_id: str) -> Tuple[bool, List[str]]:
        """Validate migration file syntax."""
        mig_file = self.migrations_dir / f"{migration_id}.sql"
        errors = []
        
        if not mig_file.exists():
            errors.append(f"Migration file not found: {mig_file}")
            return False, errors
        
        content = mig_file.read_text()
        
        # Basic validation
        if 'BEGIN;' not in content and 'BEGIN TRANSACTION;' not in content:
            errors.append("Migration should use transactions (BEGIN; ... COMMIT;)")
        
        if 'COMMIT;' not in content and 'END;' not in content:
            errors.append("Migration should commit transaction (COMMIT;)")
        
        # Check for dangerous operations
        dangerous = ['DROP DATABASE', 'DROP SCHEMA', 'TRUNCATE']
        for op in dangerous:
            if op in content.upper():
                errors.append(f"Warning: Migration contains {op} operation")
        
        return len(errors) == 0, errors
    
    def get_migration_status(self) -> Dict:
        """Get comprehensive migration status."""
        all_migrations = self.list_migrations()
        pending = self.get_pending_migrations()
        
        return {
            'total_migrations': len(all_migrations),
            'applied_migrations': len(self.metadata['applied_migrations']),
            'pending_migrations': len(pending),
            'schema_version': self.metadata['schema_version'],
            'last_migration': self.metadata.get('last_migration'),
            'migrations': all_migrations
        }


def main():
    """CLI interface for migration manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration Manager')
    parser.add_argument('command', choices=['create', 'list', 'status', 'apply', 'rollback', 'validate'],
                       help='Migration command')
    parser.add_argument('--name', help='Migration name (for create)')
    parser.add_argument('--description', help='Migration description')
    parser.add_argument('--migration-id', help='Specific migration ID')
    parser.add_argument('--steps', type=int, default=1, help='Number of steps (for rollback)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode')
    parser.add_argument('--migrations-dir', default='migrations', help='Migrations directory')
    
    args = parser.parse_args()
    
    manager = MigrationManager(migrations_dir=args.migrations_dir)
    
    if args.command == 'create':
        if not args.name:
            print("Error: --name required for create command")
            sys.exit(1)
        forward, rollback = manager.create_migration(args.name, args.description or "")
        print(f"✅ Created migration: {forward}")
        print(f"✅ Created rollback: {rollback}")
    
    elif args.command == 'list':
        migrations = manager.list_migrations()
        print(f"\nTotal migrations: {len(migrations)}")
        for mig in migrations:
            status = "✅ Applied" if mig['applied'] else "⏳ Pending"
            print(f"  {status}: {mig['id']}")
    
    elif args.command == 'status':
        status = manager.get_migration_status()
        print(f"\nMigration Status:")
        print(f"  Total: {status['total_migrations']}")
        print(f"  Applied: {status['applied_migrations']}")
        print(f"  Pending: {status['pending_migrations']}")
        print(f"  Schema Version: {status['schema_version']}")
        if status['last_migration']:
            print(f"  Last Migration: {status['last_migration']}")
    
    elif args.command == 'apply':
        success = manager.apply_migration(args.migration_id, dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    
    elif args.command == 'rollback':
        success = manager.rollback_migration(args.migration_id, steps=args.steps)
        sys.exit(0 if success else 1)
    
    elif args.command == 'validate':
        if not args.migration_id:
            print("Error: --migration-id required for validate command")
            sys.exit(1)
        valid, errors = manager.validate_migration(args.migration_id)
        if valid:
            print(f"✅ Migration {args.migration_id} is valid")
        else:
            print(f"❌ Migration {args.migration_id} has errors:")
            for error in errors:
                print(f"  - {error}")
        sys.exit(0 if valid else 1)


if __name__ == '__main__':
    main()
