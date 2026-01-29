"""
Unit tests for Emotional Muffler Logic.
Verifies time-based locks and tilt detection spamming.
"""
import pytest
import time
from datetime import datetime
from services.risk.lock_manager import LockManager
from services.risk.tilt_detector import TiltDetector

def test_lock_application():
    manager = LockManager()
    user_id = "trader_01"
    
    # 1. No lock initially
    locked, _ = manager.is_user_locked(user_id)
    assert locked == False

    # 2. Apply 4-hour lock
    manager.apply_lock(user_id, duration_hours=4)
    locked, reason = manager.is_user_locked(user_id)
    assert locked == True
    assert "COOLING_OFF" in reason
    assert "3h 59m" in reason or "4h 0m" in reason

def test_tilt_detection():
    detector = TiltDetector()
    
    # Simulate 9 rapid clicks (Below threshold)
    for _ in range(9):
        is_tilt = detector.record_attempt()
        assert is_tilt == False
    
    # 10th click (Threshold hit)
    is_tilt = detector.record_attempt()
    assert is_tilt == True

def test_tilt_reset():
    detector = TiltDetector()
    for _ in range(5):
        detector.record_attempt()
    
    detector.reset()
    assert len(detector.failed_attempts) == 0
