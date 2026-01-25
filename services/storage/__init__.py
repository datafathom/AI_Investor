"""
Storage services module.
"""

from services.storage.s3_service import S3Service, get_s3_service, DocumentMetadata, UploadResult

__all__ = ['S3Service', 'get_s3_service', 'DocumentMetadata', 'UploadResult']
