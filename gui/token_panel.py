"""
Token Panel Tab Widget for Displaying Lexical Analysis Results.
"""

import customtkinter as ctk
from tkinter import ttk
from gui import theme


class TokenPanel(ctk.CTkFrame):
    """Tabular widget presenting lexical token stream."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Style Treeview for Dark Theme
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=theme.BG_CARD,
            foreground=theme.TEXT_PRIMARY,
            fieldbackground=theme.BG_CARD,
            rowheight=24,
        )
        style.configure("Treeview.Heading", background=theme.BG_SIDEBAR, foreground=theme.TEXT_HEADER, font=(theme.FONT_FAMILY_UI, 10, "bold"))
        style.map("Treeview", background=[("selected", theme.ACCENT_PRIMARY)])

        columns = ("token", "lexeme", "line", "column")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("token", text="Token Type")
        self.tree.heading("lexeme", text="Lexeme Value")
        self.tree.heading("line", text="Line")
        self.tree.heading("column", text="Column")

        self.tree.column("token", width=120, anchor="w")
        self.tree.column("lexeme", width=160, anchor="w")
        self.tree.column("line", width=60, anchor="center")
        self.tree.column("column", width=60, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def update_tokens(self, tokens_list) -> None:
        """Populates token treeview with TokenInfo list."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for tok in tokens_list:
            self.tree.insert("", "end", values=(tok.type, tok.value, tok.line, tok.column))
