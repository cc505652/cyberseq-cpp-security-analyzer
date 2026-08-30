"""
MVC Controller Module for Tiny C Security Analyzer IDE GUI.

Connects UI events (file open, save, analyze) with backend compiler, static security,
and AI explanation pipelines.
"""

from tkinter import filedialog, messagebox
import os
from typing import Optional
from gui.main_window import MainWindow

from compiler.lexer import TinyCLexer
from compiler.parser import TinyCParser
from compiler.ast_printer import ASTPrinter
from compiler.semantic import SemanticAnalyzer
from security.security_analyzer import SecurityAnalyzer
from ai.ai_helper import AIHelper


class Controller:
    """MVC Controller linking MainWindow View with Compiler & Analysis Models."""

    def __init__(self, view: MainWindow) -> None:
        self.view: MainWindow = view
        self.current_file_path: Optional[str] = None

        self.lexer = TinyCLexer()
        self.parser = TinyCParser()
        self.semantic_analyzer = SemanticAnalyzer()
        self.security_analyzer = SecurityAnalyzer()
        self.ai_helper = AIHelper()

        self._bind_events()

    def _bind_events(self) -> None:
        """Attaches handlers to GUI toolbar buttons and key events."""
        self.view.btn_open.configure(command=self.open_file)
        self.view.btn_save.configure(command=self.save_file)
        self.view.btn_clear.configure(command=self.clear_editor)
        self.view.btn_analyze.configure(command=self.analyze_code)
        self.view.btn_report.configure(command=self.generate_report)
        self.view.btn_exit.configure(command=self.view.destroy)

        self.view.bind("<F5>", lambda e: self.analyze_code())

    def open_file(self) -> None:
        """Opens source file dialog and loads code into editor."""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("C/C++ Source Files", "*.c *.cpp *.h *.hpp"),
                ("Tiny C Files", "*.tc"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                self.view.editor.set_text(code)
                self.current_file_path = file_path
                self.view.status_bar.set_status(f"Loaded file: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("File Error", f"Could not read file: {e}")

    def save_file(self) -> None:
        """Saves editor content to file."""
        if not self.current_file_path:
            self.current_file_path = filedialog.asksaveasfilename(
                defaultextension=".cpp",
                filetypes=[
                    ("C++ Source Files", "*.cpp"),
                    ("C Source Files", "*.c"),
                    ("Tiny C Files", "*.tc"),
                    ("All Files", "*.*"),
                ],
            )
        if self.current_file_path:
            try:
                code = self.view.editor.get_text()
                with open(self.current_file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                self.view.status_bar.set_status(f"Saved file: {os.path.basename(self.current_file_path)}")
            except Exception as e:
                messagebox.showerror("File Error", f"Could not save file: {e}")

    def clear_editor(self) -> None:
        """Clears code editor text."""
        self.view.editor.clear()
        self.current_file_path = None
        self.view.status_bar.set_status("Editor cleared.")

    def analyze_code(self) -> None:
        """Runs complete compiler analysis pipeline."""
        code = self.view.editor.get_text().strip()
        if not code:
            messagebox.showwarning("Warning", "Editor is empty. Please enter source code to analyze.")
            return

        self.view.status_bar.set_status("Analyzing code...")
        self.view.update_idletasks()

        try:
            # Cleanly reset analyzer components for every Analyze operation
            self.lexer = TinyCLexer()
            self.parser = TinyCParser()
            self.semantic_analyzer = SemanticAnalyzer()
            self.security_analyzer = SecurityAnalyzer()

            # 1. Lexical Analysis
            tokens_list = self.lexer.tokenize(code)
            self.view.token_panel.update_tokens(tokens_list)

            # 2. Syntax Analysis & AST Generation
            ast_root = self.parser.parse(code)
            ast_printer = ASTPrinter()
            ast_text = ast_printer.print_tree(ast_root)
            self.view.ast_panel.update_ast(ast_text)

            # 3. Semantic Analysis
            semantic_errors = self.semantic_analyzer.analyze(ast_root)
            self.view.semantic_panel.update_errors(semantic_errors.errors)

            # 4. Static Security Analysis
            security_findings = self.security_analyzer.analyze(ast_root)
            self.view.security_panel.update_findings(security_findings)

            # 5. AI Explanation Generation
            if security_findings:
                ai_results = self.ai_helper.explain_all_findings(security_findings)
                formatted_ai_text = "\n\n" + "=" * 60 + "\n\n".join(
                    f"### Finding [{item['finding']['rule_id']}] {item['finding']['vulnerability_name']}\n\n{item['ai_explanation']}"
                    for item in ai_results
                )
                self.view.ai_panel.update_explanations(formatted_ai_text)
            else:
                self.view.ai_panel.update_explanations("No security vulnerabilities detected in the analyzed code.")

            # Update Status Bar Metrics
            self.view.status_bar.set_metrics(
                tokens_count=len(tokens_list),
                error_count=len(semantic_errors.errors),
                finding_count=len(security_findings),
            )
            self.view.status_bar.set_status("Analysis completed successfully.")

        except Exception as err:
            self.view.status_bar.set_status("Analysis failed due to error.")
            messagebox.showerror("Compiler Pipeline Error", f"An error occurred during analysis:\n{err}")

    def generate_report(self) -> None:
        """Invokes PDFReportGenerator to compile all analysis results into a PDF report."""
        code = self.view.editor.get_text().strip()
        if not code:
            messagebox.showwarning("Warning", "Editor is empty. Please analyze code before generating report.")
            return

        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf"), ("All Files", "*.*")],
            title="Save Audit PDF Report",
        )
        if not pdf_path:
            return

        try:
            self.view.status_bar.set_status("Generating PDF Report...")
            self.view.update_idletasks()

            lexer = TinyCLexer()
            parser = TinyCParser()
            semantic_analyzer = SemanticAnalyzer()
            security_analyzer = SecurityAnalyzer()

            tokens_list = lexer.tokenize(code)
            ast_root = parser.parse(code)
            from compiler.symbol_table import SymbolTable
            from compiler.symbol_visitor import SymbolVisitor
            st = SymbolTable()
            ast_root.accept(SymbolVisitor(st))

            semantic_errors = semantic_analyzer.analyze(ast_root).errors
            security_findings = security_analyzer.analyze(ast_root)
            ai_results = self.ai_helper.explain_all_findings(security_findings) if security_findings else []

            from reports.report_generator import PDFReportGenerator
            generator = PDFReportGenerator()
            source_name = os.path.basename(self.current_file_path) if self.current_file_path else "source_code.cpp"
            generator.generate(
                output_filename=pdf_path,
                source_filename=source_name,
                code_text=code,
                tokens_list=tokens_list,
                ast_root=ast_root,
                symbol_table=st,
                semantic_errors=semantic_errors,
                security_findings=security_findings,
                ai_explanations=ai_results,
            )

            self.view.status_bar.set_status(f"PDF report generated: {os.path.basename(pdf_path)}")
            messagebox.showinfo("Report Success", f"Security Audit PDF Report generated successfully:\n{pdf_path}")
        except Exception as err:
            self.view.status_bar.set_status("Report generation failed.")
            messagebox.showerror("Report Error", f"Could not generate PDF report: {err}")
