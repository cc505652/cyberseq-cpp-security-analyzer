"""
Abstract Syntax Tree (AST) Node Hierarchy for Tiny C Compiler.

Defines the strongly-typed object-oriented AST node hierarchy deriving from
the common abstract base class ASTNode, supporting source position tracking
and the Visitor Pattern.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional


class ASTNode(ABC):
    """Abstract Base Class for all Abstract Syntax Tree nodes."""

    def __init__(self, line: int = 0, column: int = 0) -> None:
        self.line: int = line
        self.column: int = column

    @abstractmethod
    def accept(self, visitor: "ASTVisitor") -> Any:
        """Accepts an ASTVisitor to perform operations using the Visitor Pattern."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(line={self.line}, col={self.column})"


# Import forward reference for type hint
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from compiler.visitor import ASTVisitor


# --- ROOT & CONTAINER NODES ---

class ProgramNode(ASTNode):
    """Root node of a Tiny C program containing a list of top-level statements/declarations."""

    def __init__(self, statements: List[ASTNode], line: int = 1, column: int = 1) -> None:
        super().__init__(line, column)
        self.statements: List[ASTNode] = statements

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_program(self)


class BlockNode(ASTNode):
    """Encapsulates a block of statements enclosed in curly braces '{ ... }'."""

    def __init__(self, statements: List[ASTNode], line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)
        self.statements: List[ASTNode] = statements

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_block(self)


# --- DECLARATION NODES ---

class VariableDeclarationNode(ASTNode):
    """Represents a variable declaration (e.g., 'int count = 10;' or 'float arr[10];')."""

    def __init__(
        self,
        var_type: str,
        var_name: str,
        initializer: Optional[ASTNode] = None,
        array_size: Optional[int] = None,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.var_type: str = var_type
        self.var_name: str = var_name
        self.initializer: Optional[ASTNode] = initializer
        self.array_size: Optional[int] = array_size

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_variable_declaration(self)


class ConstantDeclarationNode(ASTNode):
    """Represents an immutable constant declaration (e.g., 'const int MAX = 100;')."""

    def __init__(
        self,
        const_type: str,
        const_name: str,
        initializer: ASTNode,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.const_type: str = const_type
        self.const_name: str = const_name
        self.initializer: ASTNode = initializer

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_constant_declaration(self)


# --- STATEMENT NODES ---

class AssignmentNode(ASTNode):
    """Represents an assignment expression/statement (e.g., 'x = 5;' or 'x += 1;')."""

    def __init__(
        self,
        target: ASTNode,
        value: ASTNode,
        operator: str = "=",
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.target: ASTNode = target
        self.value: ASTNode = value
        self.operator: str = operator

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_assignment(self)


class ExpressionStatementNode(ASTNode):
    """Wraps an expression used as a statement (e.g., function call or assignment semicolon)."""

    def __init__(self, expression: ASTNode, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)
        self.expression: ASTNode = expression

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_expression_statement(self)


class EmptyStatementNode(ASTNode):
    """Represents a standalone null semicolon statement ';`."""

    def __init__(self, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_empty_statement(self)


class IfStatementNode(ASTNode):
    """Represents an 'if (condition) then_branch else else_branch' control flow node."""

    def __init__(
        self,
        condition: ASTNode,
        then_branch: ASTNode,
        else_branch: Optional[ASTNode] = None,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.condition: ASTNode = condition
        self.then_branch: ASTNode = then_branch
        self.else_branch: Optional[ASTNode] = else_branch

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_if_statement(self)


class WhileStatementNode(ASTNode):
    """Represents a 'while (condition) body' loop construct."""

    def __init__(self, condition: ASTNode, body: ASTNode, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)
        self.condition: ASTNode = condition
        self.body: ASTNode = body

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_while_statement(self)


class ForStatementNode(ASTNode):
    """Represents a 'for (init; condition; update) body' loop construct."""

    def __init__(
        self,
        init: Optional[ASTNode],
        condition: Optional[ASTNode],
        update: Optional[ASTNode],
        body: ASTNode,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.init: Optional[ASTNode] = init
        self.condition: Optional[ASTNode] = condition
        self.update: Optional[ASTNode] = update
        self.body: ASTNode = body

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_for_statement(self)


class BreakNode(ASTNode):
    """Represents a 'break;' loop jump statement."""

    def __init__(self, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_break(self)


class ContinueNode(ASTNode):
    """Represents a 'continue;' loop jump statement."""

    def __init__(self, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_continue(self)


class ReturnNode(ASTNode):
    """Represents a 'return expression;' or 'return;' function exit statement."""

    def __init__(self, value: Optional[ASTNode] = None, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)
        self.value: Optional[ASTNode] = value

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_return(self)


class PrintNode(ASTNode):
    """Represents a built-in 'print(expression);' I/O statement."""

    def __init__(self, expression: ASTNode, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)
        self.expression: ASTNode = expression

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_print(self)


class FunctionCallNode(ASTNode):
    """Represents a generic function invocation (e.g., 'gets(buf)', 'db_query(q)', 'system(cmd)')."""

    def __init__(
        self,
        func_name: str,
        arguments: List[ASTNode],
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.func_name: str = func_name
        self.arguments: List[ASTNode] = arguments

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_function_call(self)


# --- EXPRESSION NODES ---

class IdentifierNode(ASTNode):
    """Represents a variable, parameter, or function identifier reference (e.g., 'counter')."""

    def __init__(self, name: str, line: int = 0, column: int = 0) -> None:
        super().__init__(line, column)
        self.name: str = name

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_identifier(self)


class LiteralNode(ASTNode):
    """Represents literal constant values (Integer, Float, Boolean, Character, String, Null)."""

    def __init__(
        self,
        value: Any,
        literal_type: str,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.value: Any = value
        self.literal_type: str = literal_type  # "int", "float", "bool", "char", "string", "null"

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_literal(self)


class BinaryExpressionNode(ASTNode):
    """Represents binary operator operations (e.g., 'a + b', 'x == y', 'p && q')."""

    def __init__(
        self,
        left: ASTNode,
        operator: str,
        right: ASTNode,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.left: ASTNode = left
        self.operator: str = operator
        self.right: ASTNode = right

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_binary_expression(self)


class UnaryExpressionNode(ASTNode):
    """Represents unary operator operations (e.g., '!flag', '-count', '++i')."""

    def __init__(
        self,
        operator: str,
        operand: ASTNode,
        prefix: bool = True,
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.operator: str = operator
        self.operand: ASTNode = operand
        self.prefix: bool = prefix

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_unary_expression(self)


# --- ERROR & RECOVERY NODES ---

class ErrorNode(ASTNode):
    """Represents a syntax/parse error placeholder node preserving context for recovery."""

    def __init__(
        self,
        error_message: str,
        offending_token: str = "",
        line: int = 0,
        column: int = 0,
    ) -> None:
        super().__init__(line, column)
        self.error_message: str = error_message
        self.offending_token: str = offending_token

    def accept(self, visitor: "ASTVisitor") -> Any:
        return visitor.visit_error(self)
