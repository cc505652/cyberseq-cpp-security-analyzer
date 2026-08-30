"""
Main Window Layout for AI-Powered Secure Code Analyzer IDE.
"""

import customtkinter as ctk
import tkinter as tk
from gui import theme
from gui.menu_bar import MenuBar
from gui.editor import CodeEditor
from gui.token_panel import TokenPanel
from gui.ast_panel import ASTPanel
from gui.semantic_panel import SemanticPanel
from gui.security_panel import SecurityPanel
from gui.ai_panel import AIPanel
from gui.status_bar import StatusBar


class MainWindow(ctk.CTk):
    """Main Application Window for Tiny C Security Analyzer IDE."""

    def __init__(self) -> None:
        super().__init__()

        self.title("C/C++ Secure Code Analyzer")
        self.geometry("1280x768")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. Action Toolbar
        self.toolbar = ctk.CTkFrame(self, height=40, fg_color=theme.BG_SIDEBAR)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.btn_open = ctk.CTkButton(self.toolbar, text="Open File", width=90)
        self.btn_open.pack(side="left", padx=5, pady=5)

        self.btn_save = ctk.CTkButton(self.toolbar, text="Save File", width=90)
        self.btn_save.pack(side="left", padx=5, pady=5)

        self.btn_clear = ctk.CTkButton(self.toolbar, text="Clear", width=70, fg_color="#555555", hover_color="#666666")
        self.btn_clear.pack(side="left", padx=5, pady=5)

        self.btn_analyze = ctk.CTkButton(self.toolbar, text="Analyze Code (F5)", width=130, fg_color="#28a745", hover_color="#218838")
        self.btn_analyze.pack(side="left", padx=15, pady=5)

        self.btn_report = ctk.CTkButton(self.toolbar, text="Generate Report", width=120, fg_color="#17a2b8", hover_color="#138496")
        self.btn_report.pack(side="left", padx=5, pady=5)

        self.btn_exit = ctk.CTkButton(self.toolbar, text="Exit", width=70, fg_color="#dc3545", hover_color="#c82333")
        self.btn_exit.pack(side="right", padx=5, pady=5)

        # 2. Central Paned Content Area (Editor Left, Tabs Right)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=2)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # Left Panel: Code Editor
        self.editor = CodeEditor(self.content_frame)
        self.editor.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Right Panel: Tabview for Diagnostics & AI Analysis
        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.grid(row=0, column=1, sticky="nsew")

        self.tab_tokens = self.tabview.add("Tokens")
        self.tab_ast = self.tabview.add("AST")
        self.tab_semantic = self.tabview.add("Semantic Errors")
        self.tab_security = self.tabview.add("Security Findings")
        self.tab_ai = self.tabview.add("AI Explanations")

        # Initialize Individual Panels in Tabs
        self._init_tab_panels()

        # 3. Bottom Status Bar
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=2, column=0, sticky="ew")

    def _init_tab_panels(self) -> None:
        # Tokens Panel
        self.tab_tokens.grid_rowconfigure(0, weight=1)
        self.tab_tokens.grid_columnconfigure(0, weight=1)
        self.token_panel = TokenPanel(self.tab_tokens)
        self.token_panel.grid(row=0, column=0, sticky="nsew")

        # AST Panel
        self.tab_ast.grid_rowconfigure(0, weight=1)
        self.tab_ast.grid_columnconfigure(0, weight=1)
        self.ast_panel = ASTPanel(self.tab_ast)
        self.ast_panel.grid(row=0, column=0, sticky="nsew")

        # Semantic Panel
        self.tab_semantic.grid_rowconfigure(0, weight=1)
        self.tab_semantic.grid_columnconfigure(0, weight=1)
        self.semantic_panel = SemanticPanel(self.tab_semantic)
        self.semantic_panel.grid(row=0, column=0, sticky="nsew")

        # Security Panel
        self.tab_security.grid_rowconfigure(0, weight=1)
        self.tab_security.grid_columnconfigure(0, weight=1)
        self.security_panel = SecurityPanel(self.tab_security)
        self.security_panel.grid(row=0, column=0, sticky="nsew")

        # AI Panel
        self.tab_ai.grid_rowconfigure(0, weight=1)
        self.tab_ai.grid_columnconfigure(0, weight=1)
        self.ai_panel = AIPanel(self.tab_ai)
        self.ai_panel.grid(row=0, column=0, sticky="nsew")
