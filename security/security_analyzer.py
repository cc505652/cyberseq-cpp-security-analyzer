"""
Security Analyzer Engine for Tiny C Compiler.

Walks the AST using ASTTraversalVisitor, dispatching rule-based security checks over each node,
and compiling structured vulnerability reports.
"""

from typing import List, Optional
from compiler.visitor import ASTTraversalVisitor
from compiler.ast_nodes import ASTNode, ProgramNode
from security.severity import Severity
from security.finding import SecurityFinding
from security.security_rules import (
    SecurityRule,
    HardcodedPasswordRule,
    HardcodedAPIKeyRule,
    WeakPasswordRule,
    SQLInjectionRule,
    CommandInjectionRule,
    UnsafeGetsRule,
    UnsafeStrcpyRule,
    UnsafeSprintfRule,
    WeakRandomRule,
    ResourceLeakRule,
)


class SecurityAnalyzer(ASTTraversalVisitor):
    """AST Visitor orchestrating rule-based static security scanning."""

    def __init__(self, rules: Optional[List[SecurityRule]] = None) -> None:
        self.rules: List[SecurityRule] = rules or [
            HardcodedPasswordRule(),
            HardcodedAPIKeyRule(),
            WeakPasswordRule(),
            SQLInjectionRule(),
            CommandInjectionRule(),
            UnsafeGetsRule(),
            UnsafeStrcpyRule(),
            UnsafeSprintfRule(),
            WeakRandomRule(),
            ResourceLeakRule(),
        ]
        self.findings: List[SecurityFinding] = []
        self._root: Optional[ProgramNode] = None

    def analyze(self, ast_root: ProgramNode) -> List[SecurityFinding]:
        """Main entry point: scans AST root and returns list of SecurityFinding objects."""
        self.findings.clear()
        self._root = ast_root

        # Execute root-level program rules first
        for rule in self.rules:
            res = rule.inspect(ast_root, program_root=ast_root)
            if res:
                self.findings.extend(res)

        # Walk AST nodes
        ast_root.accept(self)
        return list(self.findings)

    def _apply_rules(self, node: ASTNode) -> None:
        for rule in self.rules:
            # Skip program root rule double-run
            if isinstance(node, ProgramNode) and isinstance(rule, ResourceLeakRule):
                continue
            res = rule.inspect(node, program_root=self._root)
            if res:
                self.findings.extend(res)

    def visit_program(self, node: ProgramNode) -> None:
        self._apply_rules(node)
        super().visit_program(node)

    def visit_block(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_block(node)

    def visit_variable_declaration(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_variable_declaration(node)

    def visit_constant_declaration(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_constant_declaration(node)

    def visit_assignment(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_assignment(node)

    def visit_expression_statement(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_expression_statement(node)

    def visit_if_statement(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_if_statement(node)

    def visit_while_statement(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_while_statement(node)

    def visit_for_statement(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_for_statement(node)

    def visit_function_call(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_function_call(node)

    def visit_literal(self, node: ASTNode) -> None:
        self._apply_rules(node)
        super().visit_literal(node)
