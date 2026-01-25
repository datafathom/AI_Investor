"""
Vault Secret Manager
Production-ready secret management using HashiCorp Vault or AWS Secrets Manager
"""

import os
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class SecretManagerInterface(ABC):
    """Abstract interface for secret managers."""
    
    @abstractmethod
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a secret value."""
        pass
    
    @abstractmethod
    def set_secret(self, key: str, value: str) -> bool:
        """Set a secret value."""
        pass
    
    @abstractmethod
    def delete_secret(self, key: str) -> bool:
        """Delete a secret."""
        pass


class VaultSecretManager(SecretManagerInterface):
    """HashiCorp Vault secret manager."""
    
    def __init__(self, vault_addr: Optional[str] = None, vault_token: Optional[str] = None):
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR', 'http://localhost:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN')
        self._client = None
        
        if self.vault_token:
            try:
                import hvac
                self._client = hvac.Client(url=self.vault_addr, token=self.vault_token)
                # Verify connection
                if not self._client.is_authenticated():
                    logger.warning("Vault authentication failed")
                    self._client = None
            except ImportError:
                logger.warning("hvac library not installed. Install with: pip install hvac")
            except Exception as e:
                logger.error(f"Failed to initialize Vault client: {e}")
                self._client = None
    
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get secret from Vault."""
        if not self._client:
            logger.warning("Vault client not available, falling back to environment variable")
            return os.getenv(key, default)
        
        try:
            # Vault path format: secret/data/{key}
            secret_path = f"secret/data/{key}"
            response = self._client.secrets.kv.v2.read_secret_version(path=key)
            if response and 'data' in response and 'data' in response['data']:
                return response['data']['data'].get('value', default)
        except Exception as e:
            logger.error(f"Failed to get secret from Vault: {e}")
            # Fallback to environment variable
            return os.getenv(key, default)
        
        return default
    
    def set_secret(self, key: str, value: str) -> bool:
        """Set secret in Vault."""
        if not self._client:
            logger.error("Vault client not available")
            return False
        
        try:
            self._client.secrets.kv.v2.create_or_update_secret(
                path=key,
                secret={'value': value}
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set secret in Vault: {e}")
            return False
    
    def delete_secret(self, key: str) -> bool:
        """Delete secret from Vault."""
        if not self._client:
            return False
        
        try:
            self._client.secrets.kv.v2.delete_metadata_and_all_versions(path=key)
            return True
        except Exception as e:
            logger.error(f"Failed to delete secret from Vault: {e}")
            return False


class AWSSecretsManager(SecretManagerInterface):
    """AWS Secrets Manager implementation."""
    
    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self._client = None
        
        try:
            import boto3
            self._client = boto3.client('secretsmanager', region_name=self.region)
        except ImportError:
            logger.warning("boto3 not installed. Install with: pip install boto3")
        except Exception as e:
            logger.error(f"Failed to initialize AWS Secrets Manager: {e}")
            self._client = None
    
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get secret from AWS Secrets Manager."""
        if not self._client:
            logger.warning("AWS Secrets Manager not available, falling back to environment variable")
            return os.getenv(key, default)
        
        try:
            response = self._client.get_secret_value(SecretId=key)
            if 'SecretString' in response:
                import json
                secret_data = json.loads(response['SecretString'])
                # If secret is a JSON object, try to get 'value' key, otherwise return the whole thing
                if isinstance(secret_data, dict) and 'value' in secret_data:
                    return secret_data['value']
                elif isinstance(secret_data, str):
                    return secret_data
                else:
                    return str(secret_data)
        except self._client.exceptions.ResourceNotFoundException:
            logger.debug(f"Secret {key} not found in AWS Secrets Manager")
            return os.getenv(key, default)
        except Exception as e:
            logger.error(f"Failed to get secret from AWS Secrets Manager: {e}")
            return os.getenv(key, default)
        
        return default
    
    def set_secret(self, key: str, value: str) -> bool:
        """Set secret in AWS Secrets Manager."""
        if not self._client:
            return False
        
        try:
            import json
            # Try to update existing secret
            try:
                self._client.update_secret(
                    SecretId=key,
                    SecretString=json.dumps({'value': value})
                )
            except self._client.exceptions.ResourceNotFoundException:
                # Create new secret
                self._client.create_secret(
                    Name=key,
                    SecretString=json.dumps({'value': value})
                )
            return True
        except Exception as e:
            logger.error(f"Failed to set secret in AWS Secrets Manager: {e}")
            return False
    
    def delete_secret(self, key: str) -> bool:
        """Delete secret from AWS Secrets Manager."""
        if not self._client:
            return False
        
        try:
            self._client.delete_secret(SecretId=key, ForceDeleteWithoutRecovery=True)
            return True
        except Exception as e:
            logger.error(f"Failed to delete secret from AWS Secrets Manager: {e}")
            return False


class ProductionSecretManager:
    """Production secret manager that uses Vault or AWS Secrets Manager."""
    
    _instance = None
    _manager: Optional[SecretManagerInterface] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductionSecretManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance
    
    def _init_manager(self):
        """Initialize the appropriate secret manager."""
        vault_enabled = os.getenv('VAULT_ENABLED', 'false').lower() == 'true'
        aws_secrets_enabled = os.getenv('AWS_SECRETS_ENABLED', 'false').lower() == 'true'
        
        if vault_enabled:
            logger.info("Initializing HashiCorp Vault secret manager")
            self._manager = VaultSecretManager()
        elif aws_secrets_enabled:
            logger.info("Initializing AWS Secrets Manager")
            self._manager = AWSSecretsManager()
        else:
            logger.warning("No production secret manager configured. Using environment variables only.")
            self._manager = None
    
    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get secret from configured manager or environment."""
        if self._manager:
            return self._manager.get_secret(key, default)
        return os.getenv(key, default)
    
    def set_secret(self, key: str, value: str) -> bool:
        """Set secret in configured manager."""
        if self._manager:
            return self._manager.set_secret(key, value)
        logger.warning("No secret manager configured, cannot set secret")
        return False
    
    def delete_secret(self, key: str) -> bool:
        """Delete secret from configured manager."""
        if self._manager:
            return self._manager.delete_secret(key)
        return False


def get_production_secret_manager() -> ProductionSecretManager:
    """Get the production secret manager instance."""
    return ProductionSecretManager()
