# Backend Service: Education

## Overview
The **Education Service** is the platform's knowledge transfer and financial literacy layer. It provides a comprehensive suite of tools ranging from institutional-grade **Learning Management Systems (LMS)** to automated **529 Education Savings** planning. It is specifically designed to support multi-generational wealth stewardship through specialized training for heirs and family office participants.

## Core Components

### 1. Learning Management System (LMS) (`learning_management_service.py`)
The foundational engine for educational content delivery.
- **Course Lifecycle**: Manages the creation, enrollment, and completion status of educational modules.
- **Progress Tracking**: Monitors lesson-level activity and calculates completion percentages in real-time.
- **Automated Certification**: Issues verifiable completion certificates once a curriculum assessment threshold is met.

### 2. Heir Training Portal (`heir_lms.py`)
Specialized curriculum tracking for multi-generational wealth.
- **Governance Training**: Tracks mandatory participation in modules like "Family Board Governance" and "Strategic Philanthropy."
- **Performance Thresholds**: Enforces a "Certified" status only for heirs who pass assessments with high scores, ensuring competence before significant wealth transitions.

### 3. Education Savings Automation (`glide_path_529.py`)
Financial planning logic for future tuition costs.
- **Dynamic Glide Paths**: Automatically shifts portfolio allocations from aggressive (90% Equity) to conservative (50% Cash) based on the "Years to Enrollment" metric.
- **529 Optimization**: Recommends risk-adjusted buckets specifically for the 529 education savings vehicle.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used |
| :--- | :--- | :--- |
| **Education Hub** | My Courses Dashboard | `learning_management_service.enroll_user()` |
| **Education Hub** | Lesson Viewer | `learning_management_service.update_progress()` |
| **Family Office Station** | Heir Training Tracker | `heir_lms.record_progress()` |
| **Education Planner** | 529 Glide Path Chart | `glide_path_recommender_529.recommend_allocation()` |
| **Profile / Awards** | Certificate Wallet | `learning_management_service.issue_certificate()` |

## Dependencies
- `pydantic`: For strictly-typed education models (`Course`, `Enrollment`, `Certificate`).
- `services.system.cache_service`: Provides high-speed persistence for progress tracking and certificate storage.

## Usage Examples

### Tracking Heir Training Progress
```python
from services.education.heir_lms import HeirLMSService
from uuid import uuid4

heir_svc = HeirLMSService()

# Record a score for a mandatory governance module
result = heir_svc.record_progress(
    heir_id=uuid4(),
    course_id="GOV-201",
    score=88
)

print(f"Certification Status: {result['certified']}")
print(f"LMS Message: {result['status']}")
```

### Retrieving 529 Allocation Recommendations
```python
from services.education.glide_path_529 import GlidePathRecommender529

recommender = GlidePathRecommender529()

# child is 10 years away from college
allocation = recommender.recommend_allocation(years_to_enrollment=10)

print("Target 529 Allocation:")
for asset_class, weight in allocation.items():
    print(f"- {asset_class}: {weight*100}%")
```
