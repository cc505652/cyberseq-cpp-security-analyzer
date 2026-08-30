"""
Prompt Templates & Builder for Tiny C AI Security Explanation Engine.

Formats structured SecurityFinding data into student-friendly prompt instructions
demanding educational, beginner-accessible remediation reports.
"""

from typing import Any, Dict
from security.finding import SecurityFinding


class PromptBuilder:
    """Constructs tailored educational prompts for LLM explanation passes."""

    EXPLANATION_SYSTEM_PROMPT = (
        "You are an expert Cybersecurity Educator helping a Computer Science student understand software security.\n"
        "Explain the provided static analysis security finding clearly, concisely, and educationally.\n"
        "Follow the required output format strictly. Do not invent unlisted vulnerabilities."
    )

    @staticmethod
    def build_explanation_prompt(finding: SecurityFinding) -> str:
        """Constructs prompt for explaining a single SecurityFinding."""
        return (
            f"Vulnerability Finding to Explain:\n"
            f"- Rule ID: {finding.rule_id}\n"
            f"- Name: {finding.vulnerability_name}\n"
            f"- Severity: {finding.severity}\n"
            f"- Line Number: {finding.line}\n"
            f"- Vulnerable Code Snippet: {finding.code_snippet}\n"
            f"- Initial Static Analyzer Note: {finding.description}\n"
            f"- Initial Static Recommendation: {finding.recommendation}\n\n"
            f"Please respond with the following 10 structured sections:\n"
            f"1. Vulnerability Name\n"
            f"2. Simple Explanation (Beginner friendly)\n"
            f"3. Technical Explanation\n"
            f"4. Why it is Dangerous\n"
            f"5. Possible Attack Scenario\n"
            f"6. Severity Rating & Impact\n"
            f"7. Secure Coding Recommendation\n"
            f"8. Corrected Code Example\n"
            f"9. Security Best Practices\n"
            f"10. Standard References (OWASP / CWE if applicable)\n"
        )
