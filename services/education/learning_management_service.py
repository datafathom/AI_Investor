"""
==============================================================================
FILE: services/education/learning_management_service.py
ROLE: Learning Management System
PURPOSE: Manages courses, progress tracking, assessments, and certifications.

INTEGRATION POINTS:
    - ContentManagementService: Course content delivery
    - UserService: User progress tracking
    - EducationAPI: Education endpoints
    - FrontendEducation: Learning dashboard

FEATURES:
    - Course creation and management
    - Progress tracking
    - Assessments and quizzes
    - Certification generation

AUTHOR: AI Investor Team
CREATED: 2026-01-21
LAST_MODIFIED: 2026-01-21
==============================================================================
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.education import Course, Enrollment, CourseStatus, Certificate
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)


class LearningManagementService:
    """
    Service for learning management.
    """
    
    def __init__(self):
        """Initialize service with dependencies."""
        self.cache_service = get_cache_service()
        
    async def create_course(
        self,
        title: str,
        description: str,
        instructor: str,
        category: str,
        difficulty: str,
        duration_hours: float,
        lessons: Optional[List[Dict]] = None
    ) -> Course:
        """
        Create a new course.
        
        Args:
            title: Course title
            description: Course description
            instructor: Instructor name
            category: Course category
            difficulty: Difficulty level
            duration_hours: Course duration in hours
            lessons: Optional list of lessons
            
        Returns:
            Course object
        """
        logger.info(f"Creating course: {title}")
        
        course = Course(
            course_id=f"course_{datetime.utcnow().timestamp()}",
            title=title,
            description=description,
            instructor=instructor,
            category=category,
            difficulty=difficulty,
            duration_hours=duration_hours,
            lessons=lessons or [],
            created_date=datetime.utcnow(),
            updated_date=datetime.utcnow()
        )
        
        # Save course
        await self._save_course(course)
        
        return course
    
    async def enroll_user(
        self,
        user_id: str,
        course_id: str
    ) -> Enrollment:
        """
        Enroll user in course.
        
        Args:
            user_id: User identifier
            course_id: Course identifier
            
        Returns:
            Enrollment object
        """
        logger.info(f"Enrolling user {user_id} in course {course_id}")
        
        enrollment = Enrollment(
            enrollment_id=f"enrollment_{user_id}_{course_id}_{datetime.utcnow().timestamp()}",
            user_id=user_id,
            course_id=course_id,
            status=CourseStatus.NOT_STARTED,
            started_date=datetime.utcnow()
        )
        
        # Save enrollment
        await self._save_enrollment(enrollment)
        
        return enrollment
    
    async def update_progress(
        self,
        enrollment_id: str,
        lesson_id: str
    ) -> Enrollment:
        """
        Update course progress.
        
        Args:
            enrollment_id: Enrollment identifier
            lesson_id: Completed lesson identifier
            
        Returns:
            Updated Enrollment
        """
        enrollment = await self._get_enrollment(enrollment_id)
        if not enrollment:
            raise ValueError(f"Enrollment {enrollment_id} not found")
        
        # Add lesson to completed
        if lesson_id not in enrollment.completed_lessons:
            enrollment.completed_lessons.append(lesson_id)
        
        # Get course to calculate progress
        course = await self._get_course(enrollment.course_id)
        if course:
            total_lessons = len(course.lessons)
            completed = len(enrollment.completed_lessons)
            enrollment.progress_percentage = (completed / total_lessons * 100) if total_lessons > 0 else 0.0
        
        # Update status
        if enrollment.progress_percentage >= 100:
            enrollment.status = CourseStatus.COMPLETED
            enrollment.completed_date = datetime.utcnow()
        elif enrollment.progress_percentage > 0:
            enrollment.status = CourseStatus.IN_PROGRESS
        
        enrollment.updated_date = datetime.utcnow()
        await self._save_enrollment(enrollment)
        
        return enrollment
    
    async def issue_certificate(
        self,
        enrollment_id: str
    ) -> Certificate:
        """
        Issue completion certificate.
        
        Args:
            enrollment_id: Enrollment identifier
            
        Returns:
            Certificate object
        """
        enrollment = await self._get_enrollment(enrollment_id)
        if not enrollment:
            raise ValueError(f"Enrollment {enrollment_id} not found")
        
        if enrollment.status != CourseStatus.COMPLETED:
            raise ValueError("Course must be completed before issuing certificate")
        
        certificate = Certificate(
            certificate_id=f"cert_{enrollment.user_id}_{enrollment.course_id}_{datetime.utcnow().timestamp()}",
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            issued_date=datetime.utcnow(),
            verification_code=f"VERIFY_{enrollment.user_id}_{enrollment.course_id}"
        )
        
        # Update enrollment
        enrollment.certificate_id = certificate.certificate_id
        enrollment.status = CourseStatus.CERTIFIED
        await self._save_enrollment(enrollment)
        
        # Save certificate
        await self._save_certificate(certificate)
        
        return certificate
    
    async def _get_course(self, course_id: str) -> Optional[Course]:
        """Get course from cache."""
        cache_key = f"course:{course_id}"
        course_data = self.cache_service.get(cache_key)
        if course_data:
            return Course(**course_data)
        return None
    
    async def _save_course(self, course: Course):
        """Save course to cache."""
        cache_key = f"course:{course.course_id}"
        self.cache_service.set(cache_key, course.dict(), ttl=86400 * 365)
    
    async def _get_enrollment(self, enrollment_id: str) -> Optional[Enrollment]:
        """Get enrollment from cache."""
        cache_key = f"enrollment:{enrollment_id}"
        enrollment_data = self.cache_service.get(cache_key)
        if enrollment_data:
            return Enrollment(**enrollment_data)
        return None
    
    async def _save_enrollment(self, enrollment: Enrollment):
        """Save enrollment to cache."""
        cache_key = f"enrollment:{enrollment.enrollment_id}"
        self.cache_service.set(cache_key, enrollment.dict(), ttl=86400 * 365)
    
    async def _save_certificate(self, certificate: Certificate):
        """Save certificate to cache."""
        cache_key = f"certificate:{certificate.certificate_id}"
        self.cache_service.set(cache_key, certificate.dict(), ttl=86400 * 365)


# Singleton instance
_learning_management_service: Optional[LearningManagementService] = None


def get_learning_management_service() -> LearningManagementService:
    """Get singleton learning management service instance."""
    global _learning_management_service
    if _learning_management_service is None:
        _learning_management_service = LearningManagementService()
    return _learning_management_service
