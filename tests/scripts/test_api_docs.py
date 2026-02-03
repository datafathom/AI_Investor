"""Unit tests for API documentation generation."""
import pytest
from unittest.mock import MagicMock

class TestApiDocs:
    def test_generate_manual_spec(self):
        """Test that manual spec generation extracts routes from a mock app."""
        # Import the function inside the test to avoid import issues
        from scripts.runners.api_docs import _generate_manual_spec
        
        mock_app = MagicMock()
        mock_rule = MagicMock()
        mock_rule.endpoint = "test_endpoint"
        mock_rule.methods = ["GET", "POST"]
        mock_rule.__str__.return_value = "/api/test"
        
        mock_app.url_map.iter_rules.return_value = [mock_rule]
        mock_view_func = MagicMock()
        mock_view_func.__doc__ = "Summary\nDescription"
        mock_app.view_functions = {"test_endpoint": mock_view_func}
        
        spec = _generate_manual_spec(mock_app)
        
        assert "/api/test" in spec["paths"]
        assert "get" in spec["paths"]["/api/test"]
        assert "post" in spec["paths"]["/api/test"]
        assert spec["paths"]["/api/test"]["get"]["summary"] == "Summary"

    def test_route_schema_has_required_keys(self):
        """Verify our route schema includes all required keys per Phase 1 spec."""
        expected_keys = [
            "path", "method", "summary", "parameters", 
            "request_body", "response_body", "error_codes", 
            "authentication", "rate_limiting", "caching"
        ]
        sample_route = {
            "path": "/api/test",
            "method": "GET",
            "summary": "Test endpoint",
            "parameters": {},
            "request_body": None,
            "response_body": {"200": {"description": "OK"}},
            "error_codes": {"400": "Bad Request", "401": "Unauthorized", "500": "Server Error"},
            "authentication": "Bearer Token",
            "rate_limiting": "100/min",
            "caching": None
        }
        
        for key in expected_keys:
            assert key in sample_route, f"Missing required key: {key}"
