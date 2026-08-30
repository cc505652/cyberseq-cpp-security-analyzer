"""
Type Checker & Type Compatibility Engine for Tiny C Compiler.

Provides type checking rules, operator result type inference, and assignability validation
for primitive Tiny C types (int, float, char, string, bool, void).
"""

from typing import Optional


class TypeChecker:
    """Utility class evaluating type compatibility and expression result types."""

    # Primitive types supported in Tiny C
    PRIMITIVE_TYPES = {"int", "float", "char", "string", "bool", "void"}

    @staticmethod
    def is_valid_type(type_name: str) -> bool:
        """Checks if type name is a recognized primitive type."""
        return type_name in TypeChecker.PRIMITIVE_TYPES

    @staticmethod
    def is_assignable(target_type: str, value_type: str) -> bool:
        """Determines if value_type can be assigned to target_type."""
        if target_type == value_type:
            return True
        # Implicit conversion: int can be assigned to float
        if target_type == "float" and value_type == "int":
            return True
        return False

    @staticmethod
    def is_condition_valid(cond_type: str) -> bool:
        """Checks if an expression type can serve as a boolean condition (bool, int, float)."""
        return cond_type in {"bool", "int", "float"}

    @staticmethod
    def get_binary_result_type(operator: str, left_type: str, right_type: str) -> Optional[str]:
        """Infers the resulting expression type for binary operations."""
        # Comparison operators (==, !=, <, >, <=, >=) return bool
        if operator in {"==", "!=", "<", ">", "<=", ">="}:
            if left_type in {"int", "float"} and right_type in {"int", "float"}:
                return "bool"
            if left_type == right_type:
                return "bool"
            return None

        # Logical operators (&&, ||) return bool
        if operator in {"&&", "||"}:
            if TypeChecker.is_condition_valid(left_type) and TypeChecker.is_condition_valid(right_type):
                return "bool"
            return None

        # Arithmetic operators (+, -, *, /, %)
        if operator in {"+", "-", "*", "/", "%"}:
            if left_type == "int" and right_type == "int":
                return "int"
            if (left_type in {"int", "float"}) and (right_type in {"int", "float"}):
                return "float"
            if operator == "+" and left_type == "string" and right_type == "string":
                return "string"
            return None

        return None

    @staticmethod
    def get_unary_result_type(operator: str, operand_type: str) -> Optional[str]:
        """Infers the resulting expression type for unary operations."""
        if operator == "!":
            if TypeChecker.is_condition_valid(operand_type):
                return "bool"
            return None
        if operator in {"-", "++", "--"}:
            if operand_type in {"int", "float"}:
                return operand_type
            return None
        return None
