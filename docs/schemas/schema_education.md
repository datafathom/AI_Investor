# Schema: Education

## File Location
`schemas/education.py`

## Purpose
Pydantic models for educational content including courses, tutorials, enrollment tracking, and certifications. Supports the learning management system that helps users improve their financial literacy.

---

## Enums

### CourseStatus
**User enrollment status in a course.**

| Value | Description |
|-------|-------------|
| `NOT_STARTED` | Enrolled but not begun |
| `IN_PROGRESS` | Actively taking course |
| `COMPLETED` | Finished course content |
| `CERTIFIED` | Passed certification exam |

---

## Models

### Course
**Educational course definition.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `course_id` | `str` | *required* | Unique course identifier | Primary key |
| `title` | `str` | *required* | Course title | Display |
| `description` | `str` | *required* | Course summary | Marketing, search |
| `instructor` | `str` | *required* | Who teaches the course | Attribution |
| `category` | `str` | *required* | Topic category | Filtering |
| `difficulty` | `str` | *required* | Level: `beginner`, `intermediate`, `advanced` | Matching to skill level |
| `duration_hours` | `float` | *required* | Estimated completion time | Planning |
| `lessons` | `List[Dict]` | `[]` | Course lesson structures | Content organization |
| `prerequisites` | `List[str]` | `[]` | Required prior courses | Learning path |
| `created_date` | `datetime` | *required* | Course creation | Audit |
| `updated_date` | `datetime` | *required* | Last content update | Freshness |

---

### Enrollment
**User enrollment in a course.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `enrollment_id` | `str` | *required* | Unique enrollment ID | Primary key |
| `user_id` | `str` | *required* | Enrolled user | Attribution |
| `course_id` | `str` | *required* | Enrolled course | Links to course |
| `status` | `CourseStatus` | `NOT_STARTED` | Current progress state | Tracking |
| `progress_percentage` | `float` | `0.0` | Completion percentage | Progress display |
| `completed_lessons` | `List[str]` | `[]` | Lesson IDs completed | Granular tracking |
| `started_date` | `Optional[datetime]` | `None` | When user started | Timeline |
| `completed_date` | `Optional[datetime]` | `None` | When user finished | Completion record |
| `certificate_id` | `Optional[str]` | `None` | Earned certificate | Links to certificate |

---

### Certificate
**Course completion certificate.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `certificate_id` | `str` | *required* | Unique certificate ID | Primary key |
| `user_id` | `str` | *required* | Certificate holder | Attribution |
| `course_id` | `str` | *required* | Completed course | Links to course |
| `issued_date` | `datetime` | *required* | When certificate was issued | Validation |
| `certificate_url` | `Optional[str]` | `None` | Downloadable certificate URL | Distribution |
| `verification_code` | `str` | *required* | Unique verification code | Authenticity check |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `LearningManagementService` | Course management |
| `ContentManagementService` | Lesson content delivery |
| `CertificationService` | Certificate generation |
| `ProgressTrackingService` | Enrollment tracking |

## Frontend Components
- Learning dashboard (FrontendEducation)
- Course catalog
- Progress tracker
- Certificate viewer
