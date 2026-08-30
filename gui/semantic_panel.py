"""
Semantic Panel Tab Widget for Displaying Semantic & Type Errors.
"""

import customtkinter as ctk
from tkinter import ttk
from gui import theme


class SemanticPanel(ctk.CTkFrame):
    """Tabular view presenting semantic diagnostic errors."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        columns = ("line", "type", "message")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("line", text="Line")
        self.tree.heading("type", text="Error Type")
        self.tree.heading("message", text="Diagnostic Message")

        self.tree.column("line", width=60, anchor="center")
        self.tree.column("type", width=180, anchor="w")
        self.tree.column("message", width=450, anchor="w")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def update_errors(self, errors_list) -> None:
        """Populates semantic error list."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for err in errors_list:
            pos = str(err.line) if err.line > 0 else "Global"
            self.tree.insert("", "end", values=(pos, err.error_type, err.message))
