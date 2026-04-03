import streamlit as st
import numpy as np
from backend import measure_Circuit, teleportation, hubbard, GHZ_Circuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
st.title("Theo's 10-Qubit Universal Quantum Computer Simulator")
n_qubits = st.slider("How many qubits do you want?", 1, 10, 5)
theta = 0.0

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
if option == 0: 
    if n_qubits >= 3:
        theta = st.slider("What rotation angle do you want to teleport?", -2*np.pi, 2*np.pi, 0.0, step=np.pi/16)
        #theta = 2*np.arctan(0.5) #solved for with inverse trig for desired state in q2.1
        qc, sv = teleportation(n_qubits, theta)
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.write("Your secret qubit:")
        for idx, amp in enumerate(sv.data):
            if abs(amp) > 0:   # or > 1e-12 for numerical noise
                bitstring = format(idx, f"0{sv.num_qubits}b")
                if idx == 0:
                    with col2:
                        st.write(amp,"|0⟩")
                else: 
                    with col3:
                        st.write(amp,"|1⟩")
        st.pyplot(qc.draw("mpl"))
        counts = measure_Circuit(qc)
        all_states = [format(i, f"0{n_qubits}b") for i in range(2**n_qubits)]
        full_counts = {state: counts.get(state, 0) for state in all_states}
        trimmed_counts = counts = {k: v for k, v in full_counts.items() if v != 0}
        st.pyplot(plot_histogram(trimmed_counts))
        st.write("***Only plotting non-zero counts***")
    else:
        st.write("You'll want at least 3 qubits to perform quantum teleportation :]")
else:
    if n_qubits%2 == 0:
        initial_state = Statevector.from_label("0001")
        U = st.slider("What interaction scaling U do you want?", 0, 10, 1)
        J = st.slider("What kinetic energy scaling J do you want?", 0, 10, 1)
        qc = hubbard(n_qubits, U, J, 1)
        st.pyplot(qc.draw("mpl"))
    else:
        st.write("You'll want an even number of qubits to simulate the Fermi-Hubbard Model :]")


