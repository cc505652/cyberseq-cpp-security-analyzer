"""
Pytest Unit Test Suite for AST Generation and Visitor Pattern.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.parser import TinyCParser
from compiler.ast_nodes import ProgramNode, VariableDeclarationNode, BinaryExpressionNode, FunctionCallNode
from compiler.ast_printer import ASTPrinter


@pytest.fixture
def parser() -> TinyCParser:
    return TinyCParser()


def test_variable_declaration_ast(parser: TinyCParser) -> None:
    code = "int x = 10;"
    ast_root = parser.parse(code)
    assert isinstance(ast_root, ProgramNode)
    assert len(ast_root.statements) == 1
    decl = ast_root.statements[0]
    assert isinstance(decl, VariableDeclarationNode)
    assert decl.var_type == "int"
    assert decl.var_name == "x"


def test_binary_expression_ast(parser: TinyCParser) -> None:
    code = "int result = a + b * c;"
    ast_root = parser.parse(code)
    decl = ast_root.statements[0]
    bin_op = decl.initializer
    assert isinstance(bin_op, BinaryExpressionNode)
    assert bin_op.operator == "+"
    assert bin_op.right.operator == "*"


def test_function_call_ast(parser: TinyCParser) -> None:
    code = 'gets(buffer);'
    ast_root = parser.parse(code)
    stmt = ast_root.statements[0]
    func_call = stmt.expression
    assert isinstance(func_call, FunctionCallNode)
    assert func_call.func_name == "gets"
    assert len(func_call.arguments) == 1


def test_ast_printer(parser: TinyCParser) -> None:
    code = "int x = 5;"
    ast_root = parser.parse(code)
    printer = ASTPrinter()
    tree_text = printer.print_tree(ast_root)
    assert "Program" in tree_text
    assert "VarDecl" in tree_text


if __name__ == "__main__":
    pytest.main([__file__])
