"""
Lexical Analyzer Implementation for C/C++ Subset Compiler using PLY (Python Lex-Yacc).

Converts source code into a stream of structured TokenInfo objects,
handling comments, #include directives, std:: qualifiers, and error diagnostics.
"""

from typing import List, Optional, Tuple, Any
import ply.lex as lex

from compiler.config import KEYWORDS, SECURITY_FUNCTIONS, ESCAPE_SEQUENCES
from compiler.tokens import tokens, TokenInfo
from compiler.errors import LexerErrorManager, LexicalError


class TinyCLexer:
    """Production-grade Lexical Analyzer for C/C++ subset programming language."""

    tokens = tokens

    # Ignored characters (Whitespace except newlines)
    t_ignore = " \t"

    # --- OPERATORS (Compound before simple) ---
    t_PLUS_ASSIGN = r"\+="
    t_MINUS_ASSIGN = r"-="
    t_TIMES_ASSIGN = r"\*="
    t_DIV_ASSIGN = r"/="
    t_EQ = r"=="
    t_NE = r"!="
    t_LE = r"<="
    t_GE = r">="
    t_AND = r"&&"
    t_OR = r"\|\|"
    t_INC = r"\+\+"
    t_DEC = r"--"
    t_LSHIFT = r"<<"
    t_RSHIFT = r">>"

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_MODULO = r"%"
    t_ASSIGN = r"="
    t_LT = r"<"
    t_GT = r">"
    t_NOT = r"!"

    # --- DELIMITERS & BRACKETS ---
    t_SEMI = r";"
    t_COMMA = r","
    t_DOT = r"\."
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_LBRACK = r"\["
    t_RBRACK = r"\]"

    def __init__(self, error_manager: Optional[LexerErrorManager] = None) -> None:
        self.error_manager: LexerErrorManager = error_manager or LexerErrorManager()
        self.source_code: str = ""
        self.lexer: lex.Lexer = lex.lex(module=self)

    def compute_column(self, lexpos: int) -> int:
        """Computes 1-indexed column number from source code position."""
        last_newline = self.source_code.rfind("\n", 0, lexpos)
        if last_newline < 0:
            return lexpos + 1
        return lexpos - last_newline

    # --- NEWLINE TRACKING ---
    def t_newline(self, t: lex.LexToken) -> None:
        r"\n+"
        t.lexer.lineno += len(t.value)

    # --- PREPROCESSOR DIRECTIVES & STD NAMESPACE (IGNORED) ---
    def t_PREPROCESSOR(self, t: lex.LexToken) -> None:
        r"\#.*"
        t.lexer.lineno += t.value.count("\n")
        # Ignored, return nothing

    def t_STD_PREFIX(self, t: lex.LexToken) -> None:
        r"std::"
        # Ignored, return nothing

    def t_USING_NAMESPACE(self, t: lex.LexToken) -> None:
        r"using\s+namespace\s+std\s*;"
        # Ignored, return nothing

    # --- COMMENTS ---
    def t_MULTI_COMMENT(self, t: lex.LexToken) -> None:
        r"/\*(.|\n)*?\*/"
        t.lexer.lineno += t.value.count("\n")

    def t_SINGLE_COMMENT(self, t: lex.LexToken) -> None:
        r"//.*"

    def t_UNTERMINATED_MULTI_COMMENT(self, t: lex.LexToken) -> None:
        r"/\*(.|\n)*"
        col = self.compute_column(t.lexpos)
        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=t.value[:20] + "...",
            message="Unterminated multi-line comment starting here",
            error_type="UNTERMINATED_COMMENT_ERROR",
        )
        t.lexer.lineno += t.value.count("\n")

    # --- INVALID IDENTIFIER / BAD NUMBER PATTERNS ---
    def t_INVALID_IDENTIFIER(self, t: lex.LexToken) -> None:
        r"[0-9]+[a-zA-Z_][a-zA-Z0-9_]*"
        col = self.compute_column(t.lexpos)
        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=t.value,
            message="Invalid identifier: identifiers cannot start with digits",
            error_type="INVALID_IDENTIFIER_ERROR",
        )

    def t_INVALID_FLOAT_MULTIPLE_DOTS(self, t: lex.LexToken) -> None:
        r"[0-9]+\.[0-9]+\.[0-9.]+"
        col = self.compute_column(t.lexpos)
        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=t.value,
            message="Malformed floating point literal containing multiple decimal points",
            error_type="INVALID_NUMBER_ERROR",
        )

    # --- NUMERIC LITERALS ---
    def t_FLOAT_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
        r"[0-9]+\.[0-9]+"
        t.value = float(t.value)
        return t

    def t_INVALID_FLOAT_TRAILING_DOT(self, t: lex.LexToken) -> None:
        r"[0-9]+\."
        col = self.compute_column(t.lexpos)
        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=t.value,
            message="Malformed floating point literal with trailing dot",
            error_type="INVALID_NUMBER_ERROR",
        )

    def t_INT_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
        r"[0-9]+"
        t.value = int(t.value)
        return t

    # --- STRING LITERALS ---
    def t_STRING_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
        r'"([^"\\\n]|(\\.))*"'
        raw_str = t.value[1:-1]
        processed_str = raw_str
        for escape_seq, char_val in ESCAPE_SEQUENCES.items():
            processed_str = processed_str.replace(escape_seq, char_val)
        t.value = processed_str
        return t

    def t_UNTERMINATED_STRING(self, t: lex.LexToken) -> None:
        r'"([^"\\\n]|(\\.))*'
        col = self.compute_column(t.lexpos)
        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=t.value,
            message="Unterminated string literal",
            error_type="UNTERMINATED_STRING_ERROR",
        )

    # --- CHARACTER LITERALS ---
    def t_CHAR_LITERAL(self, t: lex.LexToken) -> lex.LexToken:
        r"'([^'\\\n]|(\\.))'"
        raw_char = t.value[1:-1]
        if raw_char in ESCAPE_SEQUENCES:
            t.value = ESCAPE_SEQUENCES[raw_char]
        else:
            t.value = raw_char
        return t

    def t_INVALID_CHAR_LITERAL(self, t: lex.LexToken) -> None:
        r"'[^'\n]*'?"
        col = self.compute_column(t.lexpos)
        val = t.value
        if val == "''":
            msg = "Empty character literal"
        elif not val.endswith("'"):
            msg = "Unterminated character literal"
        else:
            msg = f"Multi-character character literal '{val}'"

        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=val,
            message=msg,
            error_type="INVALID_CHAR_LITERAL_ERROR",
        )

    # --- IDENTIFIERS, KEYWORDS & SECURITY FUNCTIONS ---
    def t_ID(self, t: lex.LexToken) -> lex.LexToken:
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        if t.value in KEYWORDS:
            t.type = KEYWORDS[t.value]
            if t.value in ("true", "false"):
                t.value = True if t.value == "true" else False
        elif t.value in SECURITY_FUNCTIONS:
            t.type = SECURITY_FUNCTIONS[t.value]

        return t

    # --- FALLBACK ERROR HANDLER ---
    def t_error(self, t: lex.LexToken) -> None:
        col = self.compute_column(t.lexpos)
        self.error_manager.add_error(
            line=t.lexer.lineno,
            column=col,
            position=t.lexpos,
            invalid_token=t.value[0],
            message=f"Illegal character '{t.value[0]}'",
            error_type="ILLEGAL_CHARACTER_ERROR",
        )
        t.lexer.skip(1)

    # --- PUBLIC SCANNER API ---
    def tokenize(self, source_code: str) -> List[TokenInfo]:
        """Scans complete source code and returns list of TokenInfo objects."""
        self.source_code = source_code
        self.error_manager.clear()
        self.lexer.lineno = 1
        self.lexer.input(source_code)

        tokens_list: List[TokenInfo] = []

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            col = self.compute_column(tok.lexpos)
            tokens_list.append(
                TokenInfo(
                    type=tok.type,
                    value=tok.value,
                    line=tok.lineno,
                    column=col,
                    lexpos=tok.lexpos,
                )
            )

        return tokens_list
