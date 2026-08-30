"""
AI Helper Orchestrator Module for Tiny C Security Analyzer.

Receives SecurityFinding objects from static analysis pass, constructs prompts,
invokes configured LLM provider, and collects educational explanations.
"""

from typing import List, Dict, Any, Optional
from security.finding import SecurityFinding
from ai.prompts import PromptBuilder
from ai.providers import AIProvider, OpenAIProvider, OllamaProvider, MockAIProvider
import ai.config as config


class AIHelper:
    """Facade for processing SecurityFindings through configured AI Provider."""

    def __init__(self, provider: Optional[AIProvider] = None) -> None:
        self.provider: AIProvider = provider or self._get_default_provider()

    def _get_default_provider(self) -> AIProvider:
        provider_type = config.AI_PROVIDER.lower().strip()
        if provider_type == "openai":
            return OpenAIProvider()
        elif provider_type == "ollama":
            return OllamaProvider()
        elif provider_type == "mock":
            return MockAIProvider()
        else:
            # Default fallback
            return OllamaProvider()

    def explain_finding(self, finding: SecurityFinding) -> str:
        """Generates AI explanation for a single SecurityFinding."""
        system_prompt = PromptBuilder.EXPLANATION_SYSTEM_PROMPT
        user_prompt = PromptBuilder.build_explanation_prompt(finding)

        try:
            return self.provider.generate_explanation(system_prompt, user_prompt, rule_id=finding.rule_id)
        except Exception as err:
            return (
                f"[AI Explanation System Error]: Could not generate explanation for finding {finding.rule_id}.\n"
                f"Details: {str(err)}\n\n"
                f"Basic Finding Info:\n{str(finding)}"
            )

    def explain_all_findings(self, findings: List[SecurityFinding]) -> List[Dict[str, Any]]:
        """Generates AI explanations for a batch of SecurityFinding objects."""
        results = []
        for finding in findings:
            explanation_text = self.explain_finding(finding)
            results.append({
                "finding": finding.to_dict(),
                "ai_explanation": explanation_text,
            })
        return results
