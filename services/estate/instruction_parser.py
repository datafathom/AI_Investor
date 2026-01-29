
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class InstructionParser:
    """
    Parses 'Pour-Over' instructions from a Will for Testamentary Trust funding.
    """
    
    def parse_instructions(self, raw_json: str) -> Dict[str, Any]:
        """
        Extracts funding rules and distribution ages.
        """
        try:
            data = json.loads(raw_json)
            logger.info(f"Parsing Will Instructions for Trust: {data.get('trust_name')}")
            return {
                "trust_name": data.get("trust_name"),
                "distribution_ages": data.get("distribution_ages"),
                "funding_source": "ESTATE_RESIDUE"
            }
        except Exception as e:
            logger.error(f"Failed to parse instructions: {e}")
            return {"error": "INVALID_FORMAT"}
