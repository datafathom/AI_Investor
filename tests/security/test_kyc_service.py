"""
Test KYC Service - Phase 54 Unit Tests

Tests for identity verification, document management, and regulatory filings.

Run with:
    .\\venv\\Scripts\\python.exe -m pytest tests/security/test_kyc_service.py -v
"""

import pytest
from datetime import datetime
from services.security.kyc_service import (
    KYCService,
    Document,
    DocumentType,
    VerificationStatus,
    VerificationResult,
    FilingDeadline,
    ThirteenFHolding
)


@pytest.fixture
def kyc_service() -> KYCService:
    """Create KYC service instance."""
    return KYCService()


@pytest.fixture
def sample_documents() -> list[Document]:
    """Create sample documents for testing."""
    return [
        Document(
            id="doc-1",
            document_type=DocumentType.PASSPORT,
            filename="passport.pdf",
            checksum="abc123",
            uploaded_at=datetime.now().isoformat(),
            expires_at=None,
            status=VerificationStatus.PENDING
        ),
        Document(
            id="doc-2",
            document_type=DocumentType.UTILITY_BILL,
            filename="utility.pdf",
            checksum="def456",
            uploaded_at=datetime.now().isoformat(),
            expires_at="2026-04-18",
            status=VerificationStatus.PENDING
        )
    ]


