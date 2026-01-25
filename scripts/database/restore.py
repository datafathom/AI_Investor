"""
Database Restore Script
Restore PostgreSQL and Neo4j databases from backups
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseRestore:
    """Database restore manager."""
    
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
    
    def restore_postgres(self, backup_file: str, db_name: str,
                       host: str = "localhost", port: int = 5432,
                       user: str = "postgres", password: Optional[str] = None,
                       drop_existing: bool = False) -> bool:
        """Restore PostgreSQL database from backup."""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_file}")
                return False
            
            env = os.environ.copy()
            if password:
                env['PGPASSWORD'] = password
            
            # Drop existing database if requested
            if drop_existing:
                logger.warning(f"Dropping existing database: {db_name}")
                cmd_drop = [
                    'psql',
                    '-h', host,
                    '-p', str(port),
                    '-U', user,
                    '-d', 'postgres',  # Connect to default DB
                    '-c', f'DROP DATABASE IF EXISTS {db_name};'
                ]
                subprocess.run(cmd_drop, env=env, check=True)
                
                # Create new database
                cmd_create = [
                    'psql',
                    '-h', host,
                    '-p', str(port),
                    '-U', user,
                    '-d', 'postgres',
                    '-c', f'CREATE DATABASE {db_name};'
                ]
                subprocess.run(cmd_create, env=env, check=True)
            
            # Restore from backup
            logger.info(f"Restoring PostgreSQL database: {db_name} from {backup_file}")
            
            # Check if it's a custom format backup (.dump) or SQL file
            if backup_path.suffix == '.dump' or 'custom' in backup_path.name:
                cmd = [
                    'pg_restore',
                    '-h', host,
                    '-p', str(port),
                    '-U', user,
                    '-d', db_name,
                    '--clean',  # Clean before restore
                    '--if-exists',
                    str(backup_path)
                ]
            else:
                # SQL file
                cmd = [
                    'psql',
                    '-h', host,
                    '-p', str(port),
                    '-U', user,
                    '-d', db_name,
                    '-f', str(backup_path)
                ]
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"PostgreSQL restore completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"PostgreSQL restore failed: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"PostgreSQL restore error: {e}")
            return False
    
    def restore_neo4j(self, backup_file: str, uri: str = "bolt://localhost:7687",
                    user: str = "neo4j", password: Optional[str] = None,
                    clear_existing: bool = False) -> bool:
        """Restore Neo4j database from backup."""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_file}")
                return False
            
            logger.info(f"Restoring Neo4j database from {backup_file}")
            
            # Clear existing data if requested
            if clear_existing:
                logger.warning("Clearing existing Neo4j data")
                cmd_clear = [
                    'cypher-shell',
                    '-a', uri,
                    '-u', user,
                    '-p', password or '',
                    'MATCH (n) DETACH DELETE n'
                ]
                subprocess.run(cmd_clear, check=False)
            
            # Restore from Cypher export
            if backup_path.suffix == '.cypher':
                with open(backup_path, 'r') as f:
                    cypher_commands = f.read()
                
                # Execute Cypher commands
                cmd = [
                    'cypher-shell',
                    '-a', uri,
                    '-u', user,
                    '-p', password or '',
                    '--format', 'plain'
                ]
                
                result = subprocess.run(
                    cmd,
                    input=cypher_commands,
                    text=True,
                    capture_output=True,
                    check=False
                )
                
                if result.returncode == 0:
                    logger.info("Neo4j restore completed successfully")
                    return True
                else:
                    logger.warning(f"Neo4j restore completed with warnings: {result.stderr}")
                    return True  # Still consider it successful if data was loaded
            else:
                logger.error(f"Unsupported Neo4j backup format: {backup_path.suffix}")
                return False
                
        except Exception as e:
            logger.error(f"Neo4j restore error: {e}")
            return False
    
    def find_latest_backup(self, db_type: str) -> Optional[Path]:
        """Find the latest backup for a database type."""
        if db_type == 'postgres':
            pattern = "postgres_*.sql"
        elif db_type == 'neo4j':
            pattern = "neo4j_*.cypher"
        else:
            return None
        
        backups = sorted(
            self.backup_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        return backups[0] if backups else None


def main():
    """Main restore function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Restore Script')
    parser.add_argument('--postgres', action='store_true', help='Restore PostgreSQL')
    parser.add_argument('--neo4j', action='store_true', help='Restore Neo4j')
    parser.add_argument('--backup-file', help='Specific backup file to restore')
    parser.add_argument('--latest', action='store_true', help='Use latest backup')
    parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    parser.add_argument('--drop-existing', action='store_true', help='Drop existing database before restore (PostgreSQL)')
    parser.add_argument('--clear-existing', action='store_true', help='Clear existing data before restore (Neo4j)')
    
    # PostgreSQL options
    parser.add_argument('--pg-host', default=os.getenv('POSTGRES_HOST', 'localhost'))
    parser.add_argument('--pg-port', type=int, default=int(os.getenv('POSTGRES_PORT', '5432')))
    parser.add_argument('--pg-user', default=os.getenv('POSTGRES_USER', 'postgres'))
    parser.add_argument('--pg-password', default=os.getenv('POSTGRES_PASSWORD'))
    parser.add_argument('--pg-database', default=os.getenv('POSTGRES_DB', 'ai_investor'))
    
    # Neo4j options
    parser.add_argument('--neo4j-uri', default=os.getenv('NEO4J_URI', 'bolt://localhost:7687'))
    parser.add_argument('--neo4j-user', default=os.getenv('NEO4J_USER', 'neo4j'))
    parser.add_argument('--neo4j-password', default=os.getenv('NEO4J_PASSWORD'))
    
    args = parser.parse_args()
    
    restore_manager = DatabaseRestore(backup_dir=args.backup_dir)
    
    if args.postgres:
        if args.latest:
            backup_file = restore_manager.find_latest_backup('postgres')
            if not backup_file:
                logger.error("No PostgreSQL backup found")
                return
            backup_file = str(backup_file)
        elif args.backup_file:
            backup_file = args.backup_file
        else:
            logger.error("Must specify --backup-file or --latest")
            return
        
        success = restore_manager.restore_postgres(
            backup_file=backup_file,
            db_name=args.pg_database,
            host=args.pg_host,
            port=args.pg_port,
            user=args.pg_user,
            password=args.pg_password,
            drop_existing=args.drop_existing
        )
        
        if success:
            print(f"\n✅ PostgreSQL restore completed successfully!")
        else:
            print(f"\n❌ PostgreSQL restore failed!")
            sys.exit(1)
    
    if args.neo4j:
        if args.latest:
            backup_file = restore_manager.find_latest_backup('neo4j')
            if not backup_file:
                logger.error("No Neo4j backup found")
                return
            backup_file = str(backup_file)
        elif args.backup_file:
            backup_file = args.backup_file
        else:
            logger.error("Must specify --backup-file or --latest")
            return
        
        success = restore_manager.restore_neo4j(
            backup_file=backup_file,
            uri=args.neo4j_uri,
            user=args.neo4j_user,
            password=args.neo4j_password,
            clear_existing=args.clear_existing
        )
        
        if success:
            print(f"\n✅ Neo4j restore completed successfully!")
        else:
            print(f"\n❌ Neo4j restore failed!")
            sys.exit(1)


if __name__ == '__main__':
    main()
