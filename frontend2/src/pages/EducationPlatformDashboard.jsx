/**
 * ==============================================================================
 * FILE: frontend2/src/pages/EducationPlatformDashboard.jsx
 * ROLE: Education Platform Dashboard
 * PURPOSE: Phase 21 - Investment Education & Learning Platform
 * 
 * INTEGRATION POINTS:
 *    - EducationStore: Uses apiClient for all API calls (User Rule 6)
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-30
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import useEducationStore from '../stores/educationStore';
import './EducationPlatformDashboard.css';

const EducationPlatformDashboard = () => {
  const userId = 'user_1'; // TODO: Get from authStore
  
  const {
    courses,
    userProgress,
    certifications,
    loading,
    fetchCourses,
    fetchUserProgress,
    fetchCertifications,
    enrollInCourse
  } = useEducationStore();

  const [selectedCourse, setSelectedCourse] = useState(null);

  useEffect(() => {
    fetchCourses();
    fetchUserProgress(userId);
    fetchCertifications(userId);
  }, [fetchCourses, fetchUserProgress, fetchCertifications]);

  const handleEnroll = async (courseId) => {
    await enrollInCourse(userId, courseId);
  };

  const getProgressPercentage = (course) => {
    if (!userProgress || !userProgress.course_progress) return 0;
    const progress = userProgress.course_progress.find(p => p.course_id === course.course_id);
    if (!progress) return 0;
    return (progress.completed_lessons / course.total_lessons) * 100;
  };

  return (
    <div className="education-platform-dashboard">
      <div className="dashboard-header">
        <h1>Investment Education Platform</h1>
        <p className="subtitle">Phase 21: Investment Education & Learning Platform</p>
      </div>

      <div className="dashboard-content">
        {/* User Progress Summary */}
        {userProgress && (
          <div className="progress-summary-panel">
            <h2>Your Learning Progress</h2>
            <div className="progress-metrics">
              <div className="metric-card">
                <div className="metric-label">Courses Enrolled</div>
                <div className="metric-value">{userProgress.courses_enrolled || 0}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Lessons Completed</div>
                <div className="metric-value">{userProgress.lessons_completed || 0}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Certifications</div>
                <div className="metric-value">{certifications.length}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Learning Streak</div>
                <div className="metric-value">{userProgress.learning_streak_days || 0} days</div>
              </div>
            </div>
          </div>
        )}

        {/* Course Catalog */}
        <div className="courses-panel">
          <h2>Course Catalog</h2>
          {courses.length > 0 ? (
            <div className="courses-list">
              {courses.map((course) => {
                const progress = getProgressPercentage(course);
                return (
                  <div key={course.course_id} className="course-card">
                    <div className="course-header">
                      <h3>{course.course_name}</h3>
                      <span className="course-level">{course.difficulty_level}</span>
                    </div>
                    <p className="course-description">{course.description}</p>
                    <div className="course-meta">
                      <span>{course.total_lessons} lessons</span>
                      <span>{course.estimated_hours} hours</span>
                      {progress > 0 && (
                        <span className="progress-text">{progress.toFixed(0)}% complete</span>
                      )}
                    </div>
                    {progress > 0 && (
                      <div className="progress-bar-container">
                        <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                      </div>
                    )}
                    <button
                      onClick={() => handleEnroll(course.course_id)}
                      disabled={loading || progress > 0}
                      className="enroll-button"
                    >
                      {progress > 0 ? 'Continue Learning' : 'Enroll Now'}
                    </button>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="no-data">No courses available</div>
          )}
        </div>

        {/* Certifications */}
        <div className="certifications-panel">
          <h2>Your Certifications</h2>
          {certifications.length > 0 ? (
            <div className="certifications-list">
              {certifications.map((cert) => (
                <div key={cert.certification_id} className="certification-card">
                  <div className="cert-header">
                    <h3>{cert.certification_name}</h3>
                    <span className="cert-status">Certified</span>
                  </div>
                  <div className="cert-details">
                    <span>Issued: {new Date(cert.issued_date).toLocaleDateString()}</span>
                    <span>Score: {cert.score || 'N/A'}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No certifications earned yet</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EducationPlatformDashboard;
