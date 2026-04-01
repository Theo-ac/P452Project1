import qiskit
from qiskit import QuantumCircuit, transpile
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
def create_Circuit(n_qubits, type):
    if type == 0:
        return teleportation(n_qubits)
    else: 
        return hubbard(n_qubits)
def measure_Circuit(circuit):
    sampler = SamplerV2()
    job = sampler.run([circuit], shots=1024)
    result_ideal = job.result()
    counts_ideal = result_ideal[0].data.meas.get_counts()
    print('Counts(ideal):', counts_ideal)
    return counts_ideal
