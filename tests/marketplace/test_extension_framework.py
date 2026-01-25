"""
Tests for Extension Framework
Comprehensive test coverage for extension creation and sandboxed execution
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.marketplace.extension_framework import ExtensionFramework
from models.marketplace import Extension, ExtensionStatus


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.marketplace.extension_framework.get_cache_service'):
        return ExtensionFramework()


@pytest.mark.asyncio
async def test_create_extension(service):
    """Test extension creation."""
    service._save_extension = AsyncMock()
    
    result = await service.create_extension(
        developer_id="dev_123",
        extension_name="Portfolio Analyzer",
        description="Analyzes portfolio performance",
        version="1.0.0",
        category="analytics"
    )
    
    assert result is not None
    assert isinstance(result, Extension)
    assert result.developer_id == "dev_123"
    assert result.extension_name == "Portfolio Analyzer"
    assert result.status == ExtensionStatus.DRAFT


@pytest.mark.asyncio
async def test_validate_extension(service):
    """Test extension validation."""
    extension = Extension(
        extension_id="ext_123",
        developer_id="dev_123",
        extension_name="Test Extension",
        description="Description",
        version="1.0.0",
        category="analytics",
        status=ExtensionStatus.DRAFT,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._validate_security = AsyncMock(return_value={'valid': True, 'errors': []})
    service._validate_code = AsyncMock(return_value={'valid': True, 'errors': []})
    
    result = await service.validate_extension(extension)
    
    assert result is not None
    assert result['valid'] is True
