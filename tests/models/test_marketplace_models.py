"""
Tests for Marketplace Pydantic Models
Phase 7: Model Validation Tests
"""

import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.marketplace import (
    ExtensionStatus,
    Extension,
    ExtensionReview
)


class TestExtensionStatusEnum:
    """Tests for ExtensionStatus enum."""
    
    def test_extension_status_enum(self):
        """Test extension status enum values."""
        assert ExtensionStatus.DRAFT == "draft"
        assert ExtensionStatus.PUBLISHED == "published"
        assert ExtensionStatus.ARCHIVED == "archived"


class TestExtension:
    """Tests for Extension model."""
    
    def test_valid_extension(self):
        """Test valid extension creation."""
        extension = Extension(
            extension_id='ext_1',
            developer_id='dev_1',
            extension_name='Test Extension',
            description='Test description',
            version='1.0.0',
            status=ExtensionStatus.PUBLISHED,
            price=9.99,
            category='analytics',
            install_count=100,
            rating=4.5,
            review_count=20,
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert extension.extension_id == 'ext_1'
        assert extension.status == ExtensionStatus.PUBLISHED
        assert extension.price == 9.99
    
    def test_extension_defaults(self):
        """Test extension with default values."""
        extension = Extension(
            extension_id='ext_1',
            developer_id='dev_1',
            extension_name='Test Extension',
            description='Test description',
            version='1.0.0',
            category='analytics',
            created_date=datetime.now(),
            updated_date=datetime.now()
        )
        assert extension.status == ExtensionStatus.DRAFT
        assert extension.price == 0.0
        assert extension.install_count == 0


class TestExtensionReview:
    """Tests for ExtensionReview model."""
    
    def test_valid_extension_review(self):
        """Test valid extension review creation."""
        review = ExtensionReview(
            review_id='review_1',
            extension_id='ext_1',
            user_id='user_1',
            rating=5,
            comment='Great extension!',
            created_date=datetime.now()
        )
        assert review.review_id == 'review_1'
        assert review.rating == 5
    
    def test_extension_review_rating_validation(self):
        """Test extension review rating validation."""
        # Should fail if rating < 1
        with pytest.raises(ValidationError):
            ExtensionReview(
                review_id='review_1',
                extension_id='ext_1',
                user_id='user_1',
                rating=0,
                created_date=datetime.now()
            )
        
        # Should fail if rating > 5
        with pytest.raises(ValidationError):
            ExtensionReview(
                review_id='review_1',
                extension_id='ext_1',
                user_id='user_1',
                rating=6,
                created_date=datetime.now()
            )
