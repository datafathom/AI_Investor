"""
Tests for Forum Service
Comprehensive test coverage for forum threads, replies, and moderation
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from services.community.forum_service import ForumService
from models.community import ForumThread, ThreadReply, ThreadCategory


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.community.forum_service.get_cache_service'):
        return ForumService()


@pytest.mark.asyncio
async def test_create_thread(service):
    """Test forum thread creation."""
    service._save_thread = AsyncMock()
    
    result = await service.create_thread(
        user_id="user_123",
        category="general",
        title="Test Thread",
        content="Thread content here"
    )
    
    assert result is not None
    assert isinstance(result, ForumThread)
    assert result.user_id == "user_123"
    assert result.title == "Test Thread"
    assert result.category == ThreadCategory.GENERAL


@pytest.mark.asyncio
async def test_add_reply(service):
    """Test adding reply to thread."""
    thread = ForumThread(
        thread_id="thread_123",
        user_id="user_123",
        category=ThreadCategory.GENERAL,
        title="Test Thread",
        content="Content",
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_thread = AsyncMock(return_value=thread)
    service._save_reply = AsyncMock()
    service._update_thread = AsyncMock()
    
    result = await service.add_reply(
        thread_id="thread_123",
        user_id="user_456",
        content="Reply content"
    )
    
    assert result is not None
    assert isinstance(result, ThreadReply)
    assert result.thread_id == "thread_123"
    assert result.user_id == "user_456"


@pytest.mark.asyncio
async def test_upvote_thread(service):
    """Test upvoting a thread."""
    thread = ForumThread(
        thread_id="thread_123",
        user_id="user_123",
        category=ThreadCategory.GENERAL,
        title="Test Thread",
        content="Content",
        upvotes=5,
        created_date=datetime.utcnow(),
        updated_date=datetime.utcnow()
    )
    
    service._get_thread = AsyncMock(return_value=thread)
    service._save_thread = AsyncMock()
    
    result = await service.upvote_thread("thread_123", "user_456")
    
    assert result is not None
    assert result.upvotes == 6


@pytest.mark.asyncio
async def test_get_threads_by_category(service):
    """Test getting threads by category."""
    service._get_threads_from_db = AsyncMock(return_value=[
        ForumThread(
            thread_id="thread_1",
            user_id="user_123",
            category=ThreadCategory.GENERAL,
            title="Thread 1",
            content="Content",
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
    ])
    
    result = await service.get_threads_by_category("general", limit=10)
    
    assert result is not None
    assert len(result) == 1
