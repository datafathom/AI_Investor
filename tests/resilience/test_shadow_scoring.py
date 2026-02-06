import pytest
import asyncio
from services.shadow_verifier import get_shadow_verifier

@pytest.mark.asyncio
async def test_shadow_agreement():
    verifier = get_shadow_verifier()
    
    # 1. Perfect Match (Mocking same lengths)
    score_perfect = verifier._calculate_agreement_score("ABC", "ABC")
    assert score_perfect == 1.0
    
    # 2. Partial Match (Mocking logic)
    # Lengths: 4 vs 5 -> 0.8
    score_partial = verifier._calculate_agreement_score("ABCD", "ABCDE")
    assert score_partial == 0.8
    
    # 3. No Match
    score_none = verifier._calculate_agreement_score("", "ABC")
    assert score_none == 0.0

@pytest.mark.asyncio
async def test_verify_decision_flow():
    verifier = get_shadow_verifier()
    
    # The mock returns "Simulated Shadow Response" (Length 25)
    # Let's provide a primary response of similar length to pass
    primary = "Simulated Shadow Response" 
    
    result = await verifier.verify_decision("Goal?", primary, {})
    
    assert result["status"] == "PASS"
    assert result["agreement_score"] >= 0.6
