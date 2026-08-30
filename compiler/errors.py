"""
Lexical Error Handling Module for Tiny C Compiler.

Provides structured error representations and error collector mechanisms
for recording lexical analysis errors without halting the lexer prematurely.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LexicalError:
    """Represents a single lexical error detected during scanning."""
    line: int
    column: int
    position: int
    invalid_token: str
    message: str
    error_type: str = "SYNTAX_LEXICAL_ERROR"

    def __str__(self) -> str:
        return (
            f"[{self.error_type}] Line {self.line}, Column {self.column} "
            f"(pos {self.position}): {self.message} -> '{self.invalid_token}'"
        )


class LexerErrorManager:
    """Manages collection, formatting, and recovery of lexical errors."""

    def __init__(self) -> None:
        self._errors: List[LexicalError] = []

    def add_error(
        self,
        line: int,
        column: int,
        position: int,
        invalid_token: str,
        message: str,
        error_type: str = "LEXICAL_ERROR"
    ) -> LexicalError:
        """Constructs and registers a LexicalError instance."""
        err = LexicalError(
            line=line,
            column=column,
            position=position,
            invalid_token=invalid_token,
            message=message,
            error_type=error_type,
        )
        self._errors.append(err)
        return err

    @property
    def errors(self) -> List[LexicalError]:
        """Returns read-only copy of registered errors."""
        return list(self._errors)

    def has_errors(self) -> bool:
        """Checks if any lexical errors were logged."""
        return len(self._errors) > 0

    def clear(self) -> None:
        """Resets recorded errors list."""
        self._errors.clear()

    def format_errors(self) -> str:
        """Returns human-readable multiline error report."""
        if not self._errors:
            return "No lexical errors detected."
        return "\n".join(str(err) for err in self._errors)
