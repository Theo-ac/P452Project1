import qiskit
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
    qc.measure(1, 1)
    qc.measure(0, 0)
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(n_qubits-1)
    with qc.if_test((qc.clbits[0], 1)):
        qc.z(n_qubits-1)
    qc.ry(theta, n_qubits-1).inverse()
    qc.measure(n_qubits-1, 2)
    qc.draw("mpl")
    return qc, sv
    
def hubbard(n_qubits):
    return qc
    
def create_Circuit(n_qubits, theta, mode):
    if mode == 0:
        qc, _sv = teleportation(n_qubits, theta)
        return qc
    else: 
        return hubbard(n_qubits)
def measure_Circuit(circuit):
    sim = AerSimulator()
    tcirc = transpile(circuit, sim)
    result = sim.run(tcirc, shots=1024).result()
    return result.get_counts(tcirc)
