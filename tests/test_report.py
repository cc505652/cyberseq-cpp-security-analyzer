"""
Pytest Unit Test Suite for PDF Report Subsystem.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from reports.report_utils import calculate_security_score
from reports.report_generator import PDFReportGenerator


def test_security_score_calculation() -> None:
    class DummyFinding:
        severity = "High"
    score, rating = calculate_security_score([DummyFinding(), DummyFinding()])
    assert score == 80
    assert rating == "Good"


def test_pdf_report_generation(tmp_path) -> None:
    pdf_file = str(tmp_path / "audit_report.pdf")
    generator = PDFReportGenerator()
    result_path = generator.generate(
        output_filename=pdf_file, source_filename="test_program.tc", code_text="int x = 10;",
        tokens_list=[], ast_root=None, symbol_table=None, semantic_errors=[], security_findings=[], ai_explanations=[],
    )
    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0


if __name__ == "__main__":
    pytest.main([__file__])
