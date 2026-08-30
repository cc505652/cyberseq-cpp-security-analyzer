"""
AST Builder Helper & Parse Tree Converter for Tiny C Compiler.

Provides factory and transformation methods to simplify expressions, wrap tokens
into strongly-typed AST nodes, and eliminate superfluous concrete parse nodes.
"""

from typing import Any, List, Optional
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


class ASTBuilder:
    """Utility builder to construct and normalize AST nodes from parse tree elements."""

    @staticmethod
    def build_program(statements: List[ASTNode], line: int = 1, column: int = 1) -> ProgramNode:
        """Constructs a ProgramNode root from statement list."""
        flattened_stmts: List[ASTNode] = []
        for s in statements:
            if isinstance(s, list):
                flattened_stmts.extend(s)
            elif s is not None:
                flattened_stmts.append(s)
        return ProgramNode(statements=flattened_stmts, line=line, column=column)

    @staticmethod
    def build_literal(value: Any, literal_type: str, line: int = 0, column: int = 0) -> LiteralNode:
        """Factory for building typed LiteralNode instances."""
        return LiteralNode(value=value, literal_type=literal_type, line=line, column=column)

    @staticmethod
    def build_binary_expr(
        left: ASTNode, operator: str, right: ASTNode, line: int = 0, column: int = 0
    ) -> BinaryExpressionNode:
        """Constructs a simplified BinaryExpressionNode."""
        return BinaryExpressionNode(left=left, operator=operator, right=right, line=line, column=column)

    @staticmethod
    def build_unary_expr(
        operator: str, operand: ASTNode, prefix: bool = True, line: int = 0, column: int = 0
    ) -> UnaryExpressionNode:
        """Constructs a UnaryExpressionNode."""
        return UnaryExpressionNode(operator=operator, operand=operand, prefix=prefix, line=line, column=column)

    @staticmethod
    def build_function_call(
        func_name: str, args: Optional[List[ASTNode]] = None, line: int = 0, column: int = 0
    ) -> FunctionCallNode:
        """Factory for FunctionCallNode, normalizing argument lists."""
        return FunctionCallNode(func_name=func_name, arguments=args or [], line=line, column=column)
