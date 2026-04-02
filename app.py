import streamlit as st
from backend import measure_Circuit, create_Circuit, teleportation, GHZ_Circuit
st.title("Theo's 10-Qubit Universal Quantum Computer Simulator")
n_qubits = st.slider("How many qubits do you want?", 0, 10, 5)

# --- init state once ---
if "mode" not in st.session_state:
    st.session_state.mode = 0  # 0 for A, 1 for B

col1, col2 = st.columns(2)

import streamlit as st

# Initialize once
if "mode" not in st.session_state:
    st.session_state.mode = 0

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "Teleportation Circuit",
        key="toggle_a",
        type="primary" if st.session_state.mode == 0 else "secondary",
    ):
        st.session_state.mode = 0
        st.rerun()

with col2:
    if st.button(
        "Hubbard Circuit",
        key="toggle_b",
        type="primary" if st.session_state.mode == 1 else "secondary",
    ):
        st.session_state.mode = 1
        st.rerun()

#st.write("Selected:", st.session_state.mode)
#ghz = GHZ_Circuit(n_qubits)
if n_qubits >= 3: 
    qc = create_Circuit(n_qubits, st.session_state_mode)
else:
    qc = GHZ_Circuit(n_qubits)
st.pyplot(qc.draw("mpl"))

