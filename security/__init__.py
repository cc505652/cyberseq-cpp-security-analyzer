"""
Security package initialization for Tiny C static security analyzer.
"""

from security.severity import Severity
from security.finding import SecurityFinding
from security.security_rules import (
    SecurityRule,
    HardcodedPasswordRule,
    HardcodedAPIKeyRule,
    WeakPasswordRule,
    SQLInjectionRule,
    CommandInjectionRule,
    UnsafeGetsRule,
    UnsafeStrcpyRule,
    UnsafeSprintfRule,
    WeakRandomRule,
    ResourceLeakRule,
)
from security.security_analyzer import SecurityAnalyzer

__all__ = [
    "Severity",
    "SecurityFinding",
    "SecurityRule",
    "HardcodedPasswordRule",
    "HardcodedAPIKeyRule",
    "WeakPasswordRule",
    "SQLInjectionRule",
    "CommandInjectionRule",
    "UnsafeGetsRule",
    "UnsafeStrcpyRule",
    "UnsafeSprintfRule",
    "WeakRandomRule",
    "ResourceLeakRule",
    "SecurityAnalyzer",
]
