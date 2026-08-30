"""
Pretty Printer Visitor for Tiny C Abstract Syntax Tree.

Converts AST node hierarchies into clean, human-readable ASCII tree structures
for terminal output, diagnostics, and visual debugging.
"""

from typing import List
from compiler.visitor import ASTVisitor
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


class ASTPrinter(ASTVisitor):
    """Generates ASCII hierarchical tree representations of AST nodes."""

    def __init__(self) -> None:
        self.lines: List[str] = []

    def print_tree(self, node: ASTNode) -> str:
        """Returns multiline ASCII tree representation of the AST node."""
        self.lines.clear()
        self._format_node(node, prefix="", is_last=True)
        return "\n".join(self.lines)

    def _format_node(self, node: ASTNode, prefix: str, is_last: bool) -> None:
        connector = "└── " if is_last else "├── "
        node_str = node.accept(self) if hasattr(node, "accept") else str(node)

        if not prefix:  # Root node
            self.lines.append(node_str)
            child_prefix = ""
        else:
            self.lines.append(f"{prefix}{connector}{node_str}")
            child_prefix = prefix + ("    " if is_last else "│   ")

        children = self._get_children(node)
        for i, child in enumerate(children):
            self._format_node(child, child_prefix, is_last=(i == len(children) - 1))

    def _get_children(self, node: ASTNode) -> List[ASTNode]:
        """Extracts child AST nodes for hierarchical tree rendering."""
        if isinstance(node, ProgramNode):
            return node.statements
        elif isinstance(node, BlockNode):
            return node.statements
        elif isinstance(node, VariableDeclarationNode):
            return [node.initializer] if node.initializer else []
        elif isinstance(node, ConstantDeclarationNode):
            return [node.initializer]
        elif isinstance(node, AssignmentNode):
            return [node.target, node.value]
        elif isinstance(node, ExpressionStatementNode):
            return [node.expression]
        elif isinstance(node, IfStatementNode):
            children = [node.condition, node.then_branch]
            if node.else_branch:
                children.append(node.else_branch)
            return children
        elif isinstance(node, WhileStatementNode):
            return [node.condition, node.body]
        elif isinstance(node, ForStatementNode):
            children = []
            if node.init:
                children.append(node.init)
            if node.condition:
                children.append(node.condition)
            if node.update:
                children.append(node.update)
            children.append(node.body)
            return children
        elif isinstance(node, ReturnNode):
            return [node.value] if node.value else []
        elif isinstance(node, PrintNode):
            return [node.expression]
        elif isinstance(node, FunctionCallNode):
            return node.arguments
        elif isinstance(node, BinaryExpressionNode):
            return [node.left, node.right]
        elif isinstance(node, UnaryExpressionNode):
            return [node.operand]
        return []

    # --- VISITOR METHOD IMPLEMENTATIONS ---

    def visit_program(self, node: ProgramNode) -> str:
        return "Program"

    def visit_block(self, node: BlockNode) -> str:
        return "Block"

    def visit_variable_declaration(self, node: VariableDeclarationNode) -> str:
        arr_str = f"[{node.array_size}]" if node.array_size is not None else ""
        return f"VarDecl({node.var_type} {node.var_name}{arr_str})"

    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> str:
        return f"ConstDecl(const {node.const_type} {node.const_name})"

    def visit_assignment(self, node: AssignmentNode) -> str:
        return f"Assignment({node.operator})"

    def visit_expression_statement(self, node: ExpressionStatementNode) -> str:
        return "ExprStmt"

    def visit_empty_statement(self, node: EmptyStatementNode) -> str:
        return "EmptyStmt(;)"

    def visit_if_statement(self, node: IfStatementNode) -> str:
        return "IfStatement"

    def visit_while_statement(self, node: WhileStatementNode) -> str:
        return "WhileLoop"

    def visit_for_statement(self, node: ForStatementNode) -> str:
        return "ForLoop"

    def visit_break(self, node: BreakNode) -> str:
        return "Break"

    def visit_continue(self, node: ContinueNode) -> str:
        return "Continue"

    def visit_return(self, node: ReturnNode) -> str:
        return "Return"

    def visit_print(self, node: PrintNode) -> str:
        return "Print"

    def visit_function_call(self, node: FunctionCallNode) -> str:
        return f"FunctionCall('{node.func_name}')"

    def visit_identifier(self, node: IdentifierNode) -> str:
        return f"Identifier({node.name})"

    def visit_literal(self, node: LiteralNode) -> str:
        return f"Literal({repr(node.value)}:{node.literal_type})"

    def visit_binary_expression(self, node: BinaryExpressionNode) -> str:
        return f"BinaryExpr('{node.operator}')"

    def visit_unary_expression(self, node: UnaryExpressionNode) -> str:
        pos = "prefix" if node.prefix else "postfix"
        return f"UnaryExpr('{node.operator}', {pos})"

    def visit_error(self, node: ErrorNode) -> str:
        return f"ASTError('{node.error_message}')"
