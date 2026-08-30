"""
Lexer Configuration Module for Tiny C / C++ Subset Compiler.

Defines global constants, token maps, keywords, security functions,
and lexer operational settings.
"""

from typing import Dict, Set

# Reserved Keywords Definition (Standard C / C++ Subset)
KEYWORDS: Dict[str, str] = {
    "int": "INT",
    "float": "FLOAT",
    "char": "CHAR",
    "string": "STRING",
    "bool": "BOOL",
    "void": "VOID",
    "const": "CONST",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    "print": "PRINT",
    "true": "TRUE",
    "false": "FALSE",
    "main": "MAIN",
    "printf": "PRINTF",
    "scanf": "SCANF",
    "cout": "COUT",
    "cin": "CIN",
}

# Built-in Security Functions Definition
SECURITY_FUNCTIONS: Dict[str, str] = {
    "db_query": "SEC_DB_QUERY",
    "system": "SEC_SYSTEM",
    "gets": "SEC_GETS",
    "strcpy": "SEC_STRCPY",
    "sprintf": "SEC_SPRINTF",
    "strcat": "SEC_STRCAT",
    "rand": "SEC_RAND",
    "secure_rand": "SEC_SECURE_RAND",
    "open": "SEC_OPEN",
    "read": "SEC_READ",
    "write": "SEC_WRITE",
    "close": "SEC_CLOSE",
}

# Operator and Delimiter Token Names
OPERATOR_TOKENS: Dict[str, str] = {
    "+=": "PLUS_ASSIGN",
    "-=": "MINUS_ASSIGN",
    "*=": "TIMES_ASSIGN",
    "/=": "DIV_ASSIGN",
    "==": "EQ",
    "!=": "NE",
    "<=": "LE",
    ">=": "GE",
    "&&": "AND",
    "||": "OR",
    "++": "INC",
    "--": "DEC",
    "<<": "LSHIFT",
    ">>": "RSHIFT",
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIVIDE",
    "%": "MODULO",
    "=": "ASSIGN",
    "<": "LT",
    ">": "GT",
    "!": "NOT",
}

DELIMITER_TOKENS: Dict[str, str] = {
    ";": "SEMI",
    ",": "COMMA",
    ".": "DOT",
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    "[": "LBRACK",
    "]": "RBRACK",
}

# Escape Sequence Mapping for Strings and Chars
ESCAPE_SEQUENCES: Dict[str, str] = {
    r"\n": "\n",
    r"\t": "\t",
    r"\r": "\r",
    r"\\": "\\",
    r"\'": "'",
    r'\"': '"',
    r"\0": "\0",
}
