import qiskit
import numpy as np
from qiskit import QuantumCircuit, transpile, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram

def GHZ_Circuit(n_qubits):
    qc = QuantumCircuit(n_qubits)

    # Step 1: create superposition on qubit 0
    qc.h(0)
    
    # Step 2: entangle all others with qubit 0
    for i in range(1, n_qubits):
        qc.cx(0, i)
    
    #qc.draw("mpl")
    return qc

def teleportation(n_qubits, theta):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.barrier(label="Bell State Preparation")
    qc.ry(theta, 0)
    sv = Statevector.from_instruction(qc)
    qc.h(1)
    qc.cx(1, n_qubits-1)
    qc.cx(0,1)
    qc.h(0)
    qc.barrier(label="Bell State Measurement")
    qc.measure(1, qc.clbits[1])
    qc.measure(0, qc.clbits[0])
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(n_qubits-1)
    with qc.if_test((qc.clbits[0], 1)):
        qc.z(n_qubits-1)
    qc.ry(theta, n_qubits-1).inverse()
    qc.measure(n_qubits-1, 2)
    qc.draw("mpl")
    return qc, sv

def hop_block(circ, i, j, theta):
    # e^{-i theta (X_i X_j + Y_i Y_j)}
    circ.sdg(i); circ.sdg(j)
    circ.h(i); circ.h(j)
    circ.cx(i, j)
    circ.rz(2*theta, j)
    circ.cx(i, j)
    circ.h(i); circ.h(j)
    circ.s(i); circ.s(j)

def zz_block(circ, i, j, phi):
    # e^{-i phi Z_i Z_j}
    circ.cx(i, j)
    circ.rz(2*phi, j)
    circ.cx(i, j)

def qubit_index(site, spin):
    # spin: 'up' or 'down'
    return 2*site + (0 if spin == 'up' else 1)

def hubbard(n_qubits, U, J, dt):
    n_sites = n_qubits // 2
    qc = QuantumCircuit(n_qubits)

    theta = J * dt      # hopping angle (up to your convention)
    phi   = U * dt / 4  # interaction angle (factor from n_up n_down mapping)

    # 1) Hopping terms: between neighboring sites, for both spins
    for site in range(n_sites - 1):
        # up spin hopping: (site, site+1)
        i_up = qubit_index(site, 'up')
        j_up = qubit_index(site + 1, 'up')
        hop_block(qc, i_up, j_up, theta)

        # down spin hopping: (site, site+1)
        i_dn = qubit_index(site, 'down')
        j_dn = qubit_index(site + 1, 'down')
        hop_block(qc, i_dn, j_dn, theta)

    # 2) On-site interaction terms: U n_{i↑} n_{i↓}
    for site in range(n_sites):
        q_up = qubit_index(site, 'up')
        q_dn = qubit_index(site, 'down')
        zz_block(qc, q_up, q_dn, phi)

    return qc
    
def time_evolve(initial_state, num_qubits, J, U, dt, steps):
    qc = QuantumCircuit(num_qubits)

    # prepare initial state
    qc.append(initial_state.to_instruction(), range(num_qubits))

    # apply Trotter steps
    for _ in range(steps):
        qc.compose(hubbard(num_qubits, J, U, dt), inplace=True)

    return qc
    
def TE_Circuit(initial_state, num_qubits, J, U, dt, steps):
    sim = AerSimulator()
    job = sim.run(time_evolve(initial_state, num_qubits, J, U, dt, steps))
    result = job.result()
    counts = result.get_counts()
    return counts

def probability_vs_Time(initial_state, n_qubits, J, U, dt, max_time, target_state):
    sim = AerSimulator(method="statevector")

    times = np.arange(0, max_time, dt)
    probs = []

    for t in times:
        steps = int(t / dt)

        # build evolution circuit
        qc = QuantumCircuit(n_qubits)
        qc.append(initial_state.to_circuit(), range(n_qubits))

        for _ in range(steps):
            qc.compose(hubbard(n_qubits, J, U, dt), inplace=True)

        # run and get statevector
        state = sim.run(qc).result().get_statevector()

        # probability of target basis state
        index = int(target_state, 2)
        prob = np.abs(state[index])**2
        probs.append(prob)

    return times, probs

def measure_Circuit(circuit):
    sim = AerSimulator()
    tcirc = transpile(circuit, sim)
    result = sim.run(tcirc, shots=1024).result()
    return result.get_counts(tcirc)
