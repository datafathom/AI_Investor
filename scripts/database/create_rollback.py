#!/usr/bin/env python3
"""
Rollback Migration Generator
Helps create rollback migrations for forward migrations
"""

import sys
from pathlib import Path
import re

MIGRATIONS_DIR = Path(__file__).parent.parent.parent / "migrations"


def extract_sql_statements(migration_file: Path) -> list:
    """Extract SQL statements from migration file."""
    with open(migration_file, 'r') as f:
        content = f.read()
    
    # Split by semicolons (simple approach)
    statements = [s.strip() for s in content.split(';') if s.strip()]
    return statements


def generate_rollback(migration_file: Path) -> str:
    """Generate rollback SQL for a migration file."""
    statements = extract_sql_statements(migration_file)
    rollback_statements = []
    
    for stmt in statements:
        stmt_upper = stmt.upper()
        
        # CREATE TABLE -> DROP TABLE
        if 'CREATE TABLE' in stmt_upper:
            table_match = re.search(r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?(\w+)', stmt_upper)
            if table_match:
                table_name = table_match.group(1)
                rollback_statements.append(f"DROP TABLE IF EXISTS {table_name};")
        
        # ALTER TABLE ADD COLUMN -> ALTER TABLE DROP COLUMN
        elif 'ALTER TABLE' in stmt_upper and 'ADD COLUMN' in stmt_upper:
            table_match = re.search(r'ALTER TABLE\s+(\w+)', stmt_upper)
            col_match = re.search(r'ADD COLUMN\s+(\w+)', stmt_upper)
            if table_match and col_match:
                table_name = table_match.group(1)
                col_name = col_match.group(1)
                rollback_statements.append(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {col_name};")
        
        # CREATE INDEX -> DROP INDEX
        elif 'CREATE INDEX' in stmt_upper or 'CREATE UNIQUE INDEX' in stmt_upper:
            index_match = re.search(r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF NOT EXISTS\s+)?(\w+)', stmt_upper)
            if index_match:
                index_name = index_match.group(1)
                rollback_statements.append(f"DROP INDEX IF EXISTS {index_name};")
        
        # CREATE FUNCTION -> DROP FUNCTION
        elif 'CREATE FUNCTION' in stmt_upper or 'CREATE OR REPLACE FUNCTION' in stmt_upper:
            func_match = re.search(r'CREATE\s+(?:OR\s+REPLACE\s+)?FUNCTION\s+(\w+)', stmt_upper)
            if func_match:
                func_name = func_match.group(1)
                rollback_statements.append(f"DROP FUNCTION IF EXISTS {func_name} CASCADE;")
        
        # CREATE TRIGGER -> DROP TRIGGER
        elif 'CREATE TRIGGER' in stmt_upper:
            trigger_match = re.search(r'CREATE TRIGGER\s+(\w+)', stmt_upper)
            if trigger_match:
                trigger_name = trigger_match.group(1)
                table_match = re.search(r'ON\s+(\w+)', stmt_upper)
                if table_match:
                    table_name = table_match.group(1)
                    rollback_statements.append(f"DROP TRIGGER IF EXISTS {trigger_name} ON {table_name};")
    
    if not rollback_statements:
        return f"-- Rollback for {migration_file.name}\n-- Manual rollback required - review migration file\n"
    
    rollback_sql = f"-- Rollback migration for {migration_file.name}\n"
    rollback_sql += f"-- Generated automatically - review before using\n\n"
    rollback_sql += "\n".join(rollback_statements)
    rollback_sql += "\n"
    
    return rollback_sql


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate rollback migration')
    parser.add_argument('migration_file', help='Path to migration file')
    parser.add_argument('--output', help='Output file path (default: migration_file_rollback.sql)')
    
    args = parser.parse_args()
    
    migration_file = Path(args.migration_file)
    if not migration_file.exists():
        print(f"❌ Migration file not found: {migration_file}")
        sys.exit(1)
    
    rollback_sql = generate_rollback(migration_file)
    
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = migration_file.parent / f"{migration_file.stem}_rollback.sql"
    
    with open(output_file, 'w') as f:
        f.write(rollback_sql)
    
    print(f"✅ Rollback migration created: {output_file}")
    print(f"\n⚠️  Please review the generated rollback before using it!")


if __name__ == '__main__':
    main()
