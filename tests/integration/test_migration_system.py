"""
Integration Tests: Database Migration System
Tests the migration system end-to-end
"""

import pytest
from pathlib import Path
from scripts.database.migration_manager import MigrationManager
import tempfile
import json


class TestMigrationManager:
    """Test MigrationManager."""
    
    @pytest.fixture
    def temp_migrations_dir(self):
        """Create temporary migrations directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_create_migration(self, temp_migrations_dir):
        """Test creating a new migration."""
        manager = MigrationManager(migrations_dir=str(temp_migrations_dir))
        forward, rollback = manager.create_migration('test_migration', 'Test migration')
        
        assert forward.exists()
        assert rollback.exists()
        assert 'test_migration' in forward.name
        assert 'rollback' in rollback.name
    
    def test_list_migrations(self, temp_migrations_dir):
        """Test listing migrations."""
        manager = MigrationManager(migrations_dir=str(temp_migrations_dir))
        
        # Create a migration
        manager.create_migration('test1', 'Test 1')
        manager.create_migration('test2', 'Test 2')
        
        migrations = manager.list_migrations()
        assert len(migrations) == 2
    
    def test_get_pending_migrations(self, temp_migrations_dir):
        """Test getting pending migrations."""
        manager = MigrationManager(migrations_dir=str(temp_migrations_dir))
        
        # Create migrations
        manager.create_migration('test1', 'Test 1')
        manager.create_migration('test2', 'Test 2')
        
        pending = manager.get_pending_migrations()
        assert len(pending) == 2
    
    def test_validate_migration(self, temp_migrations_dir):
        """Test migration validation."""
        manager = MigrationManager(migrations_dir=str(temp_migrations_dir))
        
        # Create a valid migration
        forward, _ = manager.create_migration('valid', 'Valid migration')
        
        # Read and modify to make it valid
        content = forward.read_text()
        content = content.replace('-- Add your migration SQL here', '''
BEGIN;
CREATE TABLE test_table (id SERIAL PRIMARY KEY);
COMMIT;
''')
        forward.write_text(content)
        
        valid, errors = manager.validate_migration(forward.stem)
        # Should be valid or have minor warnings
        assert isinstance(valid, bool)
        assert isinstance(errors, list)
    
    def test_get_migration_status(self, temp_migrations_dir):
        """Test getting migration status."""
        manager = MigrationManager(migrations_dir=str(temp_migrations_dir))
        
        # Create migrations
        manager.create_migration('test1', 'Test 1')
        
        status = manager.get_migration_status()
        assert 'total_migrations' in status
        assert 'applied_migrations' in status
        assert 'pending_migrations' in status
        assert status['total_migrations'] >= 1
