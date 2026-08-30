"""
Token Definitions Module for Tiny C / C++ Subset Compiler.

Contains the formal master tuple of token names required by PLY Lexer/Yacc,
along with structured token wrapper representations for downstream compiler passes.
"""

from dataclasses import dataclass
from typing import Any
from compiler.config import KEYWORDS, SECURITY_FUNCTIONS

# Base Tokens Definition for PLY
LITERAL_TOKENS = (
    "ID",
    "INT_LITERAL",
    "FLOAT_LITERAL",
    "CHAR_LITERAL",
    "STRING_LITERAL",
)

OPERATOR_TOKEN_NAMES = (
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULO",
    "ASSIGN",
    "PLUS_ASSIGN",
    "MINUS_ASSIGN",
    "TIMES_ASSIGN",
    "DIV_ASSIGN",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LE",
    "GE",
    "AND",
    "OR",
    "NOT",
    "INC",
    "DEC",
    "LSHIFT",
    "RSHIFT",
)

DELIMITER_TOKEN_NAMES = (
    "SEMI",
    "COMMA",
    "DOT",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACK",
    "RBRACK",
)

# Extract Keyword and Security Function token name values
KEYWORD_TOKEN_NAMES = tuple(sorted(set(KEYWORDS.values())))
SECURITY_FUNCTION_TOKEN_NAMES = tuple(sorted(set(SECURITY_FUNCTIONS.values())))

# Master Tokens Tuple required by PLY lexer
tokens = (
    LITERAL_TOKENS
    + OPERATOR_TOKEN_NAMES
    + DELIMITER_TOKEN_NAMES
    + KEYWORD_TOKEN_NAMES
    + SECURITY_FUNCTION_TOKEN_NAMES
)


@dataclass
class TokenInfo:
    """Structured representation of a scanned token for analysis & debugging."""
    type: str
    value: Any
    line: int
    column: int
    lexpos: int

    def __str__(self) -> str:
        return (
            f"Token(type='{self.type}', value={repr(self.value)}, "
            f"line={self.line}, col={self.column}, pos={self.lexpos})"
        )
