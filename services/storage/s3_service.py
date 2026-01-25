"""
==============================================================================
FILE: services/storage/s3_service.py
ROLE: Document Storage Service
PURPOSE: Provides secure document storage and retrieval via AWS S3. All files
         are encrypted at rest and accessed via presigned URLs.

INTEGRATION POINTS:
    - TaxService: Tax document storage
    - ReportGenerator: Generated report storage
    - UserService: Profile and uploaded document storage
    - DocumentAPI: REST endpoints for document management

SECURITY:
    - AES-256 encryption at rest
    - Presigned URLs expire after configurable duration
    - Bucket policies block public access
    - Object versioning enabled

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

import logging
import hashlib
import mimetypes
import uuid
from typing import Optional, Dict, Any, BinaryIO
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
    from botocore.config import Config
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    logger.warning("boto3 not installed. Install with: pip install boto3")


@dataclass
class DocumentMetadata:
    """Document metadata stored in database"""
    document_id: str
    user_id: str
    s3_key: str
    bucket: str
    filename: str
    content_type: str
    size_bytes: int
    checksum: str
    uploaded_at: str
    expires_at: Optional[str] = None
    category: str = "general"  # tax, kyc, report, user_upload


@dataclass
class UploadResult:
    """Result of file upload"""
    document_id: str
    s3_key: str
    bucket: str
    size_bytes: int
    checksum: str
    etag: Optional[str] = None


class S3Service:
    """
    AWS S3 storage service for secure document management.
    Supports encryption, presigned URLs, and multipart uploads.
    """
    
    # Bucket names by category
    BUCKETS = {
        "tax": "ai-investor-tax-docs",
        "kyc": "ai-investor-kyc-docs",
        "report": "ai-investor-reports",
        "user_upload": "ai-investor-user-uploads",
        "general": "ai-investor-documents"
    }
    
    # Multipart upload threshold (5MB)
    MULTIPART_THRESHOLD = 5 * 1024 * 1024
    
    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: str = "us-east-1",
        mock: bool = False
    ):
        """
        Initialize S3 service.
        
        Args:
            aws_access_key_id: AWS access key (if None, uses environment/IAM)
            aws_secret_access_key: AWS secret key (if None, uses environment/IAM)
            region_name: AWS region
            mock: If True, uses mock storage instead of live S3
        """
        self.mock = mock
        self.region = region_name
        
        if not mock and BOTO3_AVAILABLE:
            try:
                config = Config(
                    signature_version='s3v4',
                    s3={
                        'addressing_style': 'path'
                    }
                )
                
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name,
                    config=config
                )
                
                # Test connection
                self.s3_client.list_buckets()
                logger.info("S3 service initialized (live mode)")
            except Exception as e:
                logger.warning(f"S3 initialization failed, using mock: {e}")
                self.mock = True
                self.s3_client = None
        else:
            self.s3_client = None
            if not BOTO3_AVAILABLE:
                logger.warning("boto3 not available. Using mock mode.")
                self.mock = True
    
    def _get_bucket(self, category: str = "general") -> str:
        """Get bucket name for category"""
        return self.BUCKETS.get(category, self.BUCKETS["general"])
    
    def _generate_s3_key(self, user_id: str, filename: str, category: str = "general") -> str:
        """
        Generate S3 object key.
        Format: {category}/{user_id}/{year}/{month}/{uuid}-{filename}
        """
        now = datetime.now()
        doc_id = str(uuid.uuid4())
        safe_filename = filename.replace(" ", "_").replace("/", "_")
        return f"{category}/{user_id}/{now.year}/{now.month:02d}/{doc_id}-{safe_filename}"
    
    def _calculate_checksum(self, content: bytes) -> str:
        """Calculate SHA-256 checksum"""
        return hashlib.sha256(content).hexdigest()
    
    def _detect_content_type(self, filename: str) -> str:
        """Detect MIME type from filename"""
        content_type, _ = mimetypes.guess_type(filename)
        return content_type or "application/octet-stream"
    
    async def upload_file(
        self,
        user_id: str,
        filename: str,
        content: bytes,
        category: str = "general",
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> UploadResult:
        """
        Upload file to S3.
        
        Args:
            user_id: Owner user ID
            filename: Original filename
            content: File content as bytes
            category: Document category (tax, kyc, report, user_upload, general)
            content_type: MIME type (auto-detected if None)
            metadata: Optional S3 metadata tags
            
        Returns:
            UploadResult with document ID and S3 key
        """
        if self.mock:
            return await self._mock_upload(user_id, filename, content, category)
        
        if not self.s3_client:
            raise RuntimeError("S3 client not initialized. Check AWS credentials.")
        
        bucket = self._get_bucket(category)
        s3_key = self._generate_s3_key(user_id, filename, category)
        content_type = content_type or self._detect_content_type(filename)
        checksum = self._calculate_checksum(content)
        document_id = str(uuid.uuid4())
        
        # Prepare metadata
        s3_metadata = {
            "user-id": user_id,
            "document-id": document_id,
            "original-filename": filename,
            "checksum": checksum,
            "uploaded-at": datetime.now().isoformat()
        }
        if metadata:
            s3_metadata.update(metadata)
        
        try:
            # Use multipart upload for large files
            if len(content) > self.MULTIPART_THRESHOLD:
                etag = await self._multipart_upload(
                    bucket, s3_key, content, content_type, s3_metadata
                )
            else:
                # Simple upload
                response = self.s3_client.put_object(
                    Bucket=bucket,
                    Key=s3_key,
                    Body=content,
                    ContentType=content_type,
                    Metadata=s3_metadata,
                    ServerSideEncryption="AES256"  # AES-256 encryption at rest
                )
                etag = response.get("ETag", "").strip('"')
            
            logger.info(f"Uploaded file to S3: {bucket}/{s3_key} ({len(content)} bytes)")
            
            return UploadResult(
                document_id=document_id,
                s3_key=s3_key,
                bucket=bucket,
                size_bytes=len(content),
                checksum=checksum,
                etag=etag
            )
            
        except ClientError as e:
            logger.error(f"S3 upload failed: {e}")
            raise RuntimeError(f"Failed to upload file to S3: {str(e)}")
    
    async def _multipart_upload(
        self,
        bucket: str,
        key: str,
        content: bytes,
        content_type: str,
        metadata: Dict[str, str]
    ) -> str:
        """Perform multipart upload for large files"""
        # Create multipart upload
        mpu = self.s3_client.create_multipart_upload(
            Bucket=bucket,
            Key=key,
            ContentType=content_type,
            Metadata=metadata,
            ServerSideEncryption="AES256"
        )
        upload_id = mpu["UploadId"]
        
        try:
            # Upload parts (5MB chunks)
            parts = []
            chunk_size = self.MULTIPART_THRESHOLD
            
            for i in range(0, len(content), chunk_size):
                part_num = (i // chunk_size) + 1
                chunk = content[i:i + chunk_size]
                
                part_response = self.s3_client.upload_part(
                    Bucket=bucket,
                    Key=key,
                    PartNumber=part_num,
                    UploadId=upload_id,
                    Body=chunk
                )
                parts.append({
                    "ETag": part_response["ETag"],
                    "PartNumber": part_num
                })
            
            # Complete multipart upload
            complete_response = self.s3_client.complete_multipart_upload(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts}
            )
            
            return complete_response.get("ETag", "").strip('"')
            
        except Exception as e:
            # Abort multipart upload on error
            try:
                self.s3_client.abort_multipart_upload(
                    Bucket=bucket,
                    Key=key,
                    UploadId=upload_id
                )
            except:
                pass
            raise
    
    def generate_presigned_url(
        self,
        s3_key: str,
        bucket: Optional[str] = None,
        expiration_seconds: int = 3600,
        category: str = "general"
    ) -> str:
        """
        Generate presigned download URL.
        
        Args:
            s3_key: S3 object key
            bucket: Bucket name (auto-detected if None)
            expiration_seconds: URL expiration time (default 1 hour)
            category: Document category (for bucket detection)
            
        Returns:
            Presigned URL string
        """
        if self.mock:
            return f"https://mock-s3.example.com/{s3_key}?expires={expiration_seconds}"
        
        if not self.s3_client:
            raise RuntimeError("S3 client not initialized.")
        
        bucket = bucket or self._get_bucket(category)
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': s3_key},
                ExpiresIn=expiration_seconds
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise RuntimeError(f"Failed to generate presigned URL: {str(e)}")
    
    async def delete_file(
        self,
        s3_key: str,
        bucket: Optional[str] = None,
        category: str = "general"
    ) -> bool:
        """
        Delete file from S3.
        
        Args:
            s3_key: S3 object key
            bucket: Bucket name (auto-detected if None)
            category: Document category
            
        Returns:
            True if deleted successfully
        """
        if self.mock:
            logger.info(f"[MOCK] Deleted file: {s3_key}")
            return True
        
        if not self.s3_client:
            raise RuntimeError("S3 client not initialized.")
        
        bucket = bucket or self._get_bucket(category)
        
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=s3_key)
            logger.info(f"Deleted file from S3: {bucket}/{s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file: {e}")
            return False
    
    async def get_file_metadata(
        self,
        s3_key: str,
        bucket: Optional[str] = None,
        category: str = "general"
    ) -> Optional[Dict[str, Any]]:
        """
        Get file metadata from S3.
        
        Returns:
            Dict with size, content_type, last_modified, metadata, or None if not found
        """
        if self.mock:
            return {
                "size": 0,
                "content_type": "application/octet-stream",
                "last_modified": datetime.now().isoformat(),
                "metadata": {}
            }
        
        if not self.s3_client:
            raise RuntimeError("S3 client not initialized.")
        
        bucket = bucket or self._get_bucket(category)
        
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=s3_key)
            return {
                "size": response.get("ContentLength", 0),
                "content_type": response.get("ContentType", "application/octet-stream"),
                "last_modified": response.get("LastModified", datetime.now()).isoformat(),
                "metadata": response.get("Metadata", {}),
                "etag": response.get("ETag", "").strip('"')
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            logger.error(f"Failed to get file metadata: {e}")
            raise
    
    async def _mock_upload(
        self,
        user_id: str,
        filename: str,
        content: bytes,
        category: str
    ) -> UploadResult:
        """Mock upload for testing"""
        import asyncio
        await asyncio.sleep(0.1)  # Simulate upload delay
        
        s3_key = self._generate_s3_key(user_id, filename, category)
        document_id = str(uuid.uuid4())
        checksum = self._calculate_checksum(content)
        
        logger.info(f"[MOCK S3] Uploaded {filename} ({len(content)} bytes) to {s3_key}")
        
        return UploadResult(
            document_id=document_id,
            s3_key=s3_key,
            bucket=self._get_bucket(category),
            size_bytes=len(content),
            checksum=checksum
        )


# Singleton instance
_s3_service: Optional[S3Service] = None


def get_s3_service(mock: bool = True) -> S3Service:
    """
    Get singleton S3 service instance.
    
    Args:
        mock: Use mock mode if True
        
    Returns:
        S3Service instance
    """
    global _s3_service
    
    if _s3_service is None:
        from config.environment_manager import get_settings
        settings = get_settings()
        
        # Use mock if no AWS credentials provided
        use_mock = mock or not hasattr(settings, 'AWS_ACCESS_KEY_ID') or not settings.AWS_ACCESS_KEY_ID
        
        _s3_service = S3Service(
            aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
            region_name=getattr(settings, 'AWS_REGION', 'us-east-1'),
            mock=use_mock
        )
        logger.info(f"S3 service initialized (mock={use_mock})")
    
    return _s3_service
