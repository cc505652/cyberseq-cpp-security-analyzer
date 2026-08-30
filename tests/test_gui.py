"""
Pytest Unit Test Suite for GUI Subsystem.
"""

import pytest
import tkinter as tk
from gui.main_window import MainWindow
from gui.controller import Controller


@pytest.fixture
def app():
    try:
        main_win = MainWindow()
        main_win.withdraw()
        yield main_win
        main_win.destroy()
    except Exception as e:
        pytest.skip(f"GUI display not available in headless test runner: {e}")


def test_main_window_initialization(app: MainWindow) -> None:
    assert app.title() == "C/C++ Secure Code Analyzer"
    assert app.editor is not None
    assert app.token_panel is not None
    assert app.ast_panel is not None


def test_editor_text_operations(app: MainWindow) -> None:
    app.editor.set_text("int x = 10;")
    assert app.editor.get_text().strip() == "int x = 10;"
    app.editor.clear()
    assert app.editor.get_text().strip() == ""


def test_controller_analysis_flow(app: MainWindow) -> None:
    controller = Controller(app)
    app.editor.set_text("int x = 10; gets(x);")
    controller.analyze_code()
    assert app.status_bar.lbl_status.cget("text") == "Analysis completed successfully."
