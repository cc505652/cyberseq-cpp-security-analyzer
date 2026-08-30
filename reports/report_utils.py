"""
Report Utility Functions for PDF Report Generator.

Calculates overall security scores, grade ratings, and metadata formatting.
"""

from datetime import datetime
from typing import List, Dict, Any, Tuple
from security.severity import Severity


def calculate_security_score(findings: List[Any]) -> Tuple[int, str]:
    """
    Calculates security score starting at 100 points.
    Deductions:
      - Critical: -20
      - High: -10
      - Medium: -5
      - Low: -2
    Returns tuple of (Score, Rating String).
    """
    score = 100
    for f in findings:
        sev = getattr(f, "severity", None)
        sev_str = str(sev) if sev else ""

        if sev_str == "Critical":
            score -= 20
        elif sev_str == "High":
            score -= 10
        elif sev_str == "Medium":
            score -= 5
        elif sev_str == "Low":
            score -= 2

    score = max(0, score)

    if score >= 90:
        rating = "Excellent"
    elif score >= 75:
        rating = "Good"
    elif score >= 50:
        rating = "Needs Improvement"
    else:
        rating = "Poor"

    return score, rating


def get_current_timestamp() -> str:
    """Returns current formatted date and time string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
