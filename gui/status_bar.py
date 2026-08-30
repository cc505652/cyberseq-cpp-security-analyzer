"""
Status Bar Module for Tiny C IDE GUI.

Displays current compilation status, active file path, and analysis metrics.
"""

import customtkinter as ctk
from gui import theme


class StatusBar(ctk.CTkFrame):
    """Bottom status bar displaying compiler metrics and status message."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, height=25, fg_color=theme.BG_SIDEBAR, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            self,
            text="Ready",
            font=(theme.FONT_FAMILY_UI, 11),
            anchor="w",
            text_color=theme.TEXT_PRIMARY,
        )
        self.lbl_status.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        self.lbl_metrics = ctk.CTkLabel(
            self,
            text="Tokens: 0 | Semantic Errors: 0 | Security Findings: 0",
            font=(theme.FONT_FAMILY_UI, 11),
            anchor="e",
            text_color=theme.TEXT_PRIMARY,
        )
        self.lbl_metrics.grid(row=0, column=1, padx=10, pady=2, sticky="e")

    def set_status(self, message: str) -> None:
        """Sets status text."""
        self.lbl_status.configure(text=message)

    def set_metrics(self, tokens_count: int, error_count: int, finding_count: int) -> None:
        """Updates compilation metrics counters."""
        self.lbl_metrics.configure(
            text=f"Tokens: {tokens_count} | Semantic Errors: {error_count} | Security Findings: {finding_count}"
        )
