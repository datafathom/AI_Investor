# Backend Service: Storage (The Archive)

## Overview
The **Storage Service** provides secure document storage via AWS S3. All files are encrypted at rest (AES-256) and accessed via time-limited presigned URLs. It supports multipart uploads for large files and organizes documents by category.

## Core Components

### 1. S3 Service (`s3_service.py`)
- **Category Buckets**: Separate buckets for `tax`, `kyc`, `report`, `user_upload`, and `general` documents.
- **Encryption**: All objects are encrypted at rest using AWS S3-managed keys (AES-256).
- **Presigned URLs**: Secure, time-limited (default 1 hour) download links.
- **Multipart Upload**: Efficient upload of large files (>5MB) in chunks.
- **Checksum Verification**: SHA-256 checksums for data integrity.

## Frontend Integration Mapping

| Page / Component | Widget | Service Logic Used | Frontend Status |
| :--- | :--- | :--- | :--- |
| **Documents Page** | File Uploader | `s3_service.upload_file()` | **Partially Implemented** |
| **Tax Center** | Document Viewer | `s3_service.generate_presigned_url()` | **Implicit** |

## Usage Example

```python
from services.storage.s3_service import get_s3_service
import asyncio

s3 = get_s3_service()

async def main():
    # Upload a tax document
    with open("W2_2025.pdf", "rb") as f:
        content = f.read()
    
    result = await s3.upload_file(
        user_id="user_123",
        filename="W2_2025.pdf",
        content=content,
        category="tax"
    )
    
    print(f"Uploaded as: {result.s3_key}")
    
    # Generate download URL
    url = s3.generate_presigned_url(result.s3_key, category="tax")
    print(f"Download URL: {url}")

asyncio.run(main())
```
