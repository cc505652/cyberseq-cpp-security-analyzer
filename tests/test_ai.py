"""
Comprehensive Pytest Test Suite for C/C++ AI Explanation Subsystem.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from security.finding import SecurityFinding
from security.severity import Severity
from ai.prompts import PromptBuilder
from ai.providers import MockAIProvider
from ai.ai_helper import AIHelper


@pytest.fixture
def sample_finding() -> SecurityFinding:
    return SecurityFinding(
        rule_id="SEC006",
        vulnerability_name="Unsafe Function Call (gets)",
        description="gets() lacks bounds checking.",
        severity=Severity.HIGH,
        line=12,
        column=5,
        code_snippet="gets(buffer)",
        recommendation="Replace gets() with fgets().",
    )


def test_prompt_builder(sample_finding: SecurityFinding) -> None:
    prompt = PromptBuilder.build_explanation_prompt(sample_finding)
    assert "SEC006" in prompt
    assert "gets(buffer)" in prompt


def test_mock_provider_rule_specific_fallbacks() -> None:
    provider = MockAIProvider()
    rules = ["SEC001", "SEC002", "SEC003", "SEC004", "SEC005", "SEC006", "SEC007", "SEC008", "SEC009", "SEC010"]

    for rule_id in rules:
        finding = SecurityFinding(
            rule_id=rule_id,
            vulnerability_name=f"Rule {rule_id}",
            description="Test description",
            severity=Severity.HIGH,
            line=10,
            column=1,
            code_snippet="test()",
            recommendation="Test recommendation",
        )
        prompt = PromptBuilder.build_explanation_prompt(finding)
        res = provider.generate_explanation(PromptBuilder.EXPLANATION_SYSTEM_PROMPT, prompt, rule_id=rule_id)

        assert "[Offline Fallback Explanation]" in res
        assert "1. Vulnerability Name" in res
        assert "2. Simple Explanation" in res
        assert "3. Technical Explanation" in res
        assert "4. Why it is Dangerous" in res
        assert "5. Possible Attack Scenario" in res
        assert "6. Severity Rating" in res
        assert "7. Secure Coding Recommendation" in res
        assert "8. Corrected Code Example" in res
        assert "10. Standard References" in res


def test_ai_helper_offline_label(sample_finding: SecurityFinding) -> None:
    helper = AIHelper(provider=MockAIProvider())
    explanation = helper.explain_finding(sample_finding)
    assert "[Offline Fallback Explanation]" in explanation


if __name__ == "__main__":
    pytest.main([__file__])
