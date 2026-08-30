"""
Pytest Unit Test Suite for Semantic Analyzer.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.parser import TinyCParser
from compiler.semantic import SemanticAnalyzer


@pytest.fixture
def parser() -> TinyCParser:
    return TinyCParser()


@pytest.fixture
def analyzer() -> SemanticAnalyzer:
    return SemanticAnalyzer()


def test_undeclared_variable(parser: TinyCParser, analyzer: SemanticAnalyzer) -> None:
    code = "x = 10;"
    ast_root = parser.parse(code)
    err_mgr = analyzer.analyze(ast_root)
    assert err_mgr.has_errors()
    assert any("not declared" in e.message.lower() for e in err_mgr.errors)


def test_type_mismatch_assignment(parser: TinyCParser, analyzer: SemanticAnalyzer) -> None:
    code = 'int x = "hello";'
    ast_root = parser.parse(code)
    err_mgr = analyzer.analyze(ast_root)
    assert err_mgr.has_errors()
    assert any("cannot initialize" in e.message.lower() or "cannot assign" in e.message.lower() for e in err_mgr.errors)


def test_constant_reassignment(parser: TinyCParser, analyzer: SemanticAnalyzer) -> None:
    code = "const int MAX = 100; MAX = 200;"
    ast_root = parser.parse(code)
    err_mgr = analyzer.analyze(ast_root)
    assert err_mgr.has_errors()
    assert any("cannot modify" in e.message.lower() or "constant" in e.message.lower() for e in err_mgr.errors)


def test_semantic_analysis_no_state_contamination(parser: TinyCParser, analyzer: SemanticAnalyzer) -> None:
    code = "int count = 10;"
    ast_root1 = parser.parse(code)
    err_mgr1 = analyzer.analyze(ast_root1)
    assert not err_mgr1.has_errors()

    # Second analysis run on the same analyzer instance must not cause duplicate declaration error
    ast_root2 = parser.parse(code)
    err_mgr2 = analyzer.analyze(ast_root2)
    assert not err_mgr2.has_errors()


if __name__ == "__main__":
    pytest.main([__file__])
