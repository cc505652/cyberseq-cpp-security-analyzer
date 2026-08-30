"""
Symbol Table Subsystem Facade & Visualization Engine.

Provides unified interface for managing scope operations, symbol retrieval,
ASCII table formatting, Markdown export, and JSON representation.
"""

import json
from typing import Any, Dict, List, Optional
from compiler.symbols import Symbol, VariableSymbol, ConstantSymbol, FunctionSymbol, BuiltinFunctionSymbol
from compiler.scope import Scope, ScopeType
from compiler.scope_manager import ScopeManager


class SymbolTable:
    """Facade wrapping ScopeManager and formatting symbol diagnostic output."""

    def __init__(self) -> None:
        self.scope_manager: ScopeManager = ScopeManager()

    def enter_scope(self, name: str = "block", scope_type: ScopeType = ScopeType.BLOCK) -> Scope:
        return self.scope_manager.enter_scope(name, scope_type)

    def exit_scope(self) -> Scope:
        return self.scope_manager.exit_scope()

    def define(self, symbol: Symbol) -> None:
        self.scope_manager.define(symbol)

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.scope_manager.lookup(name)

    def lookup_current(self, name: str) -> Optional[Symbol]:
        return self.scope_manager.lookup_current(name)

    @property
    def current_scope(self) -> Scope:
        return self.scope_manager.current_scope

    @property
    def global_scope(self) -> Scope:
        return self.scope_manager.global_scope

    def count_symbols(self) -> int:
        """Returns total count of symbols across all created scopes."""
        return sum(len(scope.symbols) for scope in self.scope_manager.all_scopes)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes symbol table scopes into JSON-compatible dictionary."""
        scopes_data = []
        for scope in self.scope_manager.all_scopes:
            symbols_list = []
            for name, sym in scope.symbols.items():
                symbols_list.append({
                    "name": sym.name,
                    "kind": sym.__class__.__name__,
                    "type": sym.type_name,
                    "line": sym.line,
                    "column": sym.column,
                    "mutable": sym.is_mutable,
                    "attributes": sym.attributes,
                })
            scopes_data.append({
                "scope_name": scope.name,
                "scope_type": scope.scope_type.name,
                "scope_level": scope.scope_level,
                "parent_scope": scope.parent.name if scope.parent else None,
                "symbol_count": len(symbols_list),
                "symbols": symbols_list,
            })
        return {"total_scopes": len(scopes_data), "scopes": scopes_data}

    def to_json(self, indent: int = 2) -> str:
        """Exports symbol table as JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        """Exports symbol table as Markdown formatted tables."""
        lines = ["# Symbol Table Export", ""]
        for scope in self.scope_manager.all_scopes:
            lines.append(f"## Scope: `{scope.name}` (Level {scope.scope_level}, Kind: {scope.scope_type.name})")
            lines.append("| Symbol Name | Kind | Type | Line:Col | Mutability | Attributes |")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for sym in scope.symbols.values():
                attr_str = ", ".join(f"{k}={v}" for k, v in sym.attributes.items()) or "None"
                lines.append(
                    f"| `{sym.name}` | `{sym.__class__.__name__}` | `{sym.type_name}` | {sym.line}:{sym.column} | {'Yes' if sym.is_mutable else 'No'} | {attr_str} |"
                )
            lines.append("")
        return "\n".join(lines)

    def format_ascii(self) -> str:
        """Renders formatted multiline ASCII table of all scopes and symbols."""
        lines = ["=== TINY C SYMBOL TABLE ==="]
        for scope in self.scope_manager.all_scopes:
            lines.append(f"\nSCOPE [{scope.name}] (Level {scope.scope_level}, Type: {scope.scope_type.name})")
            lines.append("-" * 70)
            lines.append(f"{'NAME':<15} {'KIND':<22} {'TYPE':<10} {'POS':<10} {'MUTABLE':<8}")
            lines.append("-" * 70)
            for sym in scope.symbols.values():
                pos = f"{sym.line}:{sym.column}"
                lines.append(
                    f"{sym.name:<15} {sym.__class__.__name__:<22} {sym.type_name:<10} {pos:<10} {str(sym.is_mutable):<8}"
                )
        return "\n".join(lines)
