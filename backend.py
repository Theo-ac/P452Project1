import qiskit
from qiskit import QuantumCircuit, transpile, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
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
    qc.h(1)
    qc.cx(1, n_qubits-1)
    qc.barrier()
    qc.ry(theta, 0)
    qc.barrier()
    qc.cx(0,1)
    qc.h(0)
    qc.barrier()
    qc.measure(1, 1)
    qc.measure(0, 0)
    with qc.if_test((qc.clbits[1], 1)):
        qc.x(2)
    with qc.if_test((qc.clbits[0], 1)):
        qc.z(2)
    qc.ry(-theta, 2)
    qc.measure(2, 2)
    qc.draw("mpl")
    return qc
    
def hubbard(n_qubits):
    return qc
    
def create_Circuit(n_qubits, theta, type):
    if type == 0:
        return teleportation(n_qubits, theta)
    else: 
        return hubbard(n_qubits)
def measure_Circuit(circuit):
    sampler = SamplerV2()
    job = sampler.run([circuit], shots=1024)
    result_ideal = job.result()
    counts_ideal = result_ideal[0].data.meas.get_counts()
    print('Counts(ideal):', counts_ideal)
    return counts_ideal
