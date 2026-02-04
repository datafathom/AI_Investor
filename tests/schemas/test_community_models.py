"""
Tests for Community Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.community import (
    ThreadCategory,
    ForumThread,
    ThreadReply,
    ExpertQuestion
)


class TestThreadCategoryEnum:
    """Tests for ThreadCategory enum."""
    
    def test_thread_category_enum(self):
        """Test thread category enum values."""
        assert ThreadCategory.GENERAL == "general"
        assert ThreadCategory.TRADING == "trading"
        assert ThreadCategory.TAX == "tax"
        assert ThreadCategory.RETIREMENT == "retirement"


class TestForumThread:
    """Tests for ForumThread model."""
    
    def test_valid_forum_thread(self):
        """Test valid forum thread creation."""
        thread = ForumThread(
            thread_id='thread_1',
            user_id='user_1',
            category=ThreadCategory.TRADING,
            title='Test Thread',
            content='Test content',
            upvotes=10,
            downvotes=2,
            reply_count=5,
            views=100,
            is_pinned=False,
            is_locked=False,
            created_date=datetime.now(),
            updated_date=datetime.now(),
            last_reply_date=datetime.now()
        )
        assert thread.thread_id == 'thread_1'
        assert thread.category == ThreadCategory.TRADING
        assert thread.upvotes == 10
    
    def test_forum_thread_defaults(self):
        """Test forum thread with default values."""
        thread = ForumThread(
            thread_id='thread_1',
            user_id='user_1',
            category=ThreadCategory.GENERAL,
            title='Test Thread',
            content='Test content',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert thread.upvotes == 0
        assert thread.downvotes == 0
        assert thread.is_pinned is False


class TestThreadReply:
    """Tests for ThreadReply model."""
    
    def test_valid_thread_reply(self):
        """Test valid thread reply creation."""
        reply = ThreadReply(
            reply_id='reply_1',
            thread_id='thread_1',
            user_id='user_1',
            content='Test reply',
            parent_reply_id=None,
            upvotes=5,
            downvotes=0,
            is_best_answer=False,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert reply.reply_id == 'reply_1'
        assert reply.thread_id == 'thread_1'
        assert reply.is_best_answer is False
    
    def test_thread_reply_nested(self):
        """Test nested thread reply."""
        reply = ThreadReply(
            reply_id='reply_2',
            thread_id='thread_1',
            user_id='user_2',
            content='Nested reply',
            parent_reply_id='reply_1',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert reply.parent_reply_id == 'reply_1'


class TestExpertQuestion:
    """Tests for ExpertQuestion model."""
    
    def test_valid_expert_question(self):
        """Test valid expert question creation."""
        question = ExpertQuestion(
            question_id='question_1',
            user_id='user_1',
            title='Test Question',
            content='Test question content',
            category='tax',
            expert_id='expert_1',
            best_answer_id='answer_1',
            answer_count=3,
            status='answered',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert question.question_id == 'question_1'
        assert question.status == 'answered'
        assert question.answer_count == 3
    
    def test_expert_question_defaults(self):
        """Test expert question with default values."""
        question = ExpertQuestion(
            question_id='question_1',
            user_id='user_1',
            title='Test Question',
            content='Test content',
            category='general',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert question.status == 'open'
        assert question.answer_count == 0
        assert question.expert_id is None
