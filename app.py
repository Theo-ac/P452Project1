import streamlit as st
from backend import measure_Circuit
st.title("Theo's 10-Qubit Universal Quantum Computer Simulator")
x = st.slider("Pick a value", 0, 10, 5)
st.write("You picked:", x)
