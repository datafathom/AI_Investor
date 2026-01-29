import pytest
from services.private_banking.rm_load_balancer import RMLoadBalancer
from uuid import uuid4

def test_rm_assignment_success():
    balancer = RMLoadBalancer()
    managers = [
        {"id": uuid4(), "current_count": 48},
        {"id": uuid4(), "current_count": 20} # Lightest load
    ]
    assigned_id = balancer.assign_next_available_rm("ULTRA", managers)
    assert assigned_id == managers[1]["id"]

def test_rm_assignment_capacity_reached():
    balancer = RMLoadBalancer()
    # ULTRA cap is 50
    managers = [
        {"id": uuid4(), "current_count": 55},
        {"id": uuid4(), "current_count": 50}
    ]
    assigned_id = balancer.assign_next_available_rm("ULTRA", managers)
    assert assigned_id is None
