"""
Menu Bar Integration for Tiny C IDE GUI.
"""

import tkinter as tk
from typing import Callable, Optional


class MenuBar(tk.Menu):
    """Top window menu bar for file operations, tool triggering, and help."""

    def __init__(
        self,
        master,
        on_open: Optional[Callable] = None,
        on_save: Optional[Callable] = None,
        on_exit: Optional[Callable] = None,
        on_analyze: Optional[Callable] = None,
        on_report: Optional[Callable] = None,
        on_about: Optional[Callable] = None,
    ) -> None:
        super().__init__(master)

        # File Menu
        file_menu = tk.Menu(self, tearoff=0)
        if on_open: file_menu.add_command(label="Open File...", command=on_open, accelerator="Ctrl+O")
        if on_save: file_menu.add_command(label="Save File...", command=on_save, accelerator="Ctrl+S")
        file_menu.add_separator()
        if on_exit: file_menu.add_command(label="Exit", command=on_exit)
        self.add_cascade(label="File", menu=file_menu)

        # Tools Menu
        tools_menu = tk.Menu(self, tearoff=0)
        if on_analyze: tools_menu.add_command(label="Analyze Code", command=on_analyze, accelerator="F5")
        if on_report: tools_menu.add_command(label="Generate Report", command=on_report)
        self.add_cascade(label="Tools", menu=tools_menu)

        # Help Menu
        help_menu = tk.Menu(self, tearoff=0)
        if on_about: help_menu.add_command(label="About", command=on_about)
        self.add_cascade(label="Help", menu=help_menu)
