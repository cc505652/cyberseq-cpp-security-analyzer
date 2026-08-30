"""
Scope Representation Module for Tiny C Symbol Table.

Defines ScopeType enumeration and Scope class forming the hierarchical scope tree
with parent-child linkages and symbol resolution lookup logic.
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Any
from compiler.symbols import Symbol


class ScopeType(Enum):
    """Enumeration of supported lexical scope kinds."""
    GLOBAL = auto()
    FUNCTION = auto()
    BLOCK = auto()
    LOOP = auto()
    CONDITIONAL = auto()
    ANONYMOUS = auto()


class Scope:
    """Represents a single lexical scope node in the scope hierarchy."""

    def __init__(
        self,
        name: str,
        scope_type: ScopeType,
        scope_level: int = 0,
        parent: Optional["Scope"] = None,
    ) -> None:
        self.name: str = name
        self.scope_type: ScopeType = scope_type
        self.scope_level: int = scope_level
        self.parent: Optional["Scope"] = parent
        self.children: List["Scope"] = []
        self._symbols: Dict[str, Symbol] = {}

        if parent:
            parent.children.append(self)

    def define(self, symbol: Symbol) -> None:
        """Inserts a symbol into the current scope level."""
        symbol.scope_level = self.scope_level
        self._symbols[symbol.name] = symbol

    def lookup_current(self, name: str) -> Optional[Symbol]:
        """Looks up a symbol strictly in the local scope."""
        return self._symbols.get(name)

    def lookup(self, name: str) -> Optional[Symbol]:
        """Recursively looks up a symbol up the parent scope chain."""
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol
        if self.parent is not None:
            return self.parent.lookup(name)
        return None

    @property
    def symbols(self) -> Dict[str, Symbol]:
        """Returns read-only view of symbols registered in this scope."""
        return dict(self._symbols)

    def __repr__(self) -> str:
        return f"Scope(name='{self.name}', type={self.scope_type.name}, level={self.scope_level}, symbols={len(self._symbols)})"
