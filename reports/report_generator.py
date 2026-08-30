"""
PDF Report Generator Module for C/C++ Secure Code Analyzer.

Assembles compiler diagnostics, static security findings, symbol tables, and AI explanations
into a formatted PDF document using ReportLab.
"""

import os
from typing import Any, Dict, List, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reports.report_templates import NumberedCanvas, get_report_styles
from reports.report_utils import calculate_security_score, get_current_timestamp


def get_language_mode(source_filename: str) -> str:
    """Determines dynamic language mode based on input filename extension."""
    ext = os.path.splitext(source_filename)[1].lower()
    if ext == ".tc":
        return "Tiny C Mode"
    elif ext == ".c":
        return "C Mode"
    elif ext in (".cpp", ".cc", ".cxx", ".hpp", ".h"):
        return "C++ Subset Mode"
    return "C/C++ Mode"


class PDFReportGenerator:
    """Orchestrates PDF report creation summarizing all compiler engine phases."""

    def __init__(
        self,
        student_name: str = "Engineering Student",
        guide_name: str = "Prof. Project Guide",
        college_name: str = "Department of Computer Engineering",
    ) -> None:
        self.student_name: str = student_name
        self.guide_name: str = guide_name
        self.college_name: str = college_name
        self.styles = get_report_styles()

    def generate(
        self,
        output_filename: str,
        source_filename: str,
        code_text: str,
        tokens_list: List[Any],
        ast_root: Any,
        symbol_table: Any,
        semantic_errors: List[Any],
        security_findings: List[Any],
        ai_explanations: List[Dict[str, Any]],
    ) -> str:
        """Generates PDF report and saves to output_filename."""
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=letter,
            leftMargin=54,
            rightMargin=54,
            topMargin=54,
            bottomMargin=54,
        )

        elements = []
        lines_of_code = len(code_text.splitlines()) if code_text else 0
        score, rating = calculate_security_score(security_findings)
        lang_mode = get_language_mode(source_filename)

        # 1. Cover Page
        elements.extend(self._build_cover_page(source_filename, lang_mode))
        elements.append(PageBreak())

        # 2. Executive Analysis Summary
        elements.extend(self._build_summary_section(source_filename, lang_mode, lines_of_code, tokens_list, semantic_errors, security_findings, score, rating))
        elements.append(Spacer(1, 15))

        # 3. Compiler Pipeline Results
        elements.extend(self._build_compiler_results_section(tokens_list, ast_root, semantic_errors))
        elements.append(Spacer(1, 15))

        # 4. Token Table
        elements.extend(self._build_token_table_section(tokens_list))
        elements.append(Spacer(1, 15))

        # 5. Symbol Table
        elements.extend(self._build_symbol_table_section(symbol_table))
        elements.append(Spacer(1, 15))

        # 6. Semantic Errors
        elements.extend(self._build_semantic_errors_section(semantic_errors))
        elements.append(Spacer(1, 15))

        # 7. Security Findings
        elements.extend(self._build_security_findings_section(security_findings))
        elements.append(Spacer(1, 15))

        # 8. AI Explanations
        elements.extend(self._build_ai_explanations_section(ai_explanations))
        elements.append(Spacer(1, 15))

        # 9. Scoring Breakdown & Conclusion
        elements.extend(self._build_conclusion_section(score, rating, len(semantic_errors), security_findings))

        doc.build(elements, canvasmaker=NumberedCanvas)
        return output_filename

    # --- SECTION BUILDERS ---

    def _build_cover_page(self, source_filename: str, lang_mode: str) -> List[Any]:
        elems = []
        elems.append(Spacer(1, 80))
        elems.append(Paragraph("C/C++ Secure Code Analyzer", self.styles["title"]))
        elems.append(Paragraph("Automated Compiler Audit & Static Vulnerability Report", self.styles["subtitle"]))
        elems.append(Spacer(1, 100))

        details = [
            [Paragraph("<b>Target File:</b>", self.styles["body"]), Paragraph(source_filename, self.styles["body"])],
            [Paragraph("<b>Language Mode:</b>", self.styles["body"]), Paragraph(lang_mode, self.styles["body"])],
            [Paragraph("<b>Student Name:</b>", self.styles["body"]), Paragraph(self.student_name, self.styles["body"])],
            [Paragraph("<b>Project Guide:</b>", self.styles["body"]), Paragraph(self.guide_name, self.styles["body"])],
            [Paragraph("<b>Institution:</b>", self.styles["body"]), Paragraph(self.college_name, self.styles["body"])],
            [Paragraph("<b>Generated Date:</b>", self.styles["body"]), Paragraph(get_current_timestamp(), self.styles["body"])],
        ]
        t = Table(details, colWidths=[140, 364])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
        elems.append(t)
        return elems

    def _build_summary_section(self, source_file: str, lang_mode: str, loc: int, tokens: list, errors: list, findings: list, score: int, rating: str) -> List[Any]:
        elems = [Paragraph("1. Executive Analysis Summary", self.styles["h1"])]
        data = [
            ["Metric", "Value"],
            ["Source File", source_file],
            ["Language Mode", lang_mode],
            ["Lines of Code (LOC)", str(loc)],
            ["Total Lexical Tokens", str(len(tokens))],
            ["Semantic Errors", str(len(errors))],
            ["Security Findings", str(len(findings))],
            ["Security Score", f"{score} / 100 ({rating})"],
        ]
        t = Table(data, colWidths=[200, 304])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#007ACC")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elems.append(t)
        return elems

    def _build_compiler_results_section(self, tokens: list, ast_root: Any, errors: list) -> List[Any]:
        elems = [Paragraph("2. Compiler Engine Results", self.styles["h1"])]
        ast_status = "Generated Successfully" if ast_root else "Failed"
        semantic_status = "PASSED (0 Errors)" if not errors else f"FAILED ({len(errors)} Errors)"

        data = [
            ["Phase", "Status Summary"],
            ["Lexical Analysis", f"Passed ({len(tokens)} Tokens)"],
            ["Syntax Analysis", "Passed"],
            ["AST Generation", ast_status],
            ["Semantic Analysis", semantic_status],
        ]
        t = Table(data, colWidths=[200, 304])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#252526")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elems.append(t)
        return elems

    def _build_token_table_section(self, tokens: list) -> List[Any]:
        elems = [Paragraph("3. Sample Lexical Token Table", self.styles["h1"])]
        data = [["Token Type", "Lexeme Value", "Line Number"]]
        for tok in tokens[:10]:
            tok_type = Paragraph(str(tok.type), self.styles["body"])
            tok_val = Paragraph(str(tok.value), self.styles["body"])
            data.append([tok_type, tok_val, str(tok.line)])

        t = Table(data, colWidths=[150, 254, 100])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F0F0F0")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#DDDDDD")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elems.append(t)
        return elems

    def _build_symbol_table_section(self, symbol_table: Any) -> List[Any]:
        elems = [Paragraph("4. Symbol Table Overview", self.styles["h1"])]
        data = [["Identifier", "Kind / Type", "Scope", "Pos"]]

        if hasattr(symbol_table, "scope_manager"):
            for scope in symbol_table.scope_manager.all_scopes:
                for sym in list(scope.symbols.values())[:5]:
                    pos = f"{sym.line}:{sym.column}"
                    data.append([
                        Paragraph(sym.name, self.styles["body"]),
                        Paragraph(f"{sym.__class__.__name__} ({sym.type_name})", self.styles["body"]),
                        Paragraph(scope.name, self.styles["body"]),
                        pos,
                    ])

        if len(data) == 1:
            data.append(["No user symbols defined", "-", "-", "-"])

        t = Table(data, colWidths=[130, 184, 130, 60])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#F0F0F0")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#DDDDDD")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elems.append(t)
        return elems

    def _build_semantic_errors_section(self, errors: list) -> List[Any]:
        elems = [Paragraph("5. Semantic Diagnostic Errors", self.styles["h1"])]
        if not errors:
            elems.append(Paragraph("No semantic errors detected in program.", self.styles["body"]))
            return elems

        data = [["Line", "Error Type", "Message"]]
        for err in errors:
            pos = str(err.line) if getattr(err, "line", 0) > 0 else "Global"
            err_type = Paragraph(getattr(err, "error_type", "ERROR"), self.styles["body"])
            err_msg = Paragraph(getattr(err, "message", str(err)), self.styles["body"])
            data.append([pos, err_type, err_msg])

        t = Table(data, colWidths=[50, 150, 304])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#FF4D4D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elems.append(t)
        return elems

    def _build_security_findings_section(self, findings: list) -> List[Any]:
        elems = [Paragraph("6. Static Security Findings", self.styles["h1"])]
        if not findings:
            elems.append(Paragraph("No security vulnerabilities detected.", self.styles["body"]))
            return elems

        data = [["Severity", "Rule ID", "Vulnerability", "Line", "Recommendation"]]
        for f in findings:
            sev = Paragraph(str(f.severity), self.styles["body"])
            rule = Paragraph(f.rule_id, self.styles["body"])
            vuln = Paragraph(f.vulnerability_name, self.styles["body"])
            line_str = str(f.line)
            rec = Paragraph(f.recommendation, self.styles["body"])
            data.append([sev, rule, vuln, line_str, rec])

        t = Table(data, colWidths=[70, 60, 130, 40, 204])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#252526")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elems.append(t)
        return elems

    def _build_ai_explanations_section(self, ai_explanations: list) -> List[Any]:
        elems = [Paragraph("7. AI Educational Explanations", self.styles["h1"])]
        if not ai_explanations:
            elems.append(Paragraph("No AI explanations generated.", self.styles["body"]))
            return elems

        for item in ai_explanations:
            finding_info = item.get("finding", {})
            explanation_text = item.get("ai_explanation", "")

            title_text = f"Finding [{finding_info.get('rule_id', 'SEC')}] {finding_info.get('vulnerability_name', 'Vulnerability')}"
            elems.append(Paragraph(title_text, self.styles["h2"]))

            clean_text = explanation_text.replace("#", "").strip()
            elems.append(Paragraph(clean_text.replace("\n", "<br/>"), self.styles["body"]))
            elems.append(Spacer(1, 10))

        return elems

    def _build_conclusion_section(self, score: int, rating: str, err_count: int, findings: list) -> List[Any]:
        elems = [Paragraph("8. Overall Audit Conclusion & Scoring Summary", self.styles["h1"])]

        # Transparent Scoring Breakdown Table
        critical_count = sum(1 for f in findings if str(getattr(f, "severity", "")) == "Critical")
        high_count = sum(1 for f in findings if str(getattr(f, "severity", "")) == "High")
        medium_count = sum(1 for f in findings if str(getattr(f, "severity", "")) == "Medium")
        low_count = sum(1 for f in findings if str(getattr(f, "severity", "")) == "Low")

        score_table_data = [
            ["Severity Category", "Deduction Weight", "Findings Count", "Total Deduction"],
            ["Critical Severity", "-20 points each", str(critical_count), f"-{critical_count * 20}"],
            ["High Severity", "-10 points each", str(high_count), f"-{high_count * 10}"],
            ["Medium Severity", "-5 points each", str(medium_count), f"-{medium_count * 5}"],
            ["Low Severity", "-2 points each", str(low_count), f"-{low_count * 2}"],
            ["Base Score", "100 Points", f"Total Findings: {len(findings)}", f"Final Score: {score} / 100 ({rating})"],
        ]

        t_score = Table(score_table_data, colWidths=[140, 120, 114, 130])
        t_score.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#007ACC")),
            ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#CCCCCC")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("BACKGROUND", (0, -1), (-1, -1), HexColor("#F0F0F0")),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ]))
        elems.append(t_score)
        elems.append(Spacer(1, 10))

        summary_text = (
            f"The analyzed source file achieved an overall Security Score of <b>{score} / 100 ({rating})</b>. "
            f"Static compiler analysis identified <b>{err_count}</b> semantic errors and <b>{len(findings)}</b> security vulnerabilities."
        )
        elems.append(Paragraph(summary_text, self.styles["body"]))
        return elems
