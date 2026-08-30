"""
Compiler package initialization for Tiny C compiler.
"""

from compiler.config import KEYWORDS, SECURITY_FUNCTIONS
from compiler.tokens import tokens, TokenInfo
from compiler.errors import LexicalError, LexerErrorManager
from compiler.lexer import TinyCLexer
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
from compiler.visitor import ASTVisitor, ASTTraversalVisitor
from compiler.ast_builder import ASTBuilder
from compiler.ast_printer import ASTPrinter
from compiler.ast_visualizer import ASTVisualizer
from compiler.parser import TinyCParser
from compiler.symbols import (
    Symbol,
    VariableSymbol,
    ConstantSymbol,
    FunctionSymbol,
    BuiltinFunctionSymbol,
    ParameterSymbol,
    TemporarySymbol,
)
from compiler.scope import Scope, ScopeType
from compiler.scope_manager import ScopeManager
from compiler.symbol_table import SymbolTable
from compiler.symbol_visitor import SymbolVisitor
from compiler.semantic_errors import SemanticError, SemanticErrorManager
from compiler.type_checker import TypeChecker
from compiler.semantic import SemanticAnalyzer

__all__ = [
    "KEYWORDS",
    "SECURITY_FUNCTIONS",
    "tokens",
    "TokenInfo",
    "LexicalError",
    "LexerErrorManager",
    "TinyCLexer",
    "ASTNode",
    "ProgramNode",
    "BlockNode",
    "VariableDeclarationNode",
    "ConstantDeclarationNode",
    "AssignmentNode",
    "IdentifierNode",
    "LiteralNode",
    "BinaryExpressionNode",
    "UnaryExpressionNode",
    "IfStatementNode",
    "WhileStatementNode",
    "ForStatementNode",
    "BreakNode",
    "ContinueNode",
    "ReturnNode",
    "PrintNode",
    "FunctionCallNode",
    "ExpressionStatementNode",
    "EmptyStatementNode",
    "ErrorNode",
    "ASTVisitor",
    "ASTTraversalVisitor",
    "ASTBuilder",
    "ASTPrinter",
    "ASTVisualizer",
    "TinyCParser",
    "Symbol",
    "VariableSymbol",
    "ConstantSymbol",
    "FunctionSymbol",
    "BuiltinFunctionSymbol",
    "ParameterSymbol",
    "TemporarySymbol",
    "Scope",
    "ScopeType",
    "ScopeManager",
    "SymbolTable",
    "SymbolVisitor",
    "SemanticError",
    "SemanticErrorManager",
    "TypeChecker",
    "SemanticAnalyzer",
]
