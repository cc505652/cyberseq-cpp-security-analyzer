"""
Pytest Unit Test Suite for Symbol Table Subsystem.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.symbol_table import SymbolTable
from compiler.symbols import VariableSymbol, ConstantSymbol, FunctionSymbol


def test_symbol_table_scopes() -> None:
    st = SymbolTable()
    st.define(VariableSymbol("x", "int", line=1, column=5))
    assert st.lookup("x") is not None

    st.enter_scope("block_1")
    st.define(VariableSymbol("y", "float", line=2, column=5))
    assert st.lookup("x") is not None
    assert st.lookup("y") is not None

    st.exit_scope()
    assert st.lookup("x") is not None
    assert st.lookup("y") is None


def test_builtin_security_functions() -> None:
    st = SymbolTable()
    assert st.lookup("gets") is not None
    assert st.lookup("strcpy") is not None
    assert st.lookup("system") is not None


if __name__ == "__main__":
    pytest.main([__file__])
