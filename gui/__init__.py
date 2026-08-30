"""
GUI Package Initialization for Tiny C IDE Application.
"""

from gui.theme import BG_DARK, ACCENT_PRIMARY
from gui.editor import CodeEditor
from gui.token_panel import TokenPanel
from gui.ast_panel import ASTPanel
from gui.semantic_panel import SemanticPanel
from gui.security_panel import SecurityPanel
from gui.ai_panel import AIPanel
from gui.status_bar import StatusBar
from gui.main_window import MainWindow
from gui.controller import Controller

__all__ = [
    "BG_DARK",
    "ACCENT_PRIMARY",
    "CodeEditor",
    "TokenPanel",
    "ASTPanel",
    "SemanticPanel",
    "SecurityPanel",
    "AIPanel",
    "StatusBar",
    "MainWindow",
    "Controller",
]
