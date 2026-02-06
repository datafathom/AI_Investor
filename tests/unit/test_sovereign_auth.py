"""
Unit Tests for Sovereign Auth Service
Phase 1 Implementation: The Sovereign Kernel

Tests the WebAuthn challenge-response cycle and signature verification.
"""

import pytest
import time
from datetime import datetime, timedelta

from services.auth.sovereign_auth_service import (
    SovereignAuthService,
    SovereignChallenge,
    sovereign_auth_service,
)


class TestSovereignAuthService:
    """Tests for the Sovereign Identity layer."""

    def setup_method(self) -> None:
        """Reset singleton state between tests."""
        # Clear challenges for test isolation
        sovereign_auth_service._challenges.clear()
        sovereign_auth_service._credentials.clear()

    def test_singleton_pattern(self) -> None:
        """Verify singleton behavior per user rules."""
        service1 = SovereignAuthService()
        service2 = SovereignAuthService()
        assert service1 is service2

    def test_generate_challenge_returns_valid_structure(self) -> None:
        """Test challenge generation returns expected fields."""
        command = {"action": "BUY", "ticker": "AAPL", "quantity": 10}
        result = sovereign_auth_service.generate_challenge(command)

        assert "challenge_id" in result
        assert "challenge" in result
        assert "command_hash" in result
        assert "expires_in_seconds" in result
        assert len(result["challenge"]) == 64  # 32 bytes as hex

    def test_challenge_stored_after_generation(self) -> None:
        """Test that challenges are stored for later verification."""
        command = {"action": "SELL", "ticker": "MSFT"}
        result = sovereign_auth_service.generate_challenge(command)

        assert result["challenge_id"] in sovereign_auth_service._challenges

    def test_challenge_is_valid_initially(self) -> None:
        """Test that a new challenge is valid."""
        challenge = SovereignChallenge(
            challenge_id="test-123",
            challenge_bytes=b"test",
            command_hash="abc123",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(seconds=120),
        )
        assert challenge.is_valid() is True

    def test_challenge_expires(self) -> None:
        """Test that expired challenges are invalid."""
        challenge = SovereignChallenge(
            challenge_id="test-expired",
            challenge_bytes=b"test",
            command_hash="abc123",
            created_at=datetime.utcnow() - timedelta(seconds=200),
            expires_at=datetime.utcnow() - timedelta(seconds=80),
        )
        assert challenge.is_valid() is False

    def test_challenge_consumed_once(self) -> None:
        """Test that challenges can only be used once."""
        challenge = SovereignChallenge(
            challenge_id="test-single-use",
            challenge_bytes=b"test",
            command_hash="abc123",
            created_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(seconds=120),
            is_consumed=True,
        )
        assert challenge.is_valid() is False

    def test_verify_signature_rejects_missing_challenge(self) -> None:
        """Test that verification fails for unknown challenge IDs."""
        is_valid, message = sovereign_auth_service.verify_signature(
            challenge_id="nonexistent",
            signature=b"fake",
            authenticator_data=b"",
            client_data_json=b"",
            command_payload={},
        )
        assert is_valid is False
        assert "not found" in message.lower()

    def test_verify_signature_rejects_command_mismatch(self) -> None:
        """Test that verification fails if command payload differs."""
        original_command = {"action": "BUY", "ticker": "AAPL"}
        result = sovereign_auth_service.generate_challenge(original_command)

        # Attempt to verify with a different command
        tampered_command = {"action": "SELL", "ticker": "AAPL"}
        is_valid, message = sovereign_auth_service.verify_signature(
            challenge_id=result["challenge_id"],
            signature=b"fake-sig",
            authenticator_data=b"",
            client_data_json=b"",
            command_payload=tampered_command,
        )
        assert is_valid is False
        assert "does not match" in message.lower()

    def test_challenge_generation_performance(self) -> None:
        """Test that challenge generation meets <50ms target."""
        command = {"action": "TRANSFER", "amount": 10000}
        
        start = time.perf_counter()
        for _ in range(100):
            sovereign_auth_service.generate_challenge(command)
        elapsed_ms = (time.perf_counter() - start) * 1000 / 100

        assert elapsed_ms < 50, f"Challenge gen took {elapsed_ms:.2f}ms, target <50ms"

    def test_register_credential(self) -> None:
        """Test credential registration."""
        credential = sovereign_auth_service.register_credential(
            credential_id=b"cred-123",
            public_key=b"pubkey-abc",
            user_id="sovereign-ceo",
        )
        assert credential.user_id == "sovereign-ceo"
        assert sovereign_auth_service._credentials["sovereign-ceo"] is credential


class TestSovereignLedgerSchema:
    """Tests for the Pydantic ledger schemas."""

    def test_journal_entry_must_balance(self) -> None:
        """Test that unbalanced entries are rejected."""
        from schemas.sovereign_ledger import JournalEntry, JournalLine
        from decimal import Decimal

        with pytest.raises(ValueError, match="must balance"):
            JournalEntry(
                id="test-unbalanced",
                description="Unbalanced test",
                lines=[
                    JournalLine(account_id="cash", debit=Decimal("100.00")),
                    JournalLine(account_id="equity", credit=Decimal("50.00")),
                ],
            )

    def test_journal_entry_balanced_is_valid(self) -> None:
        """Test that balanced entries are accepted."""
        from schemas.sovereign_ledger import JournalEntry, JournalLine
        from decimal import Decimal

        entry = JournalEntry(
            id="test-balanced",
            description="Balanced test",
            lines=[
                JournalLine(account_id="cash", debit=Decimal("100.00")),
                JournalLine(account_id="equity", credit=Decimal("100.00")),
            ],
        )
        assert entry.id == "test-balanced"

    def test_journal_entry_hash_computation(self) -> None:
        """Test that hash computation is deterministic."""
        from schemas.sovereign_ledger import JournalEntry, JournalLine
        from decimal import Decimal

        entry = JournalEntry(
            id="test-hash",
            description="Hash test",
            lines=[
                JournalLine(account_id="asset", debit=Decimal("500.00")),
                JournalLine(account_id="liability", credit=Decimal("500.00")),
            ],
        )
        hash1 = entry.compute_hash()
        hash2 = entry.compute_hash()
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex
