# symbolic_engine.py

import sympy
from sympy.parsing.sympy_parser import parse_expr
import numpy as np

# --- Helper Functions ---

def parse_expression(expr_str: str):
    """Safely parse a string into a SymPy expression."""
    try:
        # Use a local dict with common math functions for parsing
        local_dict = {
            "sin": sympy.sin,
            "cos": sympy.cos,
            "tan": sympy.tan,
            "exp": sympy.exp,
            "sqrt": sympy.sqrt,
            "ln": sympy.log,
            "log": sympy.log,
        }
        return parse_expr(expr_str, local_dict=local_dict)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

def get_variables_from_expr(expr):
    """Extract variables (symbols) from a SymPy expression."""
    return list(expr.free_symbols)

# --- Core Operations ---

def simplify_expression(expr):
    """Simplifies a SymPy expression."""
    return sympy.simplify(expr)

def solve_equation(expr, var):
    """Solves an equation for a given variable."""
    try:
        return sympy.solve(expr, var)
    except Exception as e:
        # Handle cases where solve can't find a solution
        return f"Could not solve the equation: {e}"

def calculate_derivative(expr, var):
    """Calculates the derivative of an expression with respect to a variable."""
    return sympy.diff(expr, var)

def calculate_integral(expr, var):
    """Calculates the indefinite integral of an expression."""
    return sympy.integrate(expr, var)

def calculate_definite_integral(expr, var, lower_bound, upper_bound):
    """Calculates the definite integral."""
    return sympy.integrate(expr, (var, lower_bound, upper_bound))

# --- Matrix Operations ---
def parse_matrix(matrix_str: str):
    """Parses a string representation of a matrix into a SymPy Matrix."""
    try:
        # A bit of a hack to safely evaluate a string list of lists
        import ast
        matrix_list = ast.literal_eval(matrix_str)
        return sympy.Matrix(matrix_list)
    except Exception as e:
        raise ValueError(f"Invalid matrix format. Use format like [[1, 2], [3, 4]]. Error: {e}")

def get_matrix_determinant(matrix):
    return matrix.det()

def get_matrix_inverse(matrix):
    if not matrix.is_square:
        return "Matrix must be square to have an inverse."
    if matrix.det() == 0:
        return "Matrix is singular and has no inverse."
    return matrix.inv()

def get_matrix_eigenvals(matrix):
    if not matrix.is_square:
        return "Matrix must be square to have eigenvalues."
    return matrix.eigenvals()
