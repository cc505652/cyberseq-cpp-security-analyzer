"""
Symbol Visitor Module for Tiny C Compiler.

Traverses Abstract Syntax Tree nodes to populate Symbol Table scopes with symbol
declarations without performing semantic validation or type error enforcement.
"""

from typing import Optional
from compiler.visitor import ASTTraversalVisitor
from compiler.symbol_table import SymbolTable
from compiler.symbols import (
    VariableSymbol,
    ConstantSymbol,
)
from compiler.scope import ScopeType
from compiler.ast_nodes import (
    ProgramNode,
    BlockNode,
    VariableDeclarationNode,
    ConstantDeclarationNode,
    IfStatementNode,
    WhileStatementNode,
    ForStatementNode,
)


class SymbolVisitor(ASTTraversalVisitor):
    """AST Traversal Visitor that populates SymbolTable scopes with declarations."""

    def __init__(self, symbol_table: Optional[SymbolTable] = None) -> None:
        self.symbol_table: SymbolTable = symbol_table or SymbolTable()

    def visit_program(self, node: ProgramNode) -> None:
        super().visit_program(node)

    def visit_block(self, node: BlockNode) -> None:
        self.symbol_table.enter_scope(name="block", scope_type=ScopeType.BLOCK)
        super().visit_block(node)
        self.symbol_table.exit_scope()

    def visit_variable_declaration(self, node: VariableDeclarationNode) -> None:
        var_sym = VariableSymbol(
            name=node.var_name,
            type_name=node.var_type,
            line=node.line,
            column=node.column,
            array_size=node.array_size,
        )
        self.symbol_table.define(var_sym)
        super().visit_variable_declaration(node)

    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> None:
        const_sym = ConstantSymbol(
            name=node.const_name,
            type_name=node.const_type,
            line=node.line,
            column=node.column,
        )
        self.symbol_table.define(const_sym)
        super().visit_constant_declaration(node)

    def visit_if_statement(self, node: IfStatementNode) -> None:
        node.condition.accept(self)
        if isinstance(node.then_branch, BlockNode):
            node.then_branch.accept(self)
        else:
            self.symbol_table.enter_scope(name="if_then", scope_type=ScopeType.CONDITIONAL)
            node.then_branch.accept(self)
            self.symbol_table.exit_scope()

        if node.else_branch:
            if isinstance(node.else_branch, BlockNode):
                node.else_branch.accept(self)
            else:
                self.symbol_table.enter_scope(name="if_else", scope_type=ScopeType.CONDITIONAL)
                node.else_branch.accept(self)
                self.symbol_table.exit_scope()

    def visit_while_statement(self, node: WhileStatementNode) -> None:
        node.condition.accept(self)
        if isinstance(node.body, BlockNode):
            node.body.accept(self)
        else:
            self.symbol_table.enter_scope(name="while_loop", scope_type=ScopeType.LOOP)
            node.body.accept(self)
            self.symbol_table.exit_scope()

    def visit_for_statement(self, node: ForStatementNode) -> None:
        self.symbol_table.enter_scope(name="for_loop", scope_type=ScopeType.LOOP)
        if node.init:
            node.init.accept(self)
        if node.condition:
            node.condition.accept(self)
        if node.update:
            node.update.accept(self)
        node.body.accept(self)
        self.symbol_table.exit_scope()
