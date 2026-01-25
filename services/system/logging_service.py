
import logging
import json
from pythonjsonlogger import jsonlogger
from opentelemetry import trace
from datetime import datetime

class TraceCorrelationFormatter(jsonlogger.JsonFormatter):
    """
    JSON Formatter that injects OpenTelemetry trace/span IDs for correlation.
    """
    def add_fields(self, log_record, record, message_dict):
        super(TraceCorrelationFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add timestamp if not present
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now

        # Add trace context
        span = trace.get_current_span()
        if span and span.get_span_context().is_valid:
            log_record['trace_id'] = format(span.get_span_context().trace_id, '032x')
            log_record['span_id'] = format(span.get_span_context().span_id, '016x')
        
        # Add log level
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

class LoggingService:
    """
    Service for managing structured JSON logging with distributed tracing correlation.
    """
    _instance = None
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggingService, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """Configures the root logger to use JSON formatting with trace correlation."""
        if self._is_initialized:
            return

        handler = logging.StreamHandler()
        formatter = TraceCorrelationFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
        handler.setFormatter(formatter)

        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.INFO)
        
        # Suppress some noisy loggers
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        
        self._is_initialized = True
        logging.info("LoggingService initialized with JSON formatting and trace correlation.")

def get_logging_service() -> LoggingService:
    return LoggingService()
