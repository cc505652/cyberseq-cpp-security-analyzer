"""
Visitor Pattern Infrastructure for Tiny C Abstract Syntax Tree.

Defines the core abstract ASTVisitor interface and concrete traversal visitors
enabling decoupled inspection, static security analysis, and AI prompt building.
"""

from abc import ABC, abstractmethod
from typing import Any
from compiler.ast_nodes import (
    ASTNode,
    ProgramNode,
    BlockNode,
    VariableDeclarationNode,
    ConstantDeclarationNode,
    AssignmentNode,
    IdentifierNode,
    LiteralNode,
    BinaryExpressionNode,
    UnaryExpressionNode,
    IfStatementNode,
    WhileStatementNode,
    ForStatementNode,
    BreakNode,
    ContinueNode,
    ReturnNode,
    PrintNode,
    FunctionCallNode,
    ExpressionStatementNode,
    EmptyStatementNode,
    ErrorNode,
)


class ASTVisitor(ABC):
    """Abstract Interface defining visit methods for all concrete AST node types."""

    @abstractmethod
    def visit_program(self, node: ProgramNode) -> Any:
        pass

    @abstractmethod
    def visit_block(self, node: BlockNode) -> Any:
        pass

    @abstractmethod
    def visit_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        pass

    @abstractmethod
    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> Any:
        pass

    @abstractmethod
    def visit_assignment(self, node: AssignmentNode) -> Any:
        pass

    @abstractmethod
    def visit_expression_statement(self, node: ExpressionStatementNode) -> Any:
        pass

    @abstractmethod
    def visit_empty_statement(self, node: EmptyStatementNode) -> Any:
        pass

    @abstractmethod
    def visit_if_statement(self, node: IfStatementNode) -> Any:
        pass

    @abstractmethod
    def visit_while_statement(self, node: WhileStatementNode) -> Any:
        pass

    @abstractmethod
    def visit_for_statement(self, node: ForStatementNode) -> Any:
        pass

    @abstractmethod
    def visit_break(self, node: BreakNode) -> Any:
        pass

    @abstractmethod
    def visit_continue(self, node: ContinueNode) -> Any:
        pass

    @abstractmethod
    def visit_return(self, node: ReturnNode) -> Any:
        pass

    @abstractmethod
    def visit_print(self, node: PrintNode) -> Any:
        pass

    @abstractmethod
    def visit_function_call(self, node: FunctionCallNode) -> Any:
        pass

    @abstractmethod
    def visit_identifier(self, node: IdentifierNode) -> Any:
        pass

    @abstractmethod
    def visit_literal(self, node: LiteralNode) -> Any:
        pass

    @abstractmethod
    def visit_binary_expression(self, node: BinaryExpressionNode) -> Any:
        pass

    @abstractmethod
    def visit_unary_expression(self, node: UnaryExpressionNode) -> Any:
        pass

    @abstractmethod
    def visit_error(self, node: ErrorNode) -> Any:
        pass


class ASTTraversalVisitor(ASTVisitor):
    """Base Traversal Visitor that recursively visits every child node in the tree."""

    def visit_program(self, node: ProgramNode) -> Any:
        for stmt in node.statements:
            stmt.accept(self)

    def visit_block(self, node: BlockNode) -> Any:
        for stmt in node.statements:
            stmt.accept(self)

    def visit_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        if node.initializer:
            node.initializer.accept(self)

    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> Any:
        node.initializer.accept(self)

    def visit_assignment(self, node: AssignmentNode) -> Any:
        node.target.accept(self)
        node.value.accept(self)

    def visit_expression_statement(self, node: ExpressionStatementNode) -> Any:
        node.expression.accept(self)

    def visit_empty_statement(self, node: EmptyStatementNode) -> Any:
        pass

    def visit_if_statement(self, node: IfStatementNode) -> Any:
        node.condition.accept(self)
        node.then_branch.accept(self)
        if node.else_branch:
            node.else_branch.accept(self)

    def visit_while_statement(self, node: WhileStatementNode) -> Any:
        node.condition.accept(self)
        node.body.accept(self)

    def visit_for_statement(self, node: ForStatementNode) -> Any:
        if node.init:
            node.init.accept(self)
        if node.condition:
            node.condition.accept(self)
        if node.update:
            node.update.accept(self)
        node.body.accept(self)

    def visit_break(self, node: BreakNode) -> Any:
        pass

    def visit_continue(self, node: ContinueNode) -> Any:
        pass

    def visit_return(self, node: ReturnNode) -> Any:
        if node.value:
            node.value.accept(self)

    def visit_print(self, node: PrintNode) -> Any:
        node.expression.accept(self)

    def visit_function_call(self, node: FunctionCallNode) -> Any:
        for arg in node.arguments:
            arg.accept(self)

    def visit_identifier(self, node: IdentifierNode) -> Any:
        pass

    def visit_literal(self, node: LiteralNode) -> Any:
        pass

    def visit_binary_expression(self, node: BinaryExpressionNode) -> Any:
        node.left.accept(self)
        node.right.accept(self)

    def visit_unary_expression(self, node: UnaryExpressionNode) -> Any:
        node.operand.accept(self)

    def visit_error(self, node: ErrorNode) -> Any:
        pass
