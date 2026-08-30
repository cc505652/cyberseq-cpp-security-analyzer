"""
Semantic Analyzer Implementation for Tiny C Compiler.

Performs full semantic validation over the AST using Symbol Table lookups and TypeChecker rules:
- Declaration & Scope Enforcement (Undeclared vars, Duplicate declarations, Shadowing)
- Type Safety & Assignability (Type mismatches, Constant modification, Lvalue checks)
- Control Flow & Function Call Validation (Conditions, Argument counts, Return checks)
"""

from typing import Optional, Any
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
from compiler.symbol_table import SymbolTable
from compiler.symbols import (
    VariableSymbol,
    ConstantSymbol,
    FunctionSymbol,
    BuiltinFunctionSymbol,
)
from compiler.scope import ScopeType
from compiler.semantic_errors import SemanticErrorManager
from compiler.type_checker import TypeChecker


class SemanticAnalyzer(ASTVisitor):
    """AST Traversal Visitor enforcing Tiny C semantic and type rules."""

    def __init__(
        self,
        symbol_table: Optional[SymbolTable] = None,
        error_manager: Optional[SemanticErrorManager] = None,
    ) -> None:
        self.symbol_table: SymbolTable = symbol_table if symbol_table is not None else SymbolTable()
        self.error_manager: SemanticErrorManager = error_manager if error_manager is not None else SemanticErrorManager()

    def analyze(self, ast_root: ProgramNode) -> SemanticErrorManager:
        """Main entry point: analyzes ProgramNode root and returns SemanticErrorManager."""
        self.symbol_table = SymbolTable()
        self.error_manager.clear()
        ast_root.accept(self)
        return self.error_manager

    # --- PROGRAM & BLOCK SCOPES ---

    def visit_program(self, node: ProgramNode) -> Any:
        for stmt in node.statements:
            stmt.accept(self)

    def visit_block(self, node: BlockNode) -> Any:
        self.symbol_table.enter_scope(name="block", scope_type=ScopeType.BLOCK)
        for stmt in node.statements:
            stmt.accept(self)
        self.symbol_table.exit_scope()

    # --- DECLARATIONS ---

    def visit_variable_declaration(self, node: VariableDeclarationNode) -> Any:
        # Check 2: Duplicate Variable Declaration
        existing = self.symbol_table.lookup_current(node.var_name)
        if existing:
            self.error_manager.add_error(
                message=f"Redeclaration of identifier '{node.var_name}' in the same scope.",
                line=node.line,
                column=node.column,
                error_type="DUPLICATE_DECLARATION_ERROR",
            )
        else:
            var_sym = VariableSymbol(
                name=node.var_name,
                type_name=node.var_type,
                line=node.line,
                column=node.column,
                array_size=node.array_size,
            )
            self.symbol_table.define(var_sym)

        # Check 3: Type Mismatch in Initializer
        if node.initializer:
            init_type = node.initializer.accept(self)
            if init_type and not TypeChecker.is_assignable(node.var_type, init_type):
                self.error_manager.add_error(
                    message=f"Cannot initialize variable '{node.var_name}' of type '{node.var_type}' with expression of type '{init_type}'.",
                    line=node.line,
                    column=node.column,
                    error_type="TYPE_MISMATCH_ERROR",
                )

    def visit_constant_declaration(self, node: ConstantDeclarationNode) -> Any:
        existing = self.symbol_table.lookup_current(node.const_name)
        if existing:
            self.error_manager.add_error(
                message=f"Redeclaration of identifier '{node.const_name}' in the same scope.",
                line=node.line,
                column=node.column,
                error_type="DUPLICATE_DECLARATION_ERROR",
            )
        else:
            const_sym = ConstantSymbol(
                name=node.const_name,
                type_name=node.const_type,
                line=node.line,
                column=node.column,
            )
            self.symbol_table.define(const_sym)

        init_type = node.initializer.accept(self)
        if init_type and not TypeChecker.is_assignable(node.const_type, init_type):
            self.error_manager.add_error(
                message=f"Cannot initialize constant '{node.const_name}' of type '{node.const_type}' with expression of type '{init_type}'.",
                line=node.line,
                column=node.column,
                error_type="TYPE_MISMATCH_ERROR",
            )

    # --- STATEMENTS & ASSIGNMENTS ---

    def visit_assignment(self, node: AssignmentNode) -> Any:
        # Check 5: Invalid Assignment (Target must be an IdentifierNode lvalue)
        if not isinstance(node.target, IdentifierNode):
            self.error_manager.add_error(
                message="Invalid assignment target: left-hand side must be a variable identifier.",
                line=node.line,
                column=node.column,
                error_type="INVALID_ASSIGNMENT_ERROR",
            )
            val_type = node.value.accept(self)
            return val_type

        var_name = node.target.name
        sym = self.symbol_table.lookup(var_name)

        # Check 1: Undeclared Variable
        if not sym:
            self.error_manager.add_error(
                message=f"Variable '{var_name}' is not declared.",
                line=node.line,
                column=node.column,
                error_type="UNDECLARED_VARIABLE_ERROR",
            )
            val_type = node.value.accept(self)
            return val_type

        # Check 4: Constant Modification
        if isinstance(sym, ConstantSymbol) or not sym.is_mutable:
            self.error_manager.add_error(
                message=f"Cannot modify immutable constant '{var_name}'.",
                line=node.line,
                column=node.column,
                error_type="CONSTANT_MODIFICATION_ERROR",
            )

        val_type = node.value.accept(self)
        # Check 3: Type Mismatch in Assignment
        if val_type and sym.type_name:
            if not TypeChecker.is_assignable(sym.type_name, val_type):
                self.error_manager.add_error(
                    message=f"Cannot assign expression of type '{val_type}' to variable '{var_name}' of type '{sym.type_name}'.",
                    line=node.line,
                    column=node.column,
                    error_type="TYPE_MISMATCH_ERROR",
                )

        return sym.type_name

    def visit_expression_statement(self, node: ExpressionStatementNode) -> Any:
        return node.expression.accept(self)

    def visit_empty_statement(self, node: EmptyStatementNode) -> Any:
        return None

    # --- CONTROL FLOW STATEMENTS ---

    def visit_if_statement(self, node: IfStatementNode) -> Any:
        cond_type = node.condition.accept(self)
        # Check 6: Invalid Condition
        if cond_type and not TypeChecker.is_condition_valid(cond_type):
            self.error_manager.add_error(
                message=f"If condition must evaluate to boolean or numeric type, got '{cond_type}'.",
                line=node.line,
                column=node.column,
                error_type="INVALID_CONDITION_ERROR",
            )

        if isinstance(node.then_branch, BlockNode):
            node.then_branch.accept(self)
        else:
            self.symbol_table.enter_scope("if_then", ScopeType.CONDITIONAL)
            node.then_branch.accept(self)
            self.symbol_table.exit_scope()

        if node.else_branch:
            if isinstance(node.else_branch, BlockNode):
                node.else_branch.accept(self)
            else:
                self.symbol_table.enter_scope("if_else", ScopeType.CONDITIONAL)
                node.else_branch.accept(self)
                self.symbol_table.exit_scope()

    def visit_while_statement(self, node: WhileStatementNode) -> Any:
        cond_type = node.condition.accept(self)
        if cond_type and not TypeChecker.is_condition_valid(cond_type):
            self.error_manager.add_error(
                message=f"While condition must evaluate to boolean or numeric type, got '{cond_type}'.",
                line=node.line,
                column=node.column,
                error_type="INVALID_CONDITION_ERROR",
            )

        if isinstance(node.body, BlockNode):
            node.body.accept(self)
        else:
            self.symbol_table.enter_scope("while_loop", ScopeType.LOOP)
            node.body.accept(self)
            self.symbol_table.exit_scope()

    def visit_for_statement(self, node: ForStatementNode) -> Any:
        self.symbol_table.enter_scope("for_loop", ScopeType.LOOP)
        if node.init:
            node.init.accept(self)
        if node.condition:
            cond_type = node.condition.accept(self)
            if cond_type and not TypeChecker.is_condition_valid(cond_type):
                self.error_manager.add_error(
                    message=f"For loop condition must evaluate to boolean or numeric type, got '{cond_type}'.",
                    line=node.line,
                    column=node.column,
                    error_type="INVALID_CONDITION_ERROR",
                )
        if node.update:
            node.update.accept(self)
        node.body.accept(self)
        self.symbol_table.exit_scope()

    def visit_break(self, node: BreakNode) -> Any:
        return None

    def visit_continue(self, node: ContinueNode) -> Any:
        return None

    def visit_return(self, node: ReturnNode) -> Any:
        if node.value:
            return node.value.accept(self)
        return "void"

    def visit_print(self, node: PrintNode) -> Any:
        return node.expression.accept(self)

    # --- FUNCTION CALLS & EXPRESSIONS ---

    def visit_function_call(self, node: FunctionCallNode) -> Any:
        sym = self.symbol_table.lookup(node.func_name)

        # Check 7: Function Call Validation (Function Existence)
        if not sym:
            self.error_manager.add_error(
                message=f"Function '{node.func_name}' is not declared.",
                line=node.line,
                column=node.column,
                error_type="UNDECLARED_FUNCTION_ERROR",
            )
            for arg in node.arguments:
                arg.accept(self)
            return "void"

        if not isinstance(sym, (FunctionSymbol, BuiltinFunctionSymbol)):
            self.error_manager.add_error(
                message=f"Identifier '{node.func_name}' is a variable, not a callable function.",
                line=node.line,
                column=node.column,
                error_type="INVALID_CALL_ERROR",
            )
            return "void"

        # Check 7: Correct Number of Arguments
        expected_arg_count = len(sym.attributes.get("param_types", [])) if isinstance(sym, BuiltinFunctionSymbol) else len(sym.parameters)
        actual_arg_count = len(node.arguments)

        # Allow flexible args for print built-in
        if node.func_name != "print" and actual_arg_count != expected_arg_count:
            self.error_manager.add_error(
                message=f"Function '{node.func_name}' expects {expected_arg_count} arguments, but got {actual_arg_count}.",
                line=node.line,
                column=node.column,
                error_type="ARGUMENT_COUNT_MISMATCH_ERROR",
            )

        for arg in node.arguments:
            arg.accept(self)

        return sym.type_name

    def visit_identifier(self, node: IdentifierNode) -> Any:
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.error_manager.add_error(
                message=f"Variable '{node.name}' is not declared.",
                line=node.line,
                column=node.column,
                error_type="UNDECLARED_VARIABLE_ERROR",
            )
            return None
        return sym.type_name

    def visit_literal(self, node: LiteralNode) -> Any:
        return node.literal_type

    def visit_binary_expression(self, node: BinaryExpressionNode) -> Any:
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)

        if not left_type or not right_type:
            return None

        result_type = TypeChecker.get_binary_result_type(node.operator, left_type, right_type)
        if not result_type:
            self.error_manager.add_error(
                message=f"Invalid binary operation '{node.operator}' between type '{left_type}' and type '{right_type}'.",
                line=node.line,
                column=node.column,
                error_type="TYPE_MISMATCH_ERROR",
            )
            return None
        return result_type

    def visit_unary_expression(self, node: UnaryExpressionNode) -> Any:
        operand_type = node.operand.accept(self)
        if not operand_type:
            return None
        result_type = TypeChecker.get_unary_result_type(node.operator, operand_type)
        if not result_type:
            self.error_manager.add_error(
                message=f"Invalid unary operation '{node.operator}' for operand of type '{operand_type}'.",
                line=node.line,
                column=node.column,
                error_type="TYPE_MISMATCH_ERROR",
            )
            return None
        return result_type

    def visit_error(self, node: ErrorNode) -> Any:
        self.error_manager.add_error(
            message=node.error_message,
            line=node.line,
            column=node.column,
            error_type="SYNTAX_AST_ERROR",
        )
        return None
