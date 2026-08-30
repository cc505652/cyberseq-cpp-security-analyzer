"""
Semantic Error Handling Module for Tiny C Compiler.

Provides structured SemanticError representations and SemanticErrorManager collector
for recording semantic and type violations cleanly across AST traversal.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SemanticError:
    """Represents a single semantic or type check error."""
    message: str
    line: int = 0
    column: int = 0
    error_type: str = "SEMANTIC_ERROR"

    def __str__(self) -> str:
        pos = f"Line {self.line}" if self.line > 0 else "Global"
        if self.column > 0:
            pos += f", Column {self.column}"
        return f"[{self.error_type}] {pos}: {self.message}"


class SemanticErrorManager:
    """Collects and formats semantic analysis error diagnostics."""

    def __init__(self) -> None:
        self._errors: List[SemanticError] = []

    def add_error(self, message: str, line: int = 0, column: int = 0, error_type: str = "SEMANTIC_ERROR") -> SemanticError:
        """Constructs and registers a SemanticError diagnostic."""
        err = SemanticError(message=message, line=line, column=column, error_type=error_type)
        self._errors.append(err)
        return err

    @property
    def errors(self) -> List[SemanticError]:
        return list(self._errors)

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def clear(self) -> None:
        self._errors.clear()

    def format_errors(self) -> str:
        if not self._errors:
            return "No semantic errors detected."
        return "\n".join(str(err) for err in self._errors)
