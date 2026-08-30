"""
AST Diagram Visualizer for Tiny C Compiler.

Generates Graphviz DOT script strings and Mermaid diagram flowcharts
from Abstract Syntax Tree structures.
"""

from typing import List, Tuple
from compiler.ast_nodes import ASTNode
from compiler.ast_printer import ASTPrinter


class ASTVisualizer:
    """Generates Graphviz DOT and Mermaid visual diagram specifications for AST trees."""

    def __init__(self) -> None:
        self.node_count: int = 0
        self.printer: ASTPrinter = ASTPrinter()

    def generate_dot(self, root: ASTNode) -> str:
        """Generates Graphviz DOT language representation of AST."""
        self.node_count = 0
        lines = [
            'digraph AST {',
            '    node [shape=box, style="filled,rounded", fillcolor="#EBF3FA", fontname="Helvetica"];',
            '    edge [fontname="Helvetica", fontsize=10];',
        ]
        self._build_dot_nodes(root, lines)
        lines.append('}')
        return "\n".join(lines)

    def _build_dot_nodes(self, node: ASTNode, lines: List[str]) -> int:
        self.node_count += 1
        current_id = self.node_count
        label = node.accept(self.printer).replace('"', '\\"')

        # Custom fill colors for node types
        fillcolor = "#EBF3FA"
        if "Decl" in label:
            fillcolor = "#D4EDDA"
        elif "Expr" in label or "Literal" in label:
            fillcolor = "#FFF3CD"
        elif "FunctionCall" in label:
            fillcolor = "#F8D7DA"

        lines.append(f'    node_{current_id} [label="{label}", fillcolor="{fillcolor}"];')

        children = self.printer._get_children(node)
        for child in children:
            child_id = self._build_dot_nodes(child, lines)
            lines.append(f'    node_{current_id} -> node_{child_id};')

        return current_id

    def generate_mermaid(self, root: ASTNode) -> str:
        """Generates Mermaid flowchart diagram representation of AST."""
        self.node_count = 0
        lines = ["graph TD;"]
        self._build_mermaid_nodes(root, lines)
        return "\n".join(lines)

    def _build_mermaid_nodes(self, node: ASTNode, lines: List[str]) -> str:
        self.node_count += 1
        current_id = f"node_{self.node_count}"
        label = node.accept(self.printer).replace('"', "'")

        lines.append(f'    {current_id}["{label}"];')

        children = self.printer._get_children(node)
        for child in children:
            child_id = self._build_mermaid_nodes(child, lines)
            lines.append(f'    {current_id} --> {child_id};')

        return current_id
