"""
Code Editor Widget Module for Tiny C IDE GUI.

Provides source code editing area with synchronized line numbers, scrolling,
and text retrieval helpers.
"""

import customtkinter as ctk
import tkinter as tk
from gui import theme


class CodeEditor(ctk.CTkFrame):
    """CustomTkinter Code Editor widget with line numbers and scrolling."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Line Number Sidebar
        self.line_numbers = tk.Text(
            self,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background=theme.BG_SIDEBAR,
            foreground="#858585",
            state="disabled",
            font=(theme.FONT_FAMILY_CODE, 11),
        )
        self.line_numbers.grid(row=0, column=0, sticky="nsew")

        # Main Code Text Area
        self.textbox = ctk.CTkTextbox(
            self,
            font=(theme.FONT_FAMILY_CODE, 12),
            activate_scrollbars=True,
            wrap="none",
        )
        self.textbox.grid(row=0, column=1, sticky="nsew")

        # Bind events for line number synchronization
        self.textbox.bind("<KeyRelease>", self._update_line_numbers)
        self.textbox.bind("<MouseWheel>", self._update_line_numbers)
        self._update_line_numbers()

    def _update_line_numbers(self, event=None) -> None:
        content = self.textbox.get("1.0", "end-1c")
        line_count = content.count("\n") + 1
        lines_string = "\n".join(str(i) for i in range(1, line_count + 1))

        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", lines_string)
        self.line_numbers.config(state="disabled")

    def get_text(self) -> str:
        """Returns current editor text content."""
        return self.textbox.get("1.0", "end-1c")

    def set_text(self, text: str) -> None:
        """Sets editor text content."""
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
        self._update_line_numbers()

    def clear(self) -> None:
        """Clears editor text."""
        self.textbox.delete("1.0", "end")
        self._update_line_numbers()
