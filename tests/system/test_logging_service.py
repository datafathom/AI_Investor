
import logging
import json
import pytest
from io import StringIO
from unittest.mock import MagicMock, patch
from services.system.logging_service import LoggingService, TraceCorrelationFormatter

@pytest.fixture
def logging_service():
    # Reset singleton
    LoggingService._instance = None
    return LoggingService()

def test_json_formatting():
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    formatter = TraceCorrelationFormatter('%(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('test_json')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    logger.info("Test message", extra={'custom_field': 'value'})
    
    output = log_capture.getvalue()
    log_entry = json.loads(output)
    
    assert log_entry['message'] == "Test message"
    assert log_entry['custom_field'] == "value"
    assert 'timestamp' in log_entry
    assert 'level' in log_entry
    assert log_entry['level'] == 'INFO'

@patch('opentelemetry.trace.get_current_span')
def test_trace_correlation(mock_get_span):
    # Mock a valid span
    mock_span = MagicMock()
    mock_span.get_span_context().is_valid = True
    mock_span.get_span_context().trace_id = 0x12345678123456781234567812345678
    mock_span.get_span_context().span_id = 0x1234567812345678
    mock_get_span.return_value = mock_span
    
    log_capture = StringIO()
    handler = logging.StreamHandler(log_capture)
    formatter = TraceCorrelationFormatter('%(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('test_trace')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    logger.info("Trace correlation test")
    
    output = log_capture.getvalue()
    log_entry = json.loads(output)
    
    assert log_entry['trace_id'] == "12345678123456781234567812345678"
    assert log_entry['span_id'] == "1234567812345678"
