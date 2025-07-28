import streamlit as st
from sympy import symbols, Eq, solve, sympify
from sympy.solvers import solve as sym_solve
from sympy.calculus.util import continuous_domain

st.set_page_config(page_title="Math Problem Solver", layout="centered")

st.title("🧮 Math Problem Solver")
st.markdown("Enter a math equation or expression to get step-by-step solutions.")

# Input area
user_input = st.text_input("Enter your equation (e.g., x + 2 = 5):")

if user_input:
    try:
        st.subheader("📘 Parsed Expression:")
        st.code(user_input)

        # Extract symbol
        x = symbols('x')

        # Try to split equation
        if '=' in user_input:
            lhs, rhs = user_input.split('=')
            eq = Eq(sympify(lhs), sympify(rhs))

            st.subheader("✅ Solving Equation:")
            st.latex(eq)

            solution = solve(eq, x)
            st.success(f"Solution: {solution}")
        else:
            expr = sympify(user_input)
            st.subheader("📐 Simplified Expression:")
            st.latex(expr)
            st.write(f"Evaluated Result: {expr.evalf()}")

    except Exception as e:
        st.error(f"❌ Error parsing or solving equation: {e}")

st.markdown("---")
st.caption("Built with 🧠 [SymPy](https://www.sympy.org/) and Streamlit.")
