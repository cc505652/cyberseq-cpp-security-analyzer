"""
Comprehensive Pytest Test Suite for Tiny C Lexer.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.lexer import TinyCLexer


@pytest.fixture
def lexer() -> TinyCLexer:
    """Fixture initializing a fresh TinyCLexer instance."""
    return TinyCLexer()


def test_keywords(lexer: TinyCLexer) -> None:
    code = "int float char string bool void const if else while for break continue return print true false"
    tokens = lexer.tokenize(code)
    expected_types = [
        "INT", "FLOAT", "CHAR", "STRING", "BOOL", "VOID", "CONST",
        "IF", "ELSE", "WHILE", "FOR", "BREAK", "CONTINUE", "RETURN",
        "PRINT", "TRUE", "FALSE"
    ]
    assert [t.type for t in tokens] == expected_types
    assert tokens[-2].value is True
    assert tokens[-1].value is False
    assert not lexer.error_manager.has_errors()


def test_security_functions(lexer: TinyCLexer) -> None:
    code = "db_query system gets strcpy sprintf rand open close"
    tokens = lexer.tokenize(code)
    expected_types = ["SEC_DB_QUERY", "SEC_SYSTEM", "SEC_GETS", "SEC_STRCPY", "SEC_SPRINTF", "SEC_RAND", "SEC_OPEN", "SEC_CLOSE"]
    assert [t.type for t in tokens] == expected_types
    assert not lexer.error_manager.has_errors()


def test_operators(lexer: TinyCLexer) -> None:
    code = "+ - * / % == != < > <= >= && || ! = += -= *= /="
    tokens = lexer.tokenize(code)
    expected_types = [
        "PLUS", "MINUS", "TIMES", "DIVIDE", "MODULO",
        "EQ", "NE", "LT", "GT", "LE", "GE",
        "AND", "OR", "NOT", "ASSIGN",
        "PLUS_ASSIGN", "MINUS_ASSIGN", "TIMES_ASSIGN", "DIV_ASSIGN"
    ]
    assert [t.type for t in tokens] == expected_types
    assert not lexer.error_manager.has_errors()


def test_delimiters(lexer: TinyCLexer) -> None:
    code = "( ) { } [ ] ; ,"
    tokens = lexer.tokenize(code)
    expected_types = ["LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACK", "RBRACK", "SEMI", "COMMA"]
    assert [t.type for t in tokens] == expected_types
    assert not lexer.error_manager.has_errors()


def test_literals(lexer: TinyCLexer) -> None:
    code = '123 45.67 \'a\' "hello world"'
    tokens = lexer.tokenize(code)
    assert tokens[0].type == "INT_LITERAL" and tokens[0].value == 123
    assert tokens[1].type == "FLOAT_LITERAL" and tokens[1].value == 45.67
    assert tokens[2].type == "CHAR_LITERAL" and tokens[2].value == "a"
    assert tokens[3].type == "STRING_LITERAL" and tokens[3].value == "hello world"
    assert not lexer.error_manager.has_errors()


def test_identifiers(lexer: TinyCLexer) -> None:
    code = "x _var1 camelCase PascalCase CONST_VAR"
    tokens = lexer.tokenize(code)
    assert all(t.type == "ID" for t in tokens)
    assert [t.value for t in tokens] == ["x", "_var1", "camelCase", "PascalCase", "CONST_VAR"]
    assert not lexer.error_manager.has_errors()


def test_comments_and_whitespace(lexer: TinyCLexer) -> None:
    code = """
    // Single line comment
    int x = 10; /* Multi-line
                   comment */
    float y = 20.5;
    """
    tokens = lexer.tokenize(code)
    types = [t.type for t in tokens]
    assert types == ["INT", "ID", "ASSIGN", "INT_LITERAL", "SEMI", "FLOAT", "ID", "ASSIGN", "FLOAT_LITERAL", "SEMI"]
    assert not lexer.error_manager.has_errors()


def test_illegal_characters(lexer: TinyCLexer) -> None:
    code = "int x = 10; @ $ ~"
    tokens = lexer.tokenize(code)
    assert lexer.error_manager.has_errors()
    errors = lexer.error_manager.errors
    assert len(errors) == 3


def test_unterminated_string(lexer: TinyCLexer) -> None:
    code = 'string s = "hello;'
    tokens = lexer.tokenize(code)
    assert lexer.error_manager.has_errors()
    errors = lexer.error_manager.errors
    assert any("Unterminated string" in e.message for e in errors)


def test_line_and_column_tracking(lexer: TinyCLexer) -> None:
    code = "int x;\nfloat y;"
    tokens = lexer.tokenize(code)
    assert tokens[0].line == 1 and tokens[0].column == 1
    assert tokens[1].line == 1 and tokens[1].column == 5
    assert tokens[3].line == 2 and tokens[3].column == 1
    assert tokens[4].line == 2 and tokens[4].column == 7


def test_reset(lexer: TinyCLexer) -> None:
    code = "int x = @;"
    lexer.tokenize(code)
    assert lexer.error_manager.has_errors()
    lexer.error_manager.clear()
    assert not lexer.error_manager.has_errors()
    tokens = lexer.tokenize("float y = 1.0;")
    assert len(tokens) == 5


if __name__ == "__main__":
    pytest.main([__file__])
