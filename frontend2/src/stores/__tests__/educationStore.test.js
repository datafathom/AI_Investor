/**
 * Education Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import useEducationStore from '../educationStore';
import apiClient from '../../services/apiClient';

// Mock apiClient
vi.mock('../../services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('educationStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useEducationStore.setState({
      isEducationMode: false,
      activeTutorial: null,
      currentStepIndex: 0,
      isPlaying: false,
      completedTutorials: [],
      courses: [],
      userProgress: null,
      certifications: [],
      loading: false,
      error: null,
    });
  });

  it('should toggle education mode', () => {
    expect(useEducationStore.getState().isEducationMode).toBe(false);
    useEducationStore.getState().toggleEducationMode();
    expect(useEducationStore.getState().isEducationMode).toBe(true);
  });

  it('should fetch courses successfully (Wrapped Pattern)', async () => {
    const mockCourses = [{ id: 1, title: 'Investing 101' }];
    apiClient.get.mockResolvedValueOnce({ data: { data: mockCourses } });

    await useEducationStore.getState().fetchCourses();

    expect(apiClient.get).toHaveBeenCalledWith('/education/courses');
    expect(useEducationStore.getState().courses).toEqual(mockCourses);
  });

  it('should fetch user progress (Flat Pattern fallback)', async () => {
    const mockProgress = { userId: 'user1', completed: 5 };
    // Test that it handles flat response too
    apiClient.get.mockResolvedValueOnce({ data: mockProgress });

    await useEducationStore.getState().fetchUserProgress('user1');

    expect(useEducationStore.getState().userProgress).toEqual(mockProgress);
  });

  it('should start and stop tutorial', () => {
    useEducationStore.getState().startTutorial('tutorial-1');
    expect(useEducationStore.getState().activeTutorial).toBe('tutorial-1');
    expect(useEducationStore.getState().isPlaying).toBe(true);

    useEducationStore.getState().stopTutorial();
    expect(useEducationStore.getState().activeTutorial).toBeNull();
    expect(useEducationStore.getState().isPlaying).toBe(false);
  });

  it('should handle tutorial completion', async () => {
    const mockResult = { completed_tutorials: ['tutorial-1'] };
    apiClient.post.mockResolvedValueOnce({ data: { data: mockResult } });

    useEducationStore.getState().startTutorial('tutorial-1');
    // nextStep when currentStepIndex === totalSteps - 1 triggers completion
    await useEducationStore.getState().nextStep(1); 

    expect(apiClient.post).toHaveBeenCalledWith('/education/complete', expect.any(Object));
    expect(useEducationStore.getState().completedTutorials).toEqual(['tutorial-1']);
    expect(useEducationStore.getState().activeTutorial).toBeNull();
  });
});
