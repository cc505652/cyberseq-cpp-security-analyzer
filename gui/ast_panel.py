"""
AST Panel Tab Widget for Displaying Pretty-Printed Syntax Trees.
"""

import customtkinter as ctk
from gui import theme


class ASTPanel(ctk.CTkFrame):
    """Scrollable text widget displaying pretty-printed AST hierarchy."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(
            self,
            font=(theme.FONT_FAMILY_CODE, 11),
            activate_scrollbars=True,
            wrap="none",
        )
        self.textbox.grid(row=0, column=0, sticky="nsew")

    def update_ast(self, ast_text: str) -> None:
        """Updates text area with formatted AST ASCII string."""
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", ast_text)
