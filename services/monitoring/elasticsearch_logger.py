"""
Elasticsearch Logging Integration
"""

import os
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from elasticsearch import Elasticsearch
    ELASTICSEARCH_AVAILABLE = True
except ImportError:
    ELASTICSEARCH_AVAILABLE = False


class ElasticsearchLogger:
    """Elasticsearch logger."""
    
    def __init__(self):
        if not ELASTICSEARCH_AVAILABLE:
            raise ImportError("elasticsearch library required")
        
        es_url = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
        self.index_prefix = os.getenv('ELASTICSEARCH_INDEX_PREFIX', 'ai-investor')
        
        self.client = Elasticsearch([es_url])
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure index exists."""
        index_name = f"{self.index_prefix}-{datetime.utcnow().strftime('%Y.%m')}"
        try:
            if not self.client.indices.exists(index=index_name):
                self.client.indices.create(
                    index=index_name,
                    body={
                        'settings': {
                            'number_of_shards': 1,
                            'number_of_replicas': 0
                        },
                        'mappings': {
                            'properties': {
                                'timestamp': {'type': 'date'},
                                'level': {'type': 'keyword'},
                                'message': {'type': 'text'},
                                'service': {'type': 'keyword'},
                                'context': {'type': 'object'}
                            }
                        }
                    }
                )
        except Exception as e:
            logger.error(f"Failed to create Elasticsearch index: {e}")
    
    def send_log(self, log_entry: Dict[str, Any]):
        """Send log entry to Elasticsearch."""
        try:
            index_name = f"{self.index_prefix}-{datetime.utcnow().strftime('%Y.%m')}"
            self.client.index(index=index_name, body=log_entry)
        except Exception as e:
            logger.error(f"Failed to send log to Elasticsearch: {e}")
