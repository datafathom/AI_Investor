"""
Loki Logging Integration
"""

import os
import logging
import json
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class LokiLogger:
    """Loki logger."""
    
    def __init__(self):
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required")
        
        self.loki_url = os.getenv('LOKI_URL', 'http://localhost:3100')
        self.endpoint = f"{self.loki_url}/loki/api/v1/push"
        self.labels = {
            'job': 'ai-investor-backend',
            'service': 'backend'
        }
    
    def send_log(self, log_entry: Dict[str, Any]):
        """Send log entry to Loki."""
        try:
            # Convert log entry to Loki format
            timestamp_ns = int(datetime.fromisoformat(log_entry['timestamp']).timestamp() * 1e9)
            
            # Create log line
            log_line = json.dumps({
                'level': log_entry['level'],
                'message': log_entry['message'],
                'context': log_entry.get('context', {})
            })
            
            # Loki push format
            payload = {
                'streams': [{
                    'stream': self.labels,
                    'values': [[str(timestamp_ns), log_line]]
                }]
            }
            
            response = requests.post(
                self.endpoint,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to send log to Loki: {e}")
