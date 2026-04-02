import streamlit as st
from backend import measure_Circuit, create_Circuit, teleportation, GHZ_Circuit
st.title("Theo's 10-Qubit Universal Quantum Computer Simulator")
n_qubits = st.slider("How many qubits do you want?", 1, 10, 5)

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
option = int(st.session_state.mode)
#st.write("Selected:", st.session_state.mode)
#ghz = GHZ_Circuit(n_qubits)
if st.session_state.mode == 0: 
    if n_qubits >= 3:
        #theta = st.slider("What rotation angle do you want to teleport?", -6.18, 6.18, 0.0, step=0.19625)
        theta = 2*np.arctan(0.5) #solved for with inverse trig for desired state in q2.1
        qc = teleportation(n_qubits, theta)
        st.pyplot(qc.draw("mpl"))
    else:
        st.write("You'll want at least 3 qubits to perform quantum teleportation :]")
else:
    qc = GHZ_Circuit(n_qubits)
    st.pyplot(qc.draw("mpl"))

