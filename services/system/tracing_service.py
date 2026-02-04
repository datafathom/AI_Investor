import os
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
try:
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    HAS_FLASK_INSTRUMENTOR = True
except ImportError:
    HAS_FLASK_INSTRUMENTOR = False
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class TracingService:
    """
    Service for managing distributed tracing via OpenTelemetry.
    """
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TracingService, cls).__new__(cls)
        return cls._instance

    def initialize(self, app=None):
        """Initializes OpenTelemetry tracing."""
        if self._is_initialized:
            return

        # Check if tracing is enabled
        enabled = os.getenv('ENABLE_TRACING', 'false').lower() == 'true'
        if not enabled:
            logger.info("Tracing is disabled (ENABLE_TRACING != true)")
            return

        sm = get_secret_manager()
        endpoint = sm.get_secret('OTLP_ENDPOINT', 'http://localhost:4317')
        service_name = sm.get_secret('SERVICE_NAME', 'ai-investor-backend')
        
        try:
            # Set up TracerProvider if not already set
            provider = TracerProvider()
            
            # Use OTLP Exporter (Jaeger/Collector)
            otlp_exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
            span_processor = BatchSpanProcessor(otlp_exporter)
            provider.add_span_processor(span_processor)
            
            trace.set_tracer_provider(provider)
            
            if app:
                if HAS_FLASK_INSTRUMENTOR:
                    FlaskInstrumentor().instrument_app(app)
                    logger.info(f"Flask application instrumented for tracing (service: {service_name})")
                else:
                    logger.warning("FlaskInstrumentor not available, skipping instrumentation.")
            
            self._is_initialized = True
            logger.info(f"TracingService initialized with endpoint: {endpoint}")
        except Exception as e:
            logger.error(f"Failed to initialize TracingService: {e}")
            # Ensure we don't partially initialize
            self._is_initialized = False

    def get_tracer(self, name: str):
        """Returns a tracer instance."""
        if not self._is_initialized:
            # Fallback to no-op tracer if not initialized
            return trace.get_tracer(name)
        return trace.get_tracer(name)

def get_tracing_service() -> TracingService:
    return TracingService()
