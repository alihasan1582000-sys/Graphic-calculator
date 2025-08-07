# plotting.py

import plotly.graph_objects as go
import numpy as np
import sympy

def plot_2d_function(expr, var):
    """Generates an interactive 2D plot of a function using Plotly."""
    
    # Use lambdify to convert the sympy expression to a numerical function
    f = sympy.lambdify(var, expr, 'numpy')
    
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f(x_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name=str(expr)))
    
    fig.update_layout(
        title=f'2D Plot of y = {sympy.latex(expr)}',
        xaxis_title=str(var),
        yaxis_title='y',
        template='plotly_white',
        height=500
    )
    fig.update_xaxes(gridcolor='lightgrey')
    fig.update_yaxes(gridcolor='lightgrey')
    
    return fig

def plot_3d_function(expr, var1, var2):
    """Generates an interactive 3D plot of a function using Plotly."""
    f = sympy.lambdify((var1, var2), expr, 'numpy')
    
    x_vals = np.linspace(-10, 10, 50)
    y_vals = np.linspace(-10, 10, 50)
    x_grid, y_grid = np.meshgrid(x_vals, y_vals)
    z_grid = f(x_grid, y_grid)
    
    fig = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid)])
    
    fig.update_layout(
        title=f'3D Plot of z = {sympy.latex(expr)}',
        scene=dict(
            xaxis_title=str(var1),
            yaxis_title=str(var2),
            zaxis_title='z'
        ),
        height=600
    )
    return fig
