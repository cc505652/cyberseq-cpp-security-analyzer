"""
Security Rules Definitions Module for Tiny C Static Security Analyzer.

Implements rule-based AST security inspection logic without AI, searching for hardcoded credentials,
weak cryptography, injection vectors, memory unsafe function calls, and unclosed resource handles.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Set
from compiler.ast_nodes import (
    ASTNode,
    VariableDeclarationNode,
    ConstantDeclarationNode,
    AssignmentNode,
    IdentifierNode,
    LiteralNode,
    BinaryExpressionNode,
    FunctionCallNode,
    ProgramNode,
)
from security.severity import Severity
from security.finding import SecurityFinding


class SecurityRule(ABC):
    """Abstract Base Class for modular AST Security Rules."""

    rule_id: str = "SEC000"
    vulnerability_name: str = "Generic Vulnerability"
    severity: Severity = Severity.INFO

    @abstractmethod
    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        """Inspects an AST node and returns list of SecurityFinding objects."""
        pass


class HardcodedPasswordRule(SecurityRule):
    """SEC001: Detects hardcoded passwords assigned to variables or constants."""

    rule_id = "SEC001"
    vulnerability_name = "Hardcoded Password"
    severity = Severity.HIGH

    PASSWORD_KEYWORDS = {"password", "passwd", "pass", "pwd", "secret", "user_pass"}

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        var_name = None
        init_node = None
        line = node.line if getattr(node, "line", 0) > 0 else 1

        if isinstance(node, VariableDeclarationNode):
            var_name = node.var_name.lower()
            init_node = node.initializer
        elif isinstance(node, ConstantDeclarationNode):
            var_name = node.const_name.lower()
            init_node = node.initializer
        elif isinstance(node, AssignmentNode) and isinstance(node.target, IdentifierNode):
            var_name = node.target.name.lower()
            init_node = node.value

        if init_node and getattr(init_node, "line", 0) > 0 and line == 1:
            line = init_node.line

        if var_name and init_node and isinstance(init_node, LiteralNode) and init_node.literal_type == "string":
            if any(kw in var_name for kw in self.PASSWORD_KEYWORDS):
                findings.append(
                    SecurityFinding(
                        rule_id=self.rule_id,
                        vulnerability_name=self.vulnerability_name,
                        description=f"Hardcoded sensitive password assigned to variable '{var_name}'.",
                        severity=self.severity,
                        line=line,
                        column=node.column,
                        code_snippet=f'{var_name} = "{init_node.value}"',
                        recommendation="Store passwords securely using environment variables or a secret vault.",
                    )
                )

        return findings


class HardcodedAPIKeyRule(SecurityRule):
    """SEC002: Detects hardcoded API keys and authentication tokens."""

    rule_id = "SEC002"
    vulnerability_name = "Hardcoded API Key"
    severity = Severity.HIGH

    KEY_KEYWORDS = {"api_key", "apikey", "secret_key", "token", "auth_key", "access_token"}

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        var_name = None
        init_node = None
        line = node.line if getattr(node, "line", 0) > 0 else 1

        if isinstance(node, VariableDeclarationNode):
            var_name = node.var_name.lower()
            init_node = node.initializer
        elif isinstance(node, ConstantDeclarationNode):
            var_name = node.const_name.lower()
            init_node = node.initializer
        elif isinstance(node, AssignmentNode) and isinstance(node.target, IdentifierNode):
            var_name = node.target.name.lower()
            init_node = node.value

        if init_node and getattr(init_node, "line", 0) > 0 and line == 1:
            line = init_node.line

        if var_name and init_node and isinstance(init_node, LiteralNode) and init_node.literal_type == "string":
            if any(kw in var_name for kw in self.KEY_KEYWORDS) or init_node.value.startswith("AIza"):
                findings.append(
                    SecurityFinding(
                        rule_id=self.rule_id,
                        vulnerability_name=self.vulnerability_name,
                        description=f"Hardcoded API key or credential assigned to '{var_name}'.",
                        severity=self.severity,
                        line=line,
                        column=node.column,
                        code_snippet=f'{var_name} = "{init_node.value}"',
                        recommendation="Do not commit API tokens in source code. Use secure secret management APIs.",
                    )
                )

        return findings


class WeakPasswordRule(SecurityRule):
    """SEC003: Flags common weak password string literals."""

    rule_id = "SEC003"
    vulnerability_name = "Weak Password"
    severity = Severity.MEDIUM

    WEAK_PASSWORDS = {"123456", "password", "admin", "12345678", "qwerty", "admin123", "root", "12345"}

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, LiteralNode) and node.literal_type == "string":
            val = str(node.value).lower()
            if val in self.WEAK_PASSWORDS:
                line = node.line if getattr(node, "line", 0) > 0 else 1
                findings.append(
                    SecurityFinding(
                        rule_id=self.rule_id,
                        vulnerability_name=self.vulnerability_name,
                        description=f"Usage of trivially weak password constant '{node.value}'.",
                        severity=self.severity,
                        line=line,
                        column=node.column,
                        code_snippet=f'"{node.value}"',
                        recommendation="Enforce high-entropy password requirements and multi-factor authentication.",
                    )
                )

        return findings


class SQLInjectionRule(SecurityRule):
    """SEC004: Detects dynamic SQL query concatenation passed into db_query()."""

    rule_id = "SEC004"
    vulnerability_name = "Potential SQL Injection"
    severity = Severity.HIGH

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, FunctionCallNode) and node.func_name == "db_query":
            if node.arguments:
                arg = node.arguments[0]
                is_unsafe = False
                snippet = "db_query(...)"

                if isinstance(arg, BinaryExpressionNode) and arg.operator == "+":
                    is_unsafe = True
                    snippet = f"db_query(arg + ...)"
                elif isinstance(arg, IdentifierNode):
                    is_unsafe = True
                    snippet = f"db_query({arg.name})"

                if is_unsafe:
                    line = node.line if getattr(node, "line", 0) > 0 else 1
                    findings.append(
                        SecurityFinding(
                            rule_id=self.rule_id,
                            vulnerability_name=self.vulnerability_name,
                            description="Unsanitized dynamic expression or variable passed to db_query().",
                            severity=self.severity,
                            line=line,
                            column=node.column,
                            code_snippet=snippet,
                            recommendation="Use parameterized prepared statements instead of dynamic SQL string building.",
                        )
                    )

        return findings


class CommandInjectionRule(SecurityRule):
    """SEC005: Detects user-controlled input passed directly to system()."""

    rule_id = "SEC005"
    vulnerability_name = "Potential Command Injection"
    severity = Severity.CRITICAL

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, FunctionCallNode) and node.func_name == "system":
            if node.arguments:
                arg = node.arguments[0]
                # Non-constant system call
                if not (isinstance(arg, LiteralNode) and arg.literal_type == "string"):
                    line = node.line if getattr(node, "line", 0) > 0 else 1
                    findings.append(
                        SecurityFinding(
                            rule_id=self.rule_id,
                            vulnerability_name=self.vulnerability_name,
                            description="Dynamic variable or user input passed into system() command execution.",
                            severity=self.severity,
                            line=line,
                            column=node.column,
                            code_snippet="system(input)",
                            recommendation="Avoid system() execution. Use safe library APIs with strict argument sanitization.",
                        )
                    )

        return findings


class UnsafeGetsRule(SecurityRule):
    """SEC006: Flags calls to the unsafe gets() buffer function."""

    rule_id = "SEC006"
    vulnerability_name = "Unsafe Function Call (gets)"
    severity = Severity.HIGH

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, FunctionCallNode) and node.func_name == "gets":
            line = node.line if getattr(node, "line", 0) > 0 else 1
            findings.append(
                SecurityFinding(
                    rule_id=self.rule_id,
                    vulnerability_name=self.vulnerability_name,
                    description="gets() lacks bounds checking and guarantees stack buffer overflows.",
                    severity=self.severity,
                    line=line,
                    column=node.column,
                    code_snippet="gets(buffer)",
                    recommendation="Replace gets() with bounded input alternatives like fgets().",
                )
            )

        return findings


class UnsafeStrcpyRule(SecurityRule):
    """SEC007: Flags calls to unbounded strcpy()."""

    rule_id = "SEC007"
    vulnerability_name = "Unsafe Function Call (strcpy)"
    severity = Severity.MEDIUM

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, FunctionCallNode) and node.func_name == "strcpy":
            line = node.line if getattr(node, "line", 0) > 0 else 1
            findings.append(
                SecurityFinding(
                    rule_id=self.rule_id,
                    vulnerability_name=self.vulnerability_name,
                    description="strcpy() does not verify destination buffer size, causing buffer overflows.",
                    severity=self.severity,
                    line=line,
                    column=node.column,
                    code_snippet="strcpy(dest, src)",
                    recommendation="Replace strcpy() with strncpy() or snprintf() providing explicit buffer limits.",
                )
            )

        return findings


class UnsafeSprintfRule(SecurityRule):
    """SEC008: Flags calls to sprintf()."""

    rule_id = "SEC008"
    vulnerability_name = "Unsafe Function Call (sprintf)"
    severity = Severity.MEDIUM

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, FunctionCallNode) and node.func_name == "sprintf":
            line = node.line if getattr(node, "line", 0) > 0 else 1
            findings.append(
                SecurityFinding(
                    rule_id=self.rule_id,
                    vulnerability_name=self.vulnerability_name,
                    description="sprintf() formatted string output can exceed destination buffer length.",
                    severity=self.severity,
                    line=line,
                    column=node.column,
                    code_snippet="sprintf(buffer, ...)",
                    recommendation="Use snprintf() to specify buffer capacity limits explicitly.",
                )
            )

        return findings


class WeakRandomRule(SecurityRule):
    """SEC009: Flags use of predictable pseudo-random rand()."""

    rule_id = "SEC009"
    vulnerability_name = "Weak Random Number Generator"
    severity = Severity.LOW

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, FunctionCallNode) and node.func_name == "rand":
            line = node.line if getattr(node, "line", 0) > 0 else 1
            findings.append(
                SecurityFinding(
                    rule_id=self.rule_id,
                    vulnerability_name=self.vulnerability_name,
                    description="rand() produces predictable pseudo-random sequences unsuitable for cryptography.",
                    severity=self.severity,
                    line=line,
                    column=node.column,
                    code_snippet="rand()",
                    recommendation="Use secure_rand() or cryptographically secure PRNGs.",
                )
            )

        return findings


class ResourceLeakRule(SecurityRule):
    """SEC010: Identifies unclosed file handles created by open() without close()."""

    rule_id = "SEC010"
    vulnerability_name = "Resource Leak (Unclosed File)"
    severity = Severity.MEDIUM

    def inspect(self, node: ASTNode, program_root: Optional[ProgramNode] = None) -> List[SecurityFinding]:
        findings: List[SecurityFinding] = []

        if isinstance(node, ProgramNode):
            opened_handles: Set[str] = set()
            closed_handles: Set[str] = set()
            open_nodes: List[ASTNode] = []

            # Sub-walker to inspect program calls
            def walk(curr_node: ASTNode) -> None:
                if isinstance(curr_node, FunctionCallNode):
                    if curr_node.func_name == "open":
                        open_nodes.append(curr_node)
                    elif curr_node.func_name == "close":
                        if curr_node.arguments and isinstance(curr_node.arguments[0], IdentifierNode):
                            closed_handles.add(curr_node.arguments[0].name)
                elif isinstance(curr_node, AssignmentNode):
                    if isinstance(curr_node.value, FunctionCallNode) and curr_node.value.func_name == "open":
                        if isinstance(curr_node.target, IdentifierNode):
                            opened_handles.add(curr_node.target.name)

                # Recursive traversal
                for child_name in dir(curr_node):
                    val = getattr(curr_node, child_name, None)
                    if isinstance(val, ASTNode):
                        walk(val)
                    elif isinstance(val, list):
                        for item in val:
                            if isinstance(item, ASTNode):
                                walk(item)

            walk(node)

            unclosed = opened_handles - closed_handles
            if unclosed or (len(open_nodes) > len(closed_handles) and not opened_handles):
                line = open_nodes[0].line if (open_nodes and getattr(open_nodes[0], "line", 0) > 0) else (node.line if getattr(node, "line", 0) > 0 else 1)
                findings.append(
                    SecurityFinding(
                        rule_id=self.rule_id,
                        vulnerability_name=self.vulnerability_name,
                        description="Resource opened via open() without guaranteed close() handle cleanup.",
                        severity=self.severity,
                        line=line,
                        column=0,
                        code_snippet="open(...)",
                        recommendation="Ensure every opened file descriptor is explicitly released with close().",
                    )
                )

        return findings