class TestKYCServiceVerification:
    """Tests for identity verification."""
    
    @pytest.mark.asyncio
    async def test_verify_identity_with_required_docs(
        self,
        kyc_service: KYCService,
        sample_documents: list[Document]
    ) -> None:
        """Test verification succeeds with required documents."""
        result = await kyc_service.verify_identity("user-1", sample_documents)
        
        assert isinstance(result, VerificationResult)
        assert result.user_id == "user-1"
        assert result.is_verified is True
        assert result.verification_level == "enhanced"
        assert len(result.missing_documents) == 0
    
    @pytest.mark.asyncio
    async def test_verify_identity_missing_docs(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test verification fails with missing required documents."""
        # Only provide passport, missing utility bill
        docs = [
            Document(
                id="doc-1",
                document_type=DocumentType.PASSPORT,
                filename="passport.pdf",
                checksum="abc123",
                uploaded_at=datetime.now().isoformat(),
                expires_at=None
            )
        ]
        
        result = await kyc_service.verify_identity("user-2", docs)
        
        assert result.is_verified is False
        assert result.verification_level == "basic"
        assert DocumentType.UTILITY_BILL in result.missing_documents
    
    @pytest.mark.asyncio
    async def test_verify_identity_accredited_investor(
        self,
        kyc_service: KYCService,
        sample_documents: list[Document]
    ) -> None:
        """Test accredited investor level with proper documents."""
        sample_documents.append(
            Document(
                id="doc-3",
                document_type=DocumentType.ACCREDITED_INVESTOR,
                filename="accredited.pdf",
                checksum="ghi789",
                uploaded_at=datetime.now().isoformat(),
                expires_at="2027-01-18"
            )
        )
        
        result = await kyc_service.verify_identity("user-3", sample_documents)
        
        assert result.verification_level == "accredited"
    
    @pytest.mark.asyncio
    async def test_verification_expiration(
        self,
        kyc_service: KYCService,
        sample_documents: list[Document]
    ) -> None:
        """Test that verification expiration is set correctly."""
        result = await kyc_service.verify_identity("user-4", sample_documents)
        
        assert result.expires_at is not None
        # Should be ~1 year from now
        expires = datetime.strptime(result.expires_at, "%Y-%m-%d")
        assert (expires - datetime.now()).days >= 364


class TestKYCServiceDocuments:
    """Tests for document management."""
    
    @pytest.mark.asyncio
    async def test_upload_document(self, kyc_service: KYCService) -> None:
        """Test document upload."""
        content = b"test document content"
        
        doc = await kyc_service.upload_document(
            user_id="user-1",
            document_type="passport",
            filename="passport.pdf",
            content=content
        )
        
        assert doc.id.startswith("doc-")
        assert doc.document_type == DocumentType.PASSPORT
        assert doc.filename == "passport.pdf"
        assert doc.status == VerificationStatus.PENDING
        assert len(doc.checksum) == 64  # SHA-256 hex
    
    @pytest.mark.asyncio
    async def test_upload_document_expiration(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test document expiration is set based on type."""
        content = b"utility bill content"
        
        doc = await kyc_service.upload_document(
            user_id="user-1",
            document_type="utility_bill",
            filename="utility.pdf",
            content=content
        )
        
        # Utility bills expire in 90 days
        assert doc.expires_at is not None
        expires = datetime.strptime(doc.expires_at, "%Y-%m-%d")
        assert (expires - datetime.now()).days >= 89
    
    @pytest.mark.asyncio
    async def test_get_user_documents(self, kyc_service: KYCService) -> None:
        """Test retrieving user documents."""
        content = b"test content"
        
        await kyc_service.upload_document("user-5", "passport", "p.pdf", content)
        await kyc_service.upload_document("user-5", "utility_bill", "u.pdf", content)
        
        docs = await kyc_service.get_user_documents("user-5")
        
        assert len(docs) == 2
    
    @pytest.mark.asyncio
    async def test_get_user_documents_empty(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test getting documents for user with none."""
        docs = await kyc_service.get_user_documents("nonexistent-user")
        
        assert docs == []
    
    @pytest.mark.asyncio
    async def test_document_checksum_integrity(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test document checksum is calculated correctly."""
        content1 = b"content one"
        content2 = b"content two"
        
        doc1 = await kyc_service.upload_document("u1", "passport", "p1.pdf", content1)
        doc2 = await kyc_service.upload_document("u1", "passport", "p2.pdf", content2)
        
        # Different content should have different checksums
        assert doc1.checksum != doc2.checksum
        
        # Same content should have same checksum
        doc3 = await kyc_service.upload_document("u2", "passport", "p1.pdf", content1)
        assert doc1.checksum == doc3.checksum


class TestKYCServiceFilings:
    """Tests for regulatory filing features."""
    
    @pytest.mark.asyncio
    async def test_get_filing_calendar(self, kyc_service: KYCService) -> None:
        """Test getting filing calendar."""
        deadlines = await kyc_service.get_filing_calendar()
        
        assert isinstance(deadlines, list)
        assert len(deadlines) >= 1
        
        for d in deadlines:
            assert isinstance(d, FilingDeadline)
            assert d.filing_type
            assert d.due_date
            assert d.status in ["upcoming", "due_soon", "overdue"]
    
    @pytest.mark.asyncio
    async def test_filing_calendar_has_13f(self, kyc_service: KYCService) -> None:
        """Test that 13F filing is in calendar."""
        deadlines = await kyc_service.get_filing_calendar()
        
        filing_types = [d.filing_type for d in deadlines]
        assert "Form 13F" in filing_types
    
    @pytest.mark.asyncio
    async def test_generate_13f_xml(self, kyc_service: KYCService) -> None:
        """Test 13F XML generation."""
        xml = await kyc_service.generate_13f_xml("portfolio-1")
        
        assert isinstance(xml, bytes)
        xml_str = xml.decode('utf-8')
        
        # Verify XML structure
        assert '<?xml version="1.0" encoding="UTF-8"?>' in xml_str
        assert '<informationTable' in xml_str
        assert '</informationTable>' in xml_str
        assert '<infoTable>' in xml_str
    
    @pytest.mark.asyncio
    async def test_13f_xml_contains_holdings(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test 13F XML contains expected holdings."""
        xml = await kyc_service.generate_13f_xml("portfolio-1")
        xml_str = xml.decode('utf-8')
        
        # Should contain major holdings
        assert "Apple Inc" in xml_str
        assert "Microsoft Corp" in xml_str
        assert "<cusip>" in xml_str
        assert "<value>" in xml_str
    
    @pytest.mark.asyncio
    async def test_13f_xml_voting_authority(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test 13F XML contains voting authority."""
        xml = await kyc_service.generate_13f_xml("portfolio-1")
        xml_str = xml.decode('utf-8')
        
        assert "<votingAuthority>" in xml_str
        assert "<Sole>" in xml_str


class TestKYCServiceHelpers:
    """Tests for helper methods."""
    
    def test_get_required_documents_basic(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test basic required documents list."""
        docs = kyc_service.get_required_documents("basic")
        
        assert len(docs) >= 2
        types = [d["type"] for d in docs]
        assert "passport" in types
        assert "utility_bill" in types
    
    def test_get_required_documents_accredited(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test accredited investor required documents."""
        docs = kyc_service.get_required_documents("accredited")
        
        types = [d["type"] for d in docs]
        assert "accredited_investor" in types
        assert "tax_return" in types


class TestKYCServiceCaching:
    """Tests for verification caching."""
    
    @pytest.mark.asyncio
    async def test_verification_cached(
        self,
        kyc_service: KYCService,
        sample_documents: list[Document]
    ) -> None:
        """Test verification result is cached."""
        await kyc_service.verify_identity("user-cache", sample_documents)
        
        cached = await kyc_service.get_verification_status("user-cache")
        
        assert cached is not None
        assert cached.user_id == "user-cache"
    
    @pytest.mark.asyncio
    async def test_verification_not_cached_for_unknown(
        self,
        kyc_service: KYCService
    ) -> None:
        """Test no cached result for unknown user."""
        cached = await kyc_service.get_verification_status("unknown-user")
        
        assert cached is None
