"""
Vendor API Audit Script - Phase 2.2
Catalogs all external vendor API dependencies and their status.
"""
import os
import re
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
OUTPUT_PATH = PROJECT_ROOT / "notes" / "Vendor_API_Needed.json"
ENV_PATH = PROJECT_ROOT / ".env"
ENV_TEMPLATE_PATH = PROJECT_ROOT / ".env.template"

# Known vendor SDK imports and their corresponding env vars
VENDOR_MAPPINGS = {
    "stripe": {
        "vendor_name": "Stripe",
        "purpose": "Payment Processing",
        "env_vars": ["STRIPE_API_KEY", "STRIPE_SECRET_KEY", "STRIPE_PUBLISHABLE_KEY"],
        "documentation_url": "https://stripe.com/docs/api",
        "cost_tier": "paid"
    },
    "plaid": {
        "vendor_name": "Plaid",
        "purpose": "Banking Integration",
        "env_vars": ["PLAID_CLIENT_ID", "PLAID_SECRET", "PLAID_ENV"],
        "documentation_url": "https://plaid.com/docs",
        "cost_tier": "paid"
    },
    "twilio": {
        "vendor_name": "Twilio",
        "purpose": "SMS/Voice Communications",
        "env_vars": ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN"],
        "documentation_url": "https://www.twilio.com/docs",
        "cost_tier": "paid"
    },
    "boto3": {
        "vendor_name": "AWS",
        "purpose": "Cloud Infrastructure (S3, etc)",
        "env_vars": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"],
        "documentation_url": "https://boto3.amazonaws.com/v1/documentation/api/latest/index.html",
        "cost_tier": "paid"
    },
    "sendgrid": {
        "vendor_name": "SendGrid",
        "purpose": "Email Delivery",
        "env_vars": ["SENDGRID_API_KEY"],
        "documentation_url": "https://docs.sendgrid.com",
        "cost_tier": "free"
    },
    "coinbase": {
        "vendor_name": "Coinbase",
        "purpose": "Cryptocurrency Trading",
        "env_vars": ["COINBASE_API_KEY", "COINBASE_API_SECRET"],
        "documentation_url": "https://docs.cloud.coinbase.com",
        "cost_tier": "free"
    },
    "discord": {
        "vendor_name": "Discord",
        "purpose": "Community Bot/Notifications",
        "env_vars": ["DISCORD_BOT_TOKEN", "DISCORD_WEBHOOK_URL"],
        "documentation_url": "https://discord.com/developers/docs",
        "cost_tier": "free"
    },
    "slack_sdk": {
        "vendor_name": "Slack",
        "purpose": "Team Notifications",
        "env_vars": ["SLACK_BOT_TOKEN", "SLACK_WEBHOOK_URL"],
        "documentation_url": "https://api.slack.com/docs",
        "cost_tier": "free"
    },
    "praw": {
        "vendor_name": "Reddit",
        "purpose": "Social Sentiment Analysis",
        "env_vars": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
        "documentation_url": "https://www.reddit.com/dev/api",
        "cost_tier": "free"
    },
    "googleapiclient": {
        "vendor_name": "Google APIs",
        "purpose": "YouTube, Gmail, etc",
        "env_vars": ["GOOGLE_API_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"],
        "documentation_url": "https://developers.google.com/apis-explorer",
        "cost_tier": "free"
    },
    "paypalrestsdk": {
        "vendor_name": "PayPal",
        "purpose": "Payment Processing",
        "env_vars": ["PAYPAL_CLIENT_ID", "PAYPAL_CLIENT_SECRET"],
        "documentation_url": "https://developer.paypal.com/docs",
        "cost_tier": "paid"
    },
    "square": {
        "vendor_name": "Square",
        "purpose": "Payment Processing",
        "env_vars": ["SQUARE_ACCESS_TOKEN", "SQUARE_APPLICATION_ID"],
        "documentation_url": "https://developer.squareup.com/docs",
        "cost_tier": "paid"
    },
    "openai": {
        "vendor_name": "OpenAI",
        "purpose": "AI/LLM Services",
        "env_vars": ["OPENAI_API_KEY"],
        "documentation_url": "https://platform.openai.com/docs",
        "cost_tier": "paid"
    },
    "anthropic": {
        "vendor_name": "Anthropic",
        "purpose": "AI/LLM Services",
        "env_vars": ["ANTHROPIC_API_KEY"],
        "documentation_url": "https://docs.anthropic.com",
        "cost_tier": "paid"
    }
}


