import re
from typing import List

class Scrubber:
    """
    High-speed redaction engine for PII, secrets, and sensitive network data.
    Ensures that vector embeddings do not contain raw sensitive information.
    """

    PATTERNS = {
        "evm_private_key": r"\b(?:0x)?[a-fA-F0-9]{64}\b",
        "mnemonic_seed": r"\b(?:\w+\s+){11,23}\w+\b",
        "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "ipv6": r"\b(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}\b",
        "api_key": r"(?:AIza|sk-)[a-zA-Z0-9_-]{20,}",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    }

    def __init__(self, custom_patterns: dict = None):
        self.patterns = self.PATTERNS.copy()
        if custom_patterns:
            self.patterns.update(custom_patterns)
        
        self.compiled_regex = re.compile("|".join(f"(?P<{k}>{v})" for k, v in self.patterns.items()), re.IGNORECASE)

    def redact(self, text: str, replacement: str = "[REDACTED]") -> str:
        """
        Scans text and replaces all matched sensitive patterns with the replacement string.
        """
        if not text:
            return ""
        
        return self.compiled_regex.sub(replacement, text)

    def scrub_experience(self, content: str) -> str:
        """
        Specific wrapper for agent experiences.
        """
        return self.redact(content)

# Singleton instance for project-wide use
scrubber = Scrubber()
