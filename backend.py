!pip install qiskit-aer --q
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.visualization import plot_histogram
def measure_Circuit(circuit):
    sampler = SamplerV2()
    job = sampler.run([circuit], shots=1024)
    result_ideal = job.result()
    counts_ideal = result_ideal[0].data.meas.get_counts()
    print('Counts(ideal):', counts_ideal)
    return counts_ideal
