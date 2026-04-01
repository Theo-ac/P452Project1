import streamlit as st
from backend import measure_Circuit
st.title("Theo's 10-Qubit Universal Quantum Computer Simulator")
x = st.slider("How many qubits do you want?", 0, 10, 5)

# --- init state once ---
if "mode" not in st.session_state:
    st.session_state.mode = 0  # 0 for A, 1 for B

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "Option A",
        key="btn_a",
        type="primary" if st.session_state.mode == 0 else "secondary",
    ):
        st.session_state.mode = 0

with col2:
    if st.button(
        "Option B",
        key="btn_b",
        type="primary" if st.session_state.mode == 1 else "secondary",
    ):
        st.session_state.mode = 1

st.write("Selected value:", st.session_state.mode)

