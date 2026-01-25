"""
==============================================================================
FILE: models/community.py
ROLE: Community Forum Data Models
PURPOSE: Pydantic models for forums, threads, replies, and Q&A systems.

INTEGRATION POINTS:
    - ForumService: Thread management
    - ExpertQAService: Q&A system
    - CommunityAPI: Community endpoints
    - FrontendCommunity: Forum widgets

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class ThreadCategory(str, Enum):
    """Forum thread categories."""
    GENERAL = "general"
    TRADING = "trading"
    TAX = "tax"
    RETIREMENT = "retirement"
    CRYPTO = "crypto"
    OPTIONS = "options"
    EDUCATION = "education"


class ForumThread(BaseModel):
    """Forum thread definition."""
    thread_id: str
    user_id: str
    category: ThreadCategory
    title: str
    content: str
    upvotes: int = 0
    downvotes: int = 0
    reply_count: int = 0
    views: int = 0
    is_pinned: bool = False
    is_locked: bool = False
    created_date: datetime
    updated_date: datetime
    last_reply_date: Optional[datetime] = None


class ThreadReply(BaseModel):
    """Thread reply definition."""
    reply_id: str
    thread_id: str
    user_id: str
    content: str
    parent_reply_id: Optional[str] = None  # For nested replies
    upvotes: int = 0
    downvotes: int = 0
    is_best_answer: bool = False
    created_date: datetime
    updated_date: datetime


class ExpertQuestion(BaseModel):
    """Expert Q&A question."""
    question_id: str
    user_id: str
    title: str
    content: str
    category: str
    expert_id: Optional[str] = None  # Assigned expert
    best_answer_id: Optional[str] = None
    answer_count: int = 0
    status: str = "open"  # open, answered, closed
    created_date: datetime
    updated_date: datetime
