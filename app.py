# app.py

import streamlit as st
import sympy
from symbolic_engine import *
from plotting import *

# --- Page Configuration ---
st.set_page_config(
    page_title="Streamlit Maple Calculator",
    page_icon="🍁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar Navigation ---
st.sidebar.title("🍁 Maple-Style Calculator")
app_mode = st.sidebar.selectbox(
    "Choose the calculator mode",
    ["Algebra & Calculus", "Matrix Algebra", "Plotting", "Linear Programming (Coming Soon)"]
)

# --- Main App Logic ---

# --- MODE 1: ALGEBRA & CALCULUS ---
if app_mode == "Algebra & Calculus":
    st.title("Algebra & Calculus Solver")
    
    input_str = st.text_input(
        "Enter your expression or equation:",
        value="x**2 - 4*x + 3"
    )
    
    st.markdown("---")
    st.subheader("Live LaTeX Preview:")
    try:
        st.latex(sympy.latex(parse_expression(input_str)))
    except Exception:
        st.error("Invalid input. Please check your expression.")

    st.markdown("---")
    
    # Operation selection
    operation = st.selectbox(
        "Choose an operation:",
        ["Simplify", "Solve", "Differentiate", "Integrate (Indefinite)", "Integrate (Definite)"]
    )

    if st.button("Calculate"):
        try:
            expr = parse_expression(input_str)
            variables = get_variables_from_expr(expr)
            
            st.subheader("Result")
            
            if operation == "Simplify":
                result = simplify_expression(expr)
                st.latex(f"\\text{{Simplified Expression: }} {sympy.latex(result)}")
                st.markdown(f"**Decimal Approximation:** `{result.evalf()}`")

            elif operation == "Solve":
                if not variables:
                    st.warning("No variable found to solve for.")
                else:
                    var_to_solve = st.selectbox("Solve for which variable?", [str(v) for v in variables])
                    solutions = solve_equation(expr, sympy.Symbol(var_to_solve))
                    st.latex(f"\\text{{Solutions for }} {input_str} = 0 \\text{{ are: }} {sympy.latex(solutions)}")
            
            elif operation == "Differentiate":
                if not variables:
                    st.warning("No variable found to differentiate with respect to.")
                else:
                    var_to_diff = st.selectbox("Differentiate with respect to:", [str(v) for v in variables])
                    derivative = calculate_derivative(expr, sympy.Symbol(var_to_diff))
                    st.latex(f"\\frac{{d}}{{d{var_to_diff}}} \\left( {sympy.latex(expr)} \\right) = {sympy.latex(derivative)}")
                    st.markdown(f"**Simplified Derivative:**")
                    st.latex(sympy.latex(simplify_expression(derivative)))
            
            elif operation == "Integrate (Indefinite)":
                if not variables:
                    st.warning("No variable found to integrate with respect to.")
                else:
                    var_to_int = st.selectbox("Integrate with respect to:", [str(v) for v in variables])
                    integral = calculate_integral(expr, sympy.Symbol(var_to_int))
                    st.latex(f"\\int \\left( {sympy.latex(expr)} \\right) \\, d{var_to_int} = {sympy.latex(integral)} + C")

            elif operation == "Integrate (Definite)":
                 if not variables:
                    st.warning("No variable found to integrate with respect to.")
                 else:
                    var_to_int = st.selectbox("Integrate with respect to:", [str(v) for v in variables])
                    col1, col2 = st.columns(2)
                    with col1:
                        lower_bound = st.text_input("Lower Bound", "0")
                    with col2:
                        upper_bound = st.text_input("Upper Bound", "1")
                    
                    try:
                        lb = float(lower_bound)
                        ub = float(upper_bound)
                        def_integral = calculate_definite_integral(expr, sympy.Symbol(var_to_int), lb, ub)
                        st.latex(f"\\int_{{{lb}}}^{{{ub}}} \\left( {sympy.latex(expr)} \\right) \\, d{var_to_int} = {sympy.latex(def_integral)}")
                        st.markdown(f"**Numerical Value:** `{def_integral.evalf()}`")
                    except ValueError:
                        st.error("Please enter valid numerical bounds.")

        except Exception as e:
            st.error(f"An error occurred: {e}")


# --- MODE 2: MATRIX ALGEBRA ---
elif app_mode == "Matrix Algebra":
    st.title("Matrix Algebra Calculator")
    matrix_input_str = st.text_area(
        "Enter your matrix (e.g., [[1, 2], [3, 4]]):",
        value="[[1, -1], [2, 3]]",
        height=100
    )
    
    st.markdown("---")
    st.subheader("Parsed Matrix Preview:")
    try:
        matrix = parse_matrix(matrix_input_str)
        st.latex(sympy.latex(matrix))
    except Exception as e:
        st.error(f"Invalid matrix format. {e}")

    st.markdown("---")

    matrix_op = st.selectbox(
        "Choose a matrix operation:",
        ["Determinant", "Inverse", "Eigenvalues"]
    )

    if st.button("Calculate Matrix Operation"):
        try:
            matrix = parse_matrix(matrix_input_str)
            if matrix_op == "Determinant":
                det = get_matrix_determinant(matrix)
                st.latex(f"\\text{{Determinant}} = {sympy.latex(det)}")
            elif matrix_op == "Inverse":
                inv = get_matrix_inverse(matrix)
                st.latex(f"\\text{{Inverse}} = {sympy.latex(inv)}")
            elif matrix_op == "Eigenvalues":
                eigenvals = get_matrix_eigenvals(matrix)
                st.write("Eigenvalues and their multiplicities:")
                st.latex(sympy.latex(eigenvals))

        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- MODE 3: PLOTTING ---
elif app_mode == "Plotting":
    st.title("Function Plotter")
    
    plot_dim = st.radio("Select Plot Dimension", ("2D", "3D"))

    if plot_dim == "2D":
        st.header("2D Plot")
        func_str_2d = st.text_input("Enter a function of x (e.g., sin(x) * x):", "sin(x) * exp(-x/5)")
        if func_str_2d:
            try:
                expr = parse_expression(func_str_2d)
                variables = get_variables_from_expr(expr)
                if len(variables) != 1:
                    st.warning("Please enter a function with exactly one variable (e.g., x).")
                else:
                    var = variables[0]
                    fig = plot_2d_function(expr, var)
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not plot. Error: {e}")
    
    elif plot_dim == "3D":
        st.header("3D Plot")
        func_str_3d = st.text_input("Enter a function of x and y (e.g., sin(x**2 + y**2)):", "sin(sqrt(x**2 + y**2))")
        if func_str_3d:
            try:
                expr = parse_expression(func_str_3d)
                variables = get_variables_from_expr(expr)
                if len(variables) != 2:
                    st.warning("Please enter a function with exactly two variables (e.g., x, y).")
                else:
                    var1, var2 = variables
                    fig = plot_3d_function(expr, var1, var2)
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not plot. Error: {e}")
