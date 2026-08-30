"""
Scope Stack & Hierarchy Manager for C/C++ Subset Compiler.

Manages scope push/pop operations, active scope tracking, and automatic
pre-registration of built-in security function symbols into global scope.
"""

from typing import Dict, List, Optional
from compiler.symbols import Symbol, BuiltinFunctionSymbol
from compiler.scope import Scope, ScopeType


class ScopeManager:
    """Manages active scope stack, global scope root, and scope transitions."""

    def __init__(self) -> None:
        self.global_scope: Scope = Scope(name="global", scope_type=ScopeType.GLOBAL, scope_level=0)
        self.current_scope: Scope = self.global_scope
        self._scope_stack: List[Scope] = [self.global_scope]
        self._all_scopes: List[Scope] = [self.global_scope]
        self._scope_counter: int = 0
        self._register_builtins()

    def _register_builtins(self) -> None:
        """Registers built-in C/C++ I/O functions and security primitives into global scope."""
        builtins = [
            BuiltinFunctionSymbol(name="print", return_type="void", param_types=["any"]),
            BuiltinFunctionSymbol(name="printf", return_type="int", param_types=["string"]),
            BuiltinFunctionSymbol(name="scanf", return_type="int", param_types=["string"]),
            BuiltinFunctionSymbol(name="db_query", return_type="int", param_types=["string"]),
            BuiltinFunctionSymbol(name="system", return_type="int", param_types=["string"]),
            BuiltinFunctionSymbol(name="gets", return_type="string", param_types=["string"]),
            BuiltinFunctionSymbol(name="strcpy", return_type="string", param_types=["string", "string"]),
            BuiltinFunctionSymbol(name="sprintf", return_type="int", param_types=["string", "string"]),
            BuiltinFunctionSymbol(name="strcat", return_type="string", param_types=["string", "string"]),
            BuiltinFunctionSymbol(name="rand", return_type="int", param_types=[]),
            BuiltinFunctionSymbol(name="secure_rand", return_type="int", param_types=[]),
            BuiltinFunctionSymbol(name="open", return_type="int", param_types=["string", "int"]),
            BuiltinFunctionSymbol(name="read", return_type="int", param_types=["int", "string", "int"]),
            BuiltinFunctionSymbol(name="write", return_type="int", param_types=["int", "string", "int"]),
            BuiltinFunctionSymbol(name="close", return_type="int", param_types=["int"]),
        ]
        for builtin in builtins:
            self.global_scope.define(builtin)

    def enter_scope(self, name: str, scope_type: ScopeType) -> Scope:
        """Creates a new child scope, pushes it onto stack, and updates current_scope."""
        self._scope_counter += 1
        scope_name = f"{name}_{self._scope_counter}"
        new_scope = Scope(
            name=scope_name,
            scope_type=scope_type,
            scope_level=self.current_scope.scope_level + 1,
            parent=self.current_scope,
        )
        self._scope_stack.append(new_scope)
        self._all_scopes.append(new_scope)
        self.current_scope = new_scope
        return new_scope

    def exit_scope(self) -> Scope:
        """Pops current scope from stack and returns to parent scope."""
        if len(self._scope_stack) <= 1:
            raise RuntimeError("Cannot exit global scope.")
        exited = self._scope_stack.pop()
        self.current_scope = self._scope_stack[-1]
        return exited

    def define(self, symbol: Symbol) -> None:
        """Defines a symbol in the current active scope."""
        self.current_scope.define(symbol)

    def lookup(self, name: str) -> Optional[Symbol]:
        """Looks up symbol up the current scope hierarchy."""
        return self.current_scope.lookup(name)

    def lookup_current(self, name: str) -> Optional[Symbol]:
        """Looks up symbol strictly in current scope level."""
        return self.current_scope.lookup_current(name)

    @property
    def all_scopes(self) -> List[Scope]:
        """Returns list of all created scopes in creation order."""
        return list(self._all_scopes)
