from typing import Dict
from agents.base_agent import BaseAgent
from agents.lawyer.wash_sale_watchdog_agent import WashSaleWatchdogAgent
from agents.lawyer.document_notary_agent import DocumentNotaryAgent
from agents.lawyer.kyc_aml_compliance_agent import KycAmlComplianceAgent
from agents.lawyer.tax_loss_harvester_agent import TaxLossHarvesterAgent
from agents.lawyer.regulatory_news_ticker_agent import RegulatoryNewsTickerAgent
from agents.lawyer.audit_trail_reconstructor_agent import AuditTrailReconstructorAgent

def get_lawyer_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Lawyer department agents.
    """
    return {
        "lawyer.wash_sale_watchdog": WashSaleWatchdogAgent(),
        "lawyer.document_notary": DocumentNotaryAgent(),
        "lawyer.kyc_aml_compliance_agent": KycAmlComplianceAgentAgent(),
        "lawyer.tax_loss_harvester": TaxLossHarvesterAgent(),
        "lawyer.regulatory_news_ticker": RegulatoryNewsTickerAgent(),
        "lawyer.audit_trail_reconstructor": AuditTrailReconstructorAgent(),
    }
