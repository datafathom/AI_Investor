"""
Tests for Expert Q&A Service
Comprehensive test coverage for expert questions, answers, and routing
"""

import pytest
from datetime import timezone, datetime
from unittest.mock import Mock, AsyncMock, patch
from services.community.expert_qa_service import ExpertQAService
from schemas.community import ExpertQuestion, ThreadReply


@pytest.fixture
def service():
    """Create service instance with mocked dependencies."""
    with patch('services.community.expert_qa_service.get_cache_service'):
        return ExpertQAService()


@pytest.mark.asyncio
async def test_create_question(service):
    """Test creating expert question."""
    service._route_question = AsyncMock(return_value="expert_123")
    service._save_question = AsyncMock()
    
    result = await service.create_question(
        user_id="user_123",
        title="How to invest in stocks?",
        content="Question content",
        category="investing"
    )
    
    assert result is not None
    assert isinstance(result, ExpertQuestion)
    assert result.user_id == "user_123"
    assert result.expert_id == "expert_123"
    assert result.status == "open"


@pytest.mark.asyncio
async def test_submit_answer(service):
    """Test submitting expert answer."""
    question = ExpertQuestion(
        question_id="question_123",
        user_id="user_123",
        title="Test Question",
        content="Question content",
        category="investing",
        expert_id="expert_123",
        status="open",
        created_date=datetime.now(timezone.utc),
        updated_date=datetime.now(timezone.utc)
    )
    
    service._get_question = AsyncMock(return_value=question)
    service._save_answer = AsyncMock()
    service._update_question = AsyncMock()
    
    result = await service.submit_answer(
        question_id="question_123",
        expert_id="expert_123",
        content="Expert answer here"
    )
    
    assert result is not None
    assert isinstance(result, ThreadReply) or isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_expert_answers(service):
    """Test getting expert answers for question."""
    service._get_answers_from_db = AsyncMock(return_value=[
        ThreadReply(
            reply_id="answer_1",
            thread_id="question_123",
            user_id="expert_123",
            content="Expert answer",
            created_date=datetime.now(timezone.utc)
        )
    ])
    
    result = await service.get_expert_answers("question_123")
    
    assert result is not None
    assert len(result) == 1
