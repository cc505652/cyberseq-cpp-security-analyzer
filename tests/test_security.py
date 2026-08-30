"""
Comprehensive Pytest Test Suite for C/C++ Static Security Analyzer.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.parser import TinyCParser
from compiler.semantic import SemanticAnalyzer
from security.security_analyzer import SecurityAnalyzer
from security.severity import Severity
from reports.report_utils import calculate_security_score


@pytest.fixture
def parser() -> TinyCParser:
    return TinyCParser()


@pytest.fixture
def semantic_analyzer() -> SemanticAnalyzer:
    return SemanticAnalyzer()


@pytest.fixture
def security_analyzer() -> SecurityAnalyzer:
    return SecurityAnalyzer()


def test_hardcoded_password_rule(parser: TinyCParser, security_analyzer: SecurityAnalyzer) -> None:
    code = 'string password = "admin123";'
    ast_root = parser.parse(code)
    findings = security_analyzer.analyze(ast_root)
    assert any(f.rule_id == "SEC001" for f in findings)


def test_command_injection_rule(parser: TinyCParser, security_analyzer: SecurityAnalyzer) -> None:
    code = 'string cmd = "rm -rf /"; system(cmd);'
    ast_root = parser.parse(code)
    findings = security_analyzer.analyze(ast_root)
    assert any(f.rule_id == "SEC005" and f.severity == Severity.CRITICAL for f in findings)


def test_unsafe_gets_rule(parser: TinyCParser, security_analyzer: SecurityAnalyzer) -> None:
    code = 'string buf = "temp"; gets(buf);'
    ast_root = parser.parse(code)
    findings = security_analyzer.analyze(ast_root)
    assert any(f.rule_id == "SEC006" for f in findings)


def test_line_number_preservation(parser: TinyCParser, security_analyzer: SecurityAnalyzer) -> None:
    code = """
    int main() {
        string password = "secret_password_123";
        string buf = "temp";
        gets(buf);
        return 0;
    }
    """
    ast_root = parser.parse(code)
    findings = security_analyzer.analyze(ast_root)
    assert len(findings) > 0
    for finding in findings:
        assert finding.line > 0, f"Finding {finding.rule_id} has invalid line number 0"


def test_comprehensive_vulnerable_cpp_acceptance(
    parser: TinyCParser,
    semantic_analyzer: SemanticAnalyzer,
    security_analyzer: SecurityAnalyzer,
) -> None:
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "comprehensive_vulnerable.cpp")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    ast_root = parser.parse(code)
    assert ast_root is not None

    semantic_errors = semantic_analyzer.analyze(ast_root)
    assert not semantic_errors.has_errors(), f"Semantic analysis failed with errors: {semantic_errors.errors}"

    findings = security_analyzer.analyze(ast_root)
    assert len(findings) > 0, "Comprehensive vulnerable program must produce > 0 security findings"
    rule_ids = {f.rule_id for f in findings}
    assert {"SEC001", "SEC002", "SEC006", "SEC007", "SEC008", "SEC009", "SEC010"}.issubset(rule_ids)


def test_safe_program_cpp_acceptance(
    parser: TinyCParser,
    semantic_analyzer: SemanticAnalyzer,
    security_analyzer: SecurityAnalyzer,
) -> None:
    path = os.path.join(os.path.dirname(__file__), "..", "examples", "safe_program.cpp")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    ast_root = parser.parse(code)
    assert ast_root is not None

    semantic_errors = semantic_analyzer.analyze(ast_root)
    assert not semantic_errors.has_errors(), f"Safe program produced semantic errors: {semantic_errors.errors}"

    findings = security_analyzer.analyze(ast_root)
    assert len(findings) == 0, f"Safe program produced unexpected security findings: {findings}"

    score, rating = calculate_security_score(findings)
    assert score == 100
    assert rating == "Excellent"


if __name__ == "__main__":
    pytest.main([__file__])
