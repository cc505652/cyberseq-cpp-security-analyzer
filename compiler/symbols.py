"""
Symbol Definitions Module for Tiny C Symbol Table.

Defines the object hierarchy representing program symbols (Variables, Constants,
Functions, Built-in Security Primitives, Parameters) with scope, position, and metadata tracking.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Symbol(ABC):
    """Base class for all symbol table entries."""

    name: str
    type_name: str = "void"
    scope_level: int = 0
    line: int = 0
    column: int = 0
    is_mutable: bool = True
    attributes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name='{self.name}', type='{self.type_name}', "
            f"scope_level={self.scope_level}, line={self.line}, col={self.column})"
        )


@dataclass
class VariableSymbol(Symbol):
    """Represents a mutable variable symbol."""

    array_size: Optional[int] = None

    def __post_init__(self) -> None:
        self.is_mutable = True
        if self.array_size is not None:
            self.attributes["array_size"] = self.array_size


@dataclass
class ConstantSymbol(Symbol):
    """Represents an immutable constant symbol."""

    value: Optional[Any] = None

    def __post_init__(self) -> None:
        self.is_mutable = False
        if self.value is not None:
            self.attributes["constant_value"] = self.value


@dataclass
class ParameterSymbol(Symbol):
    """Represents a function parameter symbol."""

    position: int = 0

    def __post_init__(self) -> None:
        self.is_mutable = True
        self.attributes["param_position"] = self.position


@dataclass
class FunctionSymbol(Symbol):
    """Represents a user-defined function symbol."""

    return_type: str = "void"
    parameters: List[ParameterSymbol] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.type_name = self.return_type
        self.is_mutable = False
        self.attributes["param_count"] = len(self.parameters)


@dataclass
class BuiltinFunctionSymbol(Symbol):
    """Represents a pre-defined built-in security function symbol."""

    return_type: str = "void"
    param_types: List[str] = field(default_factory=list)
    is_security_primitive: bool = True

    def __post_init__(self) -> None:
        self.type_name = self.return_type
        self.is_mutable = False
        self.attributes["is_security_primitive"] = self.is_security_primitive
        self.attributes["param_types"] = self.param_types


@dataclass
class TemporarySymbol(Symbol):
    """Represents an intermediate compiler temporary variable symbol."""

    temp_id: int = 0

    def __post_init__(self) -> None:
        self.is_mutable = True
        self.attributes["temp_id"] = self.temp_id
