import os
import pytest
from unittest.mock import MagicMock, patch
from services.system.tracing_service import TracingService

@pytest.fixture
def tracing_service():
    # Reset singleton for testing
    TracingService._instance = None
    return TracingService()

def test_singleton(tracing_service):
    from services.system.tracing_service import get_tracing_service
    s2 = get_tracing_service()
    assert tracing_service is s2

@patch('opentelemetry.instrumentation.flask.FlaskInstrumentor.instrument_app')
@patch('opentelemetry.trace.set_tracer_provider')
@patch('opentelemetry.sdk.trace.TracerProvider')
@patch('services.system.tracing_service.OTLPSpanExporter')
@patch.dict(os.environ, {"ENABLE_TRACING": "true"})
def test_initialize(mock_exporter, mock_provider, mock_set_provider, mock_instrument_app, tracing_service):
    app = MagicMock()
    tracing_service.initialize(app)
    
    # Check that initialize finished successfully
    assert tracing_service._is_initialized is True
    assert mock_set_provider.called
    # The exporter class is instantiated
    assert mock_exporter.called
    assert mock_instrument_app.called

def test_get_tracer(tracing_service):
    tracer = tracing_service.get_tracer("test-tracer")
    assert tracer is not None

