"""
Log Aggregation Service
Centralized log collection and forwarding
"""

import os
import logging
import json
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class LogLevel(Enum):
    """Log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogAggregator:
    """Centralized log aggregation service."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogAggregator, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._backends = []
            self._init_backends()
    
    def _init_backends(self):
        """Initialize log backends."""
        # CloudWatch Logs
        if os.getenv('CLOUDWATCH_LOG_GROUP'):
            try:
                from services.monitoring.cloudwatch_logger import CloudWatchLogger
                self._backends.append(CloudWatchLogger())
                logger.info("CloudWatch logging initialized")
            except ImportError:
                logger.warning("CloudWatch logger not available")
        
        # ELK Stack (Elasticsearch)
        if os.getenv('ELASTICSEARCH_URL'):
            try:
                from services.monitoring.elasticsearch_logger import ElasticsearchLogger
                self._backends.append(ElasticsearchLogger())
                logger.info("Elasticsearch logging initialized")
            except ImportError:
                logger.warning("Elasticsearch logger not available")
        
        # Loki
        if os.getenv('LOKI_URL'):
            try:
                from services.monitoring.loki_logger import LokiLogger
                self._backends.append(LokiLogger())
                logger.info("Loki logging initialized")
            except ImportError:
                logger.warning("Loki logger not available")
    
    def log(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None):
        """Log message to all backends."""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': level.value,
            'message': message,
            'service': 'ai-investor-backend',
            'context': context or {}
        }
        
        for backend in self._backends:
            try:
                backend.send_log(log_entry)
            except Exception as e:
                logger.error(f"Failed to send log to backend: {e}")
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log debug message."""
        self.log(LogLevel.DEBUG, message, context)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log info message."""
        self.log(LogLevel.INFO, message, context)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log warning message."""
        self.log(LogLevel.WARNING, message, context)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log error message."""
        self.log(LogLevel.ERROR, message, context)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log critical message."""
        self.log(LogLevel.CRITICAL, message, context)


def get_log_aggregator() -> LogAggregator:
    """Get log aggregator instance."""
    return LogAggregator()
