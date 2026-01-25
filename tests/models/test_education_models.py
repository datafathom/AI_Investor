"""
Tests for Education Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from models.education import (
    CourseStatus,
    Course,
    Enrollment,
    Certificate
)


class TestCourseStatusEnum:
    """Tests for CourseStatus enum."""
    
    def test_course_status_enum(self):
        """Test course status enum values."""
        assert CourseStatus.NOT_STARTED == "not_started"
        assert CourseStatus.IN_PROGRESS == "in_progress"
        assert CourseStatus.COMPLETED == "completed"
        assert CourseStatus.CERTIFIED == "certified"


class TestCourse:
    """Tests for Course model."""
    
    def test_valid_course(self):
        """Test valid course creation."""
        course = Course(
            course_id='course_1',
            title='Introduction to Investing',
            description='Learn the basics of investing',
            instructor='John Doe',
            category='investing',
            difficulty='beginner',
            duration_hours=10.0,
            lessons=[],
            prerequisites=[],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert course.course_id == 'course_1'
        assert course.difficulty == 'beginner'
        assert course.duration_hours == 10.0
    
    def test_course_with_prerequisites(self):
        """Test course with prerequisites."""
        course = Course(
            course_id='course_2',
            title='Advanced Trading',
            description='Advanced trading strategies',
            instructor='Jane Smith',
            category='trading',
            difficulty='advanced',
            duration_hours=20.0,
            prerequisites=['course_1'],
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert len(course.prerequisites) == 1


class TestEnrollment:
    """Tests for Enrollment model."""
    
    def test_valid_enrollment(self):
        """Test valid enrollment creation."""
        enrollment = Enrollment(
            enrollment_id='enroll_1',
            user_id='user_1',
            course_id='course_1',
            status=CourseStatus.IN_PROGRESS,
            progress_percentage=50.0,
            completed_lessons=['lesson_1', 'lesson_2'],
            started_date=datetime.now(),
            completed_date=None,
            certificate_id=None
        )
        assert enrollment.enrollment_id == 'enroll_1'
        assert enrollment.status == CourseStatus.IN_PROGRESS
        assert enrollment.progress_percentage == 50.0
    
    def test_enrollment_defaults(self):
        """Test enrollment with default values."""
        enrollment = Enrollment(
            enrollment_id='enroll_1',
            user_id='user_1',
            course_id='course_1'
        )
        assert enrollment.status == CourseStatus.NOT_STARTED
        assert enrollment.progress_percentage == 0.0
        assert len(enrollment.completed_lessons) == 0


class TestCertificate:
    """Tests for Certificate model."""
    
    def test_valid_certificate(self):
        """Test valid certificate creation."""
        certificate = Certificate(
            certificate_id='cert_1',
            user_id='user_1',
            course_id='course_1',
            issued_date=datetime.now(),
            certificate_url='https://example.com/cert.pdf',
            verification_code='ABC123'
        )
        assert certificate.certificate_id == 'cert_1'
        assert certificate.verification_code == 'ABC123'
        assert certificate.certificate_url is not None
