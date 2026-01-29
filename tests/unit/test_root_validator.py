import pytest
from services.neo4j.root_node_validator import RootNodeValidator

def test_root_validation_pass():
    # Since we use logging/mocking, we test the call pattern
    validator = RootNodeValidator(None)
    res = validator.validate_client_roots(["c1", "c2"])
    assert res["verified"] == True

def test_integrity_check():
    validator = RootNodeValidator(None)
    assert validator.check_graph_integrity() == True
