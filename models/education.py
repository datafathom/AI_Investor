"""
==============================================================================
FILE: models/education.py
ROLE: Education & Learning Data Models
PURPOSE: Pydantic models for courses, tutorials, progress tracking, and
         certifications.

INTEGRATION POINTS:
    - LearningManagementService: Course management
    - ContentManagementService: Content delivery
    - EducationAPI: Education endpoints
    - FrontendEducation: Learning dashboard

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class CourseStatus(str, Enum):
    """Course enrollment status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CERTIFIED = "certified"


class Course(BaseModel):
    """Course definition."""
    course_id: str
    title: str
    description: str
    instructor: str
    category: str
    difficulty: str  # beginner, intermediate, advanced
    duration_hours: float
    lessons: List[Dict] = []
    prerequisites: List[str] = []
    created_date: datetime
    updated_date: datetime


class Enrollment(BaseModel):
    """Course enrollment."""
    enrollment_id: str
    user_id: str
    course_id: str
    status: CourseStatus = CourseStatus.NOT_STARTED
    progress_percentage: float = 0.0
    completed_lessons: List[str] = []
    started_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    certificate_id: Optional[str] = None


class Certificate(BaseModel):
    """Course completion certificate."""
    certificate_id: str
    user_id: str
    course_id: str
    issued_date: datetime
    certificate_url: Optional[str] = None
    verification_code: str
