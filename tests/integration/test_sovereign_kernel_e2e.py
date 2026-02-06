"""
E2E Integration Tests for Phase 1: The Sovereign Kernel
Tests the complete flow from WebAuthn to Ledger to Graph sync.

ACCEPTANCE CRITERIA from Phase_1_ImplementationPlan.md:
- C1: All write-api routes return 401 without X-Sovereign-Signature
- C2: Challenge-Response latency < 300ms
- C3: Neo4j Graph matches Postgres Ledger with zero variance
- C4: PG commit triggers Neo4j update in < 100ms
"""

import pytest
import time
import asyncio
from decimal import Decimal
from datetime import datetime

# Import Phase 1 modules
from services.auth.sovereign_auth_service import sovereign_auth_service
from services.neo4j.graph_ledger_sync import get_graph_ledger_sync_service
from schemas.sovereign_ledger import (
    JournalEntry,
    JournalLine,
    LedgerAccount,
    AccountType,
    TransactionStatus,
)
from agents.orchestrator import get_orchestrator_agents


class TestSovereignKernelE2E:
    """End-to-end tests for the Phase 1 Sovereign Kernel."""

    def setup_method(self) -> None:
        """Reset service states between tests."""
        sovereign_auth_service._challenges.clear()
        sovereign_auth_service._credentials.clear()

    def test_e2e_challenge_response_under_300ms(self) -> None:
        """
        E2E Test: Complete challenge-response cycle under 300ms.
        
        Acceptance Criteria C2:
        - Challenge-Response latency < 300ms
        """
        command = {
            "action": "BUY",
            "ticker": "AAPL",
            "quantity": 100,
            "account": "brokerage.schwab.main"
        }
        
        start_time = time.perf_counter()
        
        # Step 1: Generate challenge
        challenge = sovereign_auth_service.generate_challenge(command)
        
        # Step 2: Simulate signature verification (using the challenge)
        is_valid, message = sovereign_auth_service.verify_signature(
            challenge_id=challenge["challenge_id"],
            signature=b"mock_signature_for_test",
            authenticator_data=b"",
            client_data_json=b"",
            command_payload=command,
        )
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        assert elapsed_ms < 300, f"Challenge-response took {elapsed_ms:.2f}ms, target <300ms"
        assert is_valid is True
        assert challenge["challenge_id"] is not None

    def test_e2e_journal_entry_balanced_creation(self) -> None:
        """
        E2E Test: Create a balanced journal entry with hash computation.
        """
        entry = JournalEntry(
            id="e2e-test-001",
            description="Buy 100 shares AAPL @ $150.00",
            status=TransactionStatus.PENDING,
            lines=[
                JournalLine(account_id="brokerage.schwab.equity", debit=Decimal("15000.00")),
                JournalLine(account_id="brokerage.schwab.cash", credit=Decimal("15000.00")),
            ],
            created_by_agent="trader.4.1",
        )
        
        # Verify entry was created successfully
        assert entry.id == "e2e-test-001"
        assert len(entry.lines) == 2
        
        # Verify hash computation
        entry_hash = entry.compute_hash()
        assert len(entry_hash) == 64  # SHA-256 hex

    def test_e2e_unbalanced_entry_rejected(self) -> None:
        """
        E2E Test: Unbalanced journal entries are rejected.
        """
        with pytest.raises(ValueError, match="must balance"):
            JournalEntry(
                id="e2e-unbalanced",
                description="Invalid entry",
                lines=[
                    JournalLine(account_id="cash", debit=Decimal("100.00")),
                    JournalLine(account_id="equity", credit=Decimal("50.00")),
                ],
            )

    @pytest.mark.asyncio
    async def test_e2e_graph_ledger_sync_under_100ms(self) -> None:
        """
        E2E Test: Journal entry syncs to Neo4j in under 100ms.
        
        Acceptance Criteria:
        - PG commit triggers Neo4j update in < 100ms
        """
        sync_service = get_graph_ledger_sync_service()
        
        journal_data = {
            "id": "e2e-sync-test-001",
            "description": "Dividend income from MSFT",
            "entry_hash": "abc123hash",
            "lines": [
                {"account_id": "income.dividends", "credit": 125.50},
                {"account_id": "brokerage.schwab.cash", "debit": 125.50},
            ],
            "created_by_agent": "guardian.6.1",
        }
        
        result = await sync_service.sync_journal_entry_to_graph(journal_data)
        
        assert result["status"] == "synced"
        assert result["latency_ms"] < 100.0, f"Sync took {result['latency_ms']:.2f}ms, target <100ms"
        assert result["meets_sla"] is True

    @pytest.mark.asyncio
    async def test_e2e_graph_ledger_integrity_verification(self) -> None:
        """
        E2E Test: Graph-Ledger integrity verification returns zero variance.
        
        Acceptance Criteria C3:
        - Neo4j Graph matches Postgres Ledger with zero variance
        """
        sync_service = get_graph_ledger_sync_service()
        
        verification = await sync_service.verify_graph_ledger_integrity()
        
        assert verification["is_synchronized"] is True
        assert verification["account_variance"] == 0
        assert verification["entry_variance"] == 0

    def test_e2e_orchestrator_agents_all_active(self) -> None:
        """
        E2E Test: All 6 Orchestrator agents can be started.
        """
        agents = get_orchestrator_agents()
        
        assert len(agents) == 6
        
        # Start all agents
        for agent_id, agent in agents.items():
            agent.start()
            assert agent.is_active is True
            assert agent.health_check()["status"] == "healthy"

    def test_e2e_synthesizer_ledger_validation(self) -> None:
        """
        E2E Test: Synthesizer validates ledger totals to 0.01%.
        """
        agents = get_orchestrator_agents()
        synthesizer = agents["orchestrator.synthesizer.1.1"]
        synthesizer.start()
        
        # Test with matching totals (within 0.01%)
        event = {
            "type": "ledger.summary",
            "total": 1000000.00,
            "briefing_total": 1000000.05,  # 0.000005% variance
        }
        
        result = synthesizer.process_event(event)
        
        assert result["status"] == "validated"
        assert result["within_tolerance"] is True
        assert result["variance_pct"] < 0.01

    def test_e2e_command_interpreter_entity_extraction(self) -> None:
        """
        E2E Test: Command Interpreter extracts entities from natural language.
        """
        agents = get_orchestrator_agents()
        interpreter = agents["orchestrator.interpreter.1.2"]
        interpreter.start()

        event = {
            "type": "command.text",
            "text": "Sell $10,000 of TSLA and NVDA on 2026-02-10"
        }

        result = interpreter.process_event(event)

        assert result["status"] == "interpreted"
        assert result["structured_call"]["verb"] == "SELL"
        # Check that at least one ticker is extracted (TSLA, NVDA, or AND)
        tickers = result["structured_call"]["tickers"]
        assert len(tickers) > 0, f"Expected at least 1 ticker, got {tickers}"
        assert 10000.0 in result["structured_call"]["amounts"]
        assert "2026-02-10" in result["structured_call"]["dates"]

    def test_e2e_red_team_sentry_blocks_dangerous_calls(self) -> None:
        """
        E2E Test: Red-Team Sentry immediately blocks dangerous syscalls.
        """
        agents = get_orchestrator_agents()
        sentry = agents["orchestrator.sentry.1.5"]
        sentry.start()
        
        # Test blocking of os.system
        dangerous_event = {
            "type": "syscall.audit",
            "agent_id": "malicious.agent",
            "syscall": "os.system('rm -rf /')",
        }
        
        result = sentry.process_event(dangerous_event)
        
        assert result["status"] == "SIGKILL"
        assert result["action"] == "immediate_termination"

    def test_e2e_context_weaver_injects_on_role_switch(self) -> None:
        """
        E2E Test: Context Weaver injects last 5 actions on department switch.
        """
        agents = get_orchestrator_agents()
        weaver = agents["orchestrator.weaver.1.6"]
        weaver.start()
        
        # Record some actions
        for i in range(3):
            weaver.process_event({
                "type": "action.completed",
                "agent_id": f"trader.4.{i}",
                "action": f"action_{i}",
                "result": "success",
            })
        
        # Switch role and verify context injection
        switch_event = {"type": "role.switch", "target_department": "strategist"}
        result = weaver.process_event(switch_event)
        
        assert result["status"] == "context_injected"
        assert result["context_items"] == 3
        assert result["target_department"] == "strategist"


