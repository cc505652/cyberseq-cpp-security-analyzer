"""
Security Panel Tab Widget for Displaying Static Security Findings.
"""

import customtkinter as ctk
from tkinter import ttk
from gui import theme


class SecurityPanel(ctk.CTkFrame):
    """Tabular view displaying vulnerability security findings with severity badges."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        columns = ("severity", "rule_id", "vulnerability", "line", "recommendation")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("severity", text="Severity")
        self.tree.heading("rule_id", text="Rule ID")
        self.tree.heading("vulnerability", text="Vulnerability")
        self.tree.heading("line", text="Line")
        self.tree.heading("recommendation", text="Recommendation")

        self.tree.column("severity", width=90, anchor="center")
        self.tree.column("rule_id", width=80, anchor="center")
        self.tree.column("vulnerability", width=180, anchor="w")
        self.tree.column("line", width=60, anchor="center")
        self.tree.column("recommendation", width=320, anchor="w")

        # Color Tags for Severity Levels
        self.tree.tag_configure("Critical", foreground=theme.COLOR_CRITICAL)
        self.tree.tag_configure("High", foreground=theme.COLOR_HIGH)
        self.tree.tag_configure("Medium", foreground=theme.COLOR_MEDIUM)
        self.tree.tag_configure("Low", foreground=theme.COLOR_LOW)
        self.tree.tag_configure("Info", foreground=theme.COLOR_INFO)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def update_findings(self, findings_list) -> None:
        """Populates security finding treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for f in findings_list:
            sev_str = str(f.severity)
            self.tree.insert(
                "",
                "end",
                values=(sev_str, f.rule_id, f.vulnerability_name, f.line, f.recommendation),
                tags=(sev_str,),
            )
