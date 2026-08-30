"""
Main Entry Point for AI-Powered Secure Code Analyzer.

Launches the CustomTkinter IDE GUI. If executed in a headless environment,
falls back gracefully to CLI interactive/batch mode.
"""

import os
import sys

# Ensure root workspace directory is always in sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def run_cli_fallback() -> None:
    """CLI mode fallback when GUI display environment is unavailable."""
    print("=" * 70)
    print("      AI-POWERED SECURE CODE ANALYZER (CLI MODE FALLBACK)")
    print("=" * 70)

    sample_code = (
        'int main() {\n'
        '    string password = "admin123";\n'
        '    char buffer[256];\n'
        '    gets(buffer);\n'
        '    string cmd = "rm -rf /";\n'
        '    system(cmd);\n'
        '    return 0;\n'
        '}'
    )

    print("\n[+] Running Lexical & Syntax Analysis...")
    from compiler.lexer import TinyCLexer
    from compiler.parser import TinyCParser
    from compiler.ast_printer import ASTPrinter
    from compiler.semantic import SemanticAnalyzer
    from security.security_analyzer import SecurityAnalyzer
    from ai.ai_helper import AIHelper

    lexer = TinyCLexer()
    tokens = lexer.tokenize(sample_code)
    print(f"    - Tokens generated: {len(tokens)}")

    parser = TinyCParser()
    ast_root = parser.parse(sample_code)
    print("    - AST generated successfully.")

    print("\n[+] Running Semantic & Security Analysis...")
    semantic_analyzer = SemanticAnalyzer()
    semantic_errors = semantic_analyzer.analyze(ast_root)
    print(f"    - Semantic Errors: {len(semantic_errors.errors)}")

    security_analyzer = SecurityAnalyzer()
    security_findings = security_analyzer.analyze(ast_root)
    print(f"    - Security Vulnerabilities Found: {len(security_findings)}")

    for finding in security_findings:
        print(f"\n    [{finding.rule_id}] [{finding.severity}] {finding.vulnerability_name} at Line {finding.line}")
        print(f"      Description: {finding.description}")
        print(f"      Recommendation: {finding.recommendation}")

    print("\n[+] Generating AI Explanations...")
    ai_helper = AIHelper()
    explanations = ai_helper.explain_all_findings(security_findings)
    print(f"    - AI Explanations generated for {len(explanations)} findings.")

    print("\n[+] CLI Audit Complete. Use a desktop display environment to launch full GUI IDE.")


def main() -> None:
    """Launches GUI or CLI fallback."""
    try:
        from gui.main_window import MainWindow
        from gui.controller import Controller

        app = MainWindow()
        controller = Controller(app)
        app.mainloop()
    except Exception as e:
        print(f"[Notice]: GUI environment unavailable ({e}). Switching to CLI mode...")
        run_cli_fallback()


if __name__ == "__main__":
    main()