class VendorAuditor:
    """Scans for vendor SDK usage and credential status."""
    
    def __init__(self) -> None:
        self.vendors: List[Dict[str, Any]] = []
        self.env_vars: Set[str] = set()
        self._load_env_vars()
    
    def _load_env_vars(self) -> None:
        """Load environment variable names from .env and .env.template."""
        for env_file in [ENV_PATH, ENV_TEMPLATE_PATH]:
            if env_file.exists():
                try:
                    content = env_file.read_text(encoding='utf-8')
                    for line in content.split('\n'):
                        if '=' in line and not line.startswith('#'):
                            var_name = line.split('=')[0].strip()
                            self.env_vars.add(var_name)
                except Exception as e:
                    logger.warning(f"Error reading {env_file}: {e}")
    
    def scan_all(self) -> Dict[str, Any]:
        """Scan services directory for vendor imports."""
        services_dir = PROJECT_ROOT / "services"
        
        if not services_dir.exists():
            logger.error("Services directory not found")
            return {"vendors": [], "summary": {}}
        
        detected_vendors: Dict[str, Dict] = {}
        
        for py_file in services_dir.rglob("*.py"):
            self._scan_file(py_file, detected_vendors)
        
        # Build final vendor list with status
        for sdk_name, info in detected_vendors.items():
            vendor_config = VENDOR_MAPPINGS.get(sdk_name, {
                "vendor_name": sdk_name.title(),
                "purpose": "Unknown",
                "env_vars": [],
                "documentation_url": "",
                "cost_tier": "unknown"
            })
            
            # Check credential status
            required_vars = vendor_config.get("env_vars", [])
            found_vars = [v for v in required_vars if v in self.env_vars]
            missing_vars = [v for v in required_vars if v not in self.env_vars]
            
            if len(missing_vars) == len(required_vars) and required_vars:
                status = "not_configured"
            elif missing_vars:
                status = "partially_configured"
            elif info.get("has_mock_patterns", False):
                status = "mocked"
            else:
                status = "implemented"
            
            self.vendors.append({
                "vendor_name": vendor_config["vendor_name"],
                "api_name": sdk_name,
                "purpose": vendor_config["purpose"],
                "current_status": status,
                "credentials_found": found_vars,
                "credentials_missing": missing_vars,
                "files_using": info.get("files", []),
                "documentation_url": vendor_config["documentation_url"],
                "cost_tier": vendor_config["cost_tier"]
            })
        
        # Summary stats
        summary = {
            "total_vendors": len(self.vendors),
            "implemented": len([v for v in self.vendors if v["current_status"] == "implemented"]),
            "mocked": len([v for v in self.vendors if v["current_status"] == "mocked"]),
            "not_configured": len([v for v in self.vendors if v["current_status"] == "not_configured"]),
            "partially_configured": len([v for v in self.vendors if v["current_status"] == "partially_configured"])
        }
        
        return {
            "summary": summary,
            "vendors": sorted(self.vendors, key=lambda x: x["vendor_name"])
        }
    
    def _scan_file(self, file_path: Path, detected: Dict) -> None:
        """Scan a file for vendor SDK imports."""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            relative_path = str(file_path.relative_to(PROJECT_ROOT))
            
            # Check for known SDK imports
            for sdk_name in VENDOR_MAPPINGS.keys():
                import_pattern = rf'(?:from|import)\s+{sdk_name}'
                if re.search(import_pattern, content, re.IGNORECASE):
                    if sdk_name not in detected:
                        detected[sdk_name] = {"files": [], "has_mock_patterns": False}
                    detected[sdk_name]["files"].append(relative_path)
                    
                    # Check if file has mock patterns
                    if any(kw in content.lower() for kw in ["mock", "dummy", "fake", "sandbox"]):
                        detected[sdk_name]["has_mock_patterns"] = True
                        
        except Exception as e:
            logger.warning(f"Error scanning {file_path}: {e}")


def run_vendor_audit(**kwargs) -> None:
    """CLI handler for running the vendor API audit."""
    print("Running Vendor API Audit...")
    
    auditor = VendorAuditor()
    results = auditor.scan_all()
    
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nVendor API Audit Complete!")
    print(f"  Total vendors detected: {results['summary']['total_vendors']}")
    print(f"  Implemented: {results['summary']['implemented']}")
    print(f"  Mocked: {results['summary']['mocked']}")
    print(f"  Not Configured: {results['summary']['not_configured']}")
    print(f"\nOutput saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_vendor_audit()
