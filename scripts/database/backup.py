#!/usr/bin/env python3
"""
Database Backup Script
Complete automated backup system for PostgreSQL and Neo4j
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import timezone, datetime
from typing import Optional, Dict, List
import json
import gzip
import shutil

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BACKUP_DIR = Path(os.getenv('BACKUP_DIR', 'backups'))
BACKUP_RETENTION_DAYS = int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
S3_BUCKET = os.getenv('S3_BACKUP_BUCKET')
S3_PREFIX = os.getenv('S3_BACKUP_PREFIX', 'database-backups')


class DatabaseBackup:
    """Complete database backup manager."""
    
    def __init__(self):
        self.backup_dir = BACKUP_DIR
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.s3_enabled = bool(S3_BUCKET)
    
    def backup_postgres(self, db_name: str, host: str = "localhost", 
                       port: int = 5432, user: str = "postgres",
                       password: Optional[str] = None) -> Optional[str]:
        """
        Backup PostgreSQL database.
        
        Returns:
            Path to backup file or None if failed
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"postgres_{db_name}_{timestamp}.sql"
        compressed_file = self.backup_dir / f"postgres_{db_name}_{timestamp}.sql.gz"
        
        logger.info(f"Starting PostgreSQL backup: {db_name}")
        
        try:
            # Set PGPASSWORD environment variable
            env = os.environ.copy()
            if password:
                env['PGPASSWORD'] = password
            
            # Run pg_dump
            cmd = [
                'pg_dump',
                '-h', host,
                '-p', str(port),
                '-U', user,
                '-d', db_name,
                '-F', 'c',  # Custom format
                '-f', str(backup_file)
            ]
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Compress backup
            logger.info(f"Compressing backup: {backup_file}")
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed file
            backup_file.unlink()
            
            # Upload to S3 if enabled
            if self.s3_enabled:
                self._upload_to_s3(compressed_file, f"{S3_PREFIX}/postgres/")
            
            logger.info(f"✅ PostgreSQL backup completed: {compressed_file}")
            return str(compressed_file)
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ PostgreSQL backup failed: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"❌ PostgreSQL backup error: {e}")
            return None
    
    def backup_neo4j(self, uri: str = "bolt://localhost:7687",
                     user: str = "neo4j", password: Optional[str] = None) -> Optional[str]:
        """
        Backup Neo4j database.
        
        Returns:
            Path to backup file or None if failed
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"neo4j_{timestamp}.dump"
        compressed_file = self.backup_dir / f"neo4j_{timestamp}.dump.gz"
        
        logger.info("Starting Neo4j backup")
        
        try:
            # Neo4j backup using neo4j-admin (requires Neo4j Enterprise)
            # For Community Edition, use APOC procedures or manual export
            
            # Check if neo4j-admin is available
            neo4j_admin = os.getenv('NEO4J_ADMIN_PATH', 'neo4j-admin')
            
            cmd = [
                neo4j_admin,
                'dump',
                '--database=neo4j',
                f'--to={backup_file}'
            ]
            
            env = os.environ.copy()
            if user:
                env['NEO4J_AUTH'] = f"{user}/{password}"
            
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Compress backup
            logger.info(f"Compressing backup: {backup_file}")
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove uncompressed file
            backup_file.unlink()
            
            # Upload to S3 if enabled
            if self.s3_enabled:
                self._upload_to_s3(compressed_file, f"{S3_PREFIX}/neo4j/")
            
            logger.info(f"✅ Neo4j backup completed: {compressed_file}")
            return str(compressed_file)
            
        except FileNotFoundError:
            logger.warning("neo4j-admin not found. Using alternative backup method...")
            # Fallback: Use Cypher export
            return self._backup_neo4j_cypher(uri, user, password)
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Neo4j backup failed: {e.stderr}")
            return None
        except Exception as e:
            logger.error(f"❌ Neo4j backup error: {e}")
            return None
    
    def _backup_neo4j_cypher(self, uri: str, user: str, password: Optional[str]) -> Optional[str]:
        """Backup Neo4j using Cypher export (for Community Edition)."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"neo4j_cypher_{timestamp}.cypher"
        compressed_file = self.backup_dir / f"neo4j_cypher_{timestamp}.cypher.gz"
        
        try:
            from neo4j import GraphDatabase
            
            driver = GraphDatabase.driver(uri, auth=(user, password))
            
            # Export all nodes and relationships
            with driver.session() as session:
                # Get all nodes
                nodes_query = "MATCH (n) RETURN n"
                nodes = session.run(nodes_query)
                
                # Get all relationships
                rels_query = "MATCH (a)-[r]->(b) RETURN a, r, b"
                relationships = session.run(rels_query)
                
                # Write to file
                with open(backup_file, 'w') as f:
                    # Export nodes
                    for record in nodes:
                        node = record['n']
                        f.write(f"CREATE {node}\n")
                    
                    # Export relationships
                    for record in relationships:
                        a = record['a']
                        r = record['r']
                        b = record['b']
                        f.write(f"CREATE ({a})-[:{r.type}]->({b})\n")
            
            driver.close()
            
            # Compress
            with open(backup_file, 'rb') as f_in:
                with gzip.open(compressed_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            backup_file.unlink()
            
            if self.s3_enabled:
                self._upload_to_s3(compressed_file, f"{S3_PREFIX}/neo4j/")
            
            logger.info(f"✅ Neo4j Cypher backup completed: {compressed_file}")
            return str(compressed_file)
            
        except ImportError:
            logger.error("neo4j driver not installed")
            return None
        except Exception as e:
            logger.error(f"Neo4j Cypher backup failed: {e}")
            return None
    
    def _upload_to_s3(self, file_path: Path, s3_prefix: str):
        """Upload backup file to S3."""
        if not self.s3_enabled:
            return
        
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            s3_client = boto3.client('s3')
            s3_key = f"{s3_prefix}{file_path.name}"
            
            logger.info(f"Uploading to S3: s3://{S3_BUCKET}/{s3_key}")
            
            s3_client.upload_file(
                str(file_path),
                S3_BUCKET,
                s3_key,
                ExtraArgs={'ServerSideEncryption': 'AES256'}
            )
            
            logger.info(f"✅ Uploaded to S3: {s3_key}")
            
        except ImportError:
            logger.warning("boto3 not installed, skipping S3 upload")
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
    
    def list_backups(self, db_type: Optional[str] = None) -> List[Dict]:
        """List all backup files."""
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob("*.gz")):
            if db_type and db_type not in backup_file.name:
                continue
            
            stat = backup_file.stat()
            backups.append({
                'file': backup_file.name,
                'path': str(backup_file),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': 'postgres' if 'postgres' in backup_file.name else 'neo4j'
            })
        
        return backups
    
    def cleanup_old_backups(self, retention_days: int = BACKUP_RETENTION_DAYS):
        """Remove backups older than retention period."""
        cutoff_date = datetime.now(timezone.utc).timestamp() - (retention_days * 24 * 60 * 60)
        
        removed_count = 0
        for backup_file in self.backup_dir.glob("*.gz"):
            if backup_file.stat().st_mtime < cutoff_date:
                backup_file.unlink()
                removed_count += 1
                logger.info(f"Removed old backup: {backup_file.name}")
        
        logger.info(f"Cleaned up {removed_count} old backups")
        return removed_count
    
    def verify_backup(self, backup_file: str) -> bool:
        """Verify backup file integrity."""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_file}")
            return False
        
        # Check if file is compressed
        if backup_path.suffix == '.gz':
            try:
                with gzip.open(backup_path, 'rb') as f:
                    # Try to read first few bytes
                    f.read(1024)
                logger.info(f"✅ Backup file verified: {backup_file}")
                return True
            except Exception as e:
                logger.error(f"Backup file corrupted: {e}")
                return False
        
        return True


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Backup Tool')
    parser.add_argument('action', choices=['backup', 'list', 'cleanup', 'verify'],
                       help='Action to perform')
    parser.add_argument('--db-type', choices=['postgres', 'neo4j', 'all'],
                       default='all', help='Database type to backup')
    parser.add_argument('--db-name', help='PostgreSQL database name')
    parser.add_argument('--postgres-host', default='localhost', help='PostgreSQL host')
    parser.add_argument('--postgres-port', type=int, default=5432, help='PostgreSQL port')
    parser.add_argument('--postgres-user', default='postgres', help='PostgreSQL user')
    parser.add_argument('--postgres-password', help='PostgreSQL password')
    parser.add_argument('--neo4j-uri', default='bolt://localhost:7687', help='Neo4j URI')
    parser.add_argument('--neo4j-user', default='neo4j', help='Neo4j user')
    parser.add_argument('--neo4j-password', help='Neo4j password')
    parser.add_argument('--retention-days', type=int, default=BACKUP_RETENTION_DAYS,
                       help='Backup retention days')
    parser.add_argument('--backup-file', help='Backup file to verify')
    
    args = parser.parse_args()
    
    backup_manager = DatabaseBackup()
    
    if args.action == 'backup':
        if args.db_type in ['postgres', 'all']:
            if not args.db_name:
                logger.error("--db-name required for PostgreSQL backup")
                sys.exit(1)
            backup_manager.backup_postgres(
                db_name=args.db_name,
                host=args.postgres_host,
                port=args.postgres_port,
                user=args.postgres_user,
                password=args.postgres_password
            )
        
        if args.db_type in ['neo4j', 'all']:
            backup_manager.backup_neo4j(
                uri=args.neo4j_uri,
                user=args.neo4j_user,
                password=args.neo4j_password
            )
    
    elif args.action == 'list':
        backups = backup_manager.list_backups(args.db_type if args.db_type != 'all' else None)
        print(f"\nFound {len(backups)} backup(s):")
        for backup in backups:
            print(f"  {backup['file']} - {backup['size']} bytes - {backup['created']}")
    
    elif args.action == 'cleanup':
        removed = backup_manager.cleanup_old_backups(args.retention_days)
        print(f"Removed {removed} old backup(s)")
    
    elif args.action == 'verify':
        if not args.backup_file:
            logger.error("--backup-file required for verify")
            sys.exit(1)
        success = backup_manager.verify_backup(args.backup_file)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
