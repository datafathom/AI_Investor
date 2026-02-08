
import logging
import json
from datetime import timezone, datetime
from typing import List, Dict, Any, Optional
from services.system.tracing_service import trace # Ensure trace is imported if used, strictly speaking trace is used in line 25
try:
    from pythonjsonlogger import jsonlogger
    BaseFormatter = jsonlogger.JsonFormatter
except ImportError:
    class BaseFormatter(logging.Formatter):
        def add_fields(self, log_record, record, message_dict):
            pass

class TraceCorrelationFormatter(BaseFormatter):
    """
    JSON Formatter that injects OpenTelemetry trace/span IDs for correlation.
    """
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp if not present
        if not log_record.get('timestamp'):
            now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
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

    def list_log_files(self) -> List[str]:
        """List all .log and .txt files in the logs directory."""
        import os
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            return []
        return [f for f in os.listdir(log_dir) if f.endswith(('.log', '.txt'))]

    def tail_file(self, filename: str, lines: int = 50) -> List[str]:
        """Read the last N lines of a log file."""
        import os
        log_dir = os.path.join(os.getcwd(), 'logs')
        file_path = os.path.join(log_dir, filename)
        if not os.path.exists(file_path):
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.readlines()
                return [line.strip() for line in content[-lines:]]
        except Exception as e:
            logger.error(f"Error reading log file {filename}: {e}")
            return [f"ERROR_READING_FILE: {str(e)}"]

    def search(self, query: str = None, level: str = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Search across major log files (backend_debug.log, backend_full.log)."""
        import os
        results = []
        log_dir = os.path.join(os.getcwd(), 'logs')
        files_to_search = ['backend_debug.log', 'backend_full.log', 'backend_log.txt']
        
        for fname in files_to_search:
            fpath = os.path.join(log_dir, fname)
            if not os.path.exists(fpath):
                continue
            
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if query and query.lower() not in line.lower():
                            continue
                        if level and level.upper() not in line.upper():
                            continue
                        
                        results.append({
                            "file": fname,
                            "content": line.strip()
                        })
                        if len(results) >= limit + offset:
                            break
            except Exception:
                continue
                
        return results[offset:offset+limit]

def get_logging_service() -> LoggingService:
    return LoggingService()
