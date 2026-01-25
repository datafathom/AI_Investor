"""
CloudWatch Logs Integration
"""

import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False


class CloudWatchLogger:
    """CloudWatch Logs logger."""
    
    def __init__(self):
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 required for CloudWatch logging")
        
        self.log_group = os.getenv('CLOUDWATCH_LOG_GROUP', 'ai-investor')
        self.log_stream = os.getenv('CLOUDWATCH_LOG_STREAM', 'backend')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        
        self.client = boto3.client('logs', region_name=self.region)
        self._ensure_log_group()
        self._sequence_token = None
    
    def _ensure_log_group(self):
        """Ensure log group exists."""
        try:
            self.client.create_log_group(logGroupName=self.log_group)
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                logger.error(f"Failed to create log group: {e}")
    
    def send_log(self, log_entry: Dict[str, Any]):
        """Send log entry to CloudWatch."""
        import json
        
        try:
            # Create log stream if needed
            try:
                self.client.create_log_stream(
                    logGroupName=self.log_group,
                    logStreamName=self.log_stream
                )
            except ClientError as e:
                if e.response['Error']['Code'] != 'ResourceAlreadyExistsException':
                    raise
            
            # Send log event
            response = self.client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[{
                    'timestamp': int(datetime.fromisoformat(log_entry['timestamp']).timestamp() * 1000),
                    'message': json.dumps(log_entry)
                }],
                sequenceToken=self._sequence_token
            )
            
            self._sequence_token = response.get('nextSequenceToken')
        except Exception as e:
            logger.error(f"Failed to send log to CloudWatch: {e}")