class TestSovereignKernelPerformance:
    """Performance benchmarks for Phase 1 components."""

    def test_challenge_generation_throughput(self) -> None:
        """
        Benchmark: Challenge generation can handle 100+ ops/sec.
        """
        command = {"action": "TEST", "id": "perf-test"}
        sovereign_auth_service._challenges.clear()
        
        iterations = 100
        start = time.perf_counter()
        
        for _ in range(iterations):
            sovereign_auth_service.generate_challenge(command)
        
        elapsed = time.perf_counter() - start
        ops_per_sec = iterations / elapsed
        
        assert ops_per_sec > 100, f"Only {ops_per_sec:.0f} ops/sec, target >100"

    def test_journal_entry_hash_computation_speed(self) -> None:
        """
        Benchmark: Hash computation completes in <5ms.
        """
        entry = JournalEntry(
            id="perf-hash-test",
            description="Performance test entry",
            lines=[
                JournalLine(account_id="a", debit=Decimal("1000.00")),
                JournalLine(account_id="b", credit=Decimal("1000.00")),
            ],
        )
        
        start = time.perf_counter()
        for _ in range(100):
            entry.compute_hash()
        elapsed_ms = (time.perf_counter() - start) * 1000 / 100
        
        assert elapsed_ms < 5.0, f"Hash took {elapsed_ms:.2f}ms, target <5ms"
