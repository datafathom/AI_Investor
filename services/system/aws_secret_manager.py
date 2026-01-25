"""
AWS Secrets Manager Integration
Complete AWS Secrets Manager implementation
"""

import os
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Try to import boto3
try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    logger.warning("boto3 not available. Install with: pip install boto3")


class AWSSecretsManager:
    """AWS Secrets Manager integration."""
    
    def __init__(self, region: Optional[str] = None):
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 is required for AWS Secrets Manager")
        
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.client = boto3.client('secretsmanager', region_name=self.region)
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_secret(self, secret_name: str, use_cache: bool = True) -> Optional[str]:
        """Get secret from AWS Secrets Manager."""
        # Check cache
        if use_cache and secret_name in self.cache:
            cached = self.cache[secret_name]
            if cached['expires_at'] > self._now():
                return cached['value']
        
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            secret_value = response['SecretString']
            
            # Cache result
            if use_cache:
                self.cache[secret_name] = {
                    'value': secret_value,
                    'expires_at': self._now() + self.cache_ttl
                }
            
            return secret_value
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                logger.warning(f"Secret not found: {secret_name}")
            elif error_code == 'InvalidRequestException':
                logger.error(f"Invalid request for secret: {secret_name}")
            elif error_code == 'InvalidParameterException':
                logger.error(f"Invalid parameter for secret: {secret_name}")
            elif error_code == 'DecryptionFailureException':
                logger.error(f"Failed to decrypt secret: {secret_name}")
            else:
                logger.error(f"Error retrieving secret {secret_name}: {e}")
            return None
    
    def get_secret_json(self, secret_name: str) -> Optional[Dict]:
        """Get secret as JSON."""
        import json
        secret_value = self.get_secret(secret_name)
        if secret_value:
            try:
                return json.loads(secret_value)
            except json.JSONDecodeError:
                logger.error(f"Secret {secret_name} is not valid JSON")
        return None
    
    def create_secret(self, secret_name: str, secret_value: str, 
                     description: str = "") -> bool:
        """Create a new secret."""
        try:
            self.client.create_secret(
                Name=secret_name,
                SecretString=secret_value,
                Description=description
            )
            logger.info(f"Secret created: {secret_name}")
            return True
        except ClientError as e:
            logger.error(f"Error creating secret {secret_name}: {e}")
            return False
    
    def update_secret(self, secret_name: str, secret_value: str) -> bool:
        """Update existing secret."""
        try:
            self.client.update_secret(
                SecretId=secret_name,
                SecretString=secret_value
            )
            # Invalidate cache
            self.cache.pop(secret_name, None)
            logger.info(f"Secret updated: {secret_name}")
            return True
        except ClientError as e:
            logger.error(f"Error updating secret {secret_name}: {e}")
            return False
    
    def delete_secret(self, secret_name: str, force: bool = False) -> bool:
        """Delete secret."""
        try:
            if force:
                self.client.delete_secret(
                    SecretId=secret_name,
                    ForceDeleteWithoutRecovery=True
                )
            else:
                self.client.delete_secret(SecretId=secret_name)
            
            # Invalidate cache
            self.cache.pop(secret_name, None)
            logger.info(f"Secret deleted: {secret_name}")
            return True
        except ClientError as e:
            logger.error(f"Error deleting secret {secret_name}: {e}")
            return False
    
    def list_secrets(self, prefix: Optional[str] = None) -> List[str]:
        """List all secrets (optionally filtered by prefix)."""
        try:
            secrets = []
            paginator = self.client.get_paginator('list_secrets')
            
            for page in paginator.paginate():
                for secret in page['SecretList']:
                    name = secret['Name']
                    if prefix is None or name.startswith(prefix):
                        secrets.append(name)
            
            return secrets
        except ClientError as e:
            logger.error(f"Error listing secrets: {e}")
            return []
    
    def rotate_secret(self, secret_name: str) -> bool:
        """Trigger secret rotation."""
        try:
            self.client.rotate_secret(SecretId=secret_name)
            # Invalidate cache
            self.cache.pop(secret_name, None)
            logger.info(f"Secret rotation triggered: {secret_name}")
            return True
        except ClientError as e:
            logger.error(f"Error rotating secret {secret_name}: {e}")
            return False
    
    def _now(self) -> int:
        """Get current timestamp."""
        import time
        return int(time.time())


def get_aws_secret_manager(region: Optional[str] = None) -> AWSSecretsManager:
    """Get AWS Secrets Manager instance."""
    return AWSSecretsManager(region=region)
