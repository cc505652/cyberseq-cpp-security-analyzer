"""
Vulnerability Severity Level Definitions for Tiny C Static Security Analyzer.
"""

from enum import Enum


class Severity(Enum):
    """Enumeration of vulnerability severity levels."""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFO = "Info"

    def __str__(self) -> str:
        return self.value
