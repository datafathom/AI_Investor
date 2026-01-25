"""
Tests for Content Management Service
Comprehensive test coverage for educational content management
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.education.content_management_service import ContentManagementService


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.education.content_management_service.get_cache_service'):
        return ContentManagementService()


@pytest.mark.asyncio
async def test_create_content_video(service):
    """Test creating video content."""
    result = await service.create_content(
        content_type="video",
        title="Investment Basics Video",
        content_data={'url': 'https://example.com/video.mp4', 'duration': 300}
    )
    
    assert result is not None
    assert result['content_type'] == "video"
    assert result['title'] == "Investment Basics Video"


@pytest.mark.asyncio
async def test_create_content_article(service):
    """Test creating article content."""
    result = await service.create_content(
        content_type="article",
        title="Stock Market Guide",
        content_data={'body': 'Article content here...', 'author': 'John Doe'}
    )
    
    assert result is not None
    assert result['content_type'] == "article"


@pytest.mark.asyncio
async def test_get_content(service):
    """Test retrieving content."""
    content = {
        'content_id': 'content_123',
        'content_type': 'video',
        'title': 'Test Video',
        'data': {},
        'created_date': datetime.utcnow().isoformat()
    }
    
    service.cache_service.get = AsyncMock(return_value=content)
    
    result = await service.get_content("content_123")
    
    assert result is not None
    assert result['content_id'] == "content_123"
