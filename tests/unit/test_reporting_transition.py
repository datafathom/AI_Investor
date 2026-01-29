from services.reporting.epoch_summary import EpochSummaryGenerator

def test_epoch_summary_content():
    gen = EpochSummaryGenerator()
    summary = gen.generate_summary({})
    assert "EPOCH VI COMPLETION REPORT" in summary
    assert "Fiduciary RIA Framework" in summary

def test_transition_enrichment():
    from services.reporting.transition_reporter import TransitionReporter
    svc = TransitionReporter()
    res = svc.prepare_transition_data({"current_aum": 1000000})
    assert res["target_epoch"] == "VII"
    assert "SHARPE" in res["required_ratios"]
