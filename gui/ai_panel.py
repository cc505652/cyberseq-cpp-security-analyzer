"""
AI Panel Tab Widget for Displaying Educational Vulnerability Explanations.
"""

import customtkinter as ctk
from gui import theme


class AIPanel(ctk.CTkFrame):
    """Scrollable text view rendering educational LLM vulnerability explanations."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(
            self,
            font=(theme.FONT_FAMILY_CODE, 11),
            activate_scrollbars=True,
            wrap="word",
        )
        self.textbox.grid(row=0, column=0, sticky="nsew")

    def update_explanations(self, explanations_text: str) -> None:
        """Updates text area with AI explanation Markdown text."""
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", explanations_text)
