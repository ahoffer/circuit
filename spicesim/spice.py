import math

import PySpice
import numpy as np
import matplotlib.pyplot as plt
import PySpice.Logging.Logging as Logging

logger = Logging.setup_logging()

from PySpice.Plot.BodeDiagram import bode_diagram
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'

# Define the circuit
circuit = Circuit('Low-Pass RC Filter')

circuit.SinusoidalVoltageSource('input', 'input', circuit.gnd, amplitude=1@u_V)
R1 = circuit.R(1, 'input', 'output', 1@u_kΩ)
C1 = circuit.C(1, 'output', circuit.gnd, 1@u_uF)

# Calculate the break frequency
break_frequency = 1 / (2 * math.pi * float(R1.resistance * C1.capacitance))
print("Break frequency = {:.1f} Hz".format(break_frequency))

# Run the simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.ac(start_frequency=1@u_Hz, stop_frequency=1@u_MHz, number_of_points=10, variation='dec')

# Plot the Bode diagram
figure, axes = plt.subplots(2, figsize=(20, 10))
plt.title("Bode Diagram of a Low-Pass RC Filter")
bode_diagram(axes=axes,
             frequency=analysis.frequency,
             gain=20*np.log10(np.absolute(analysis.output)),
             phase=np.angle(analysis.output, deg=False),
             marker='.',
             color='blue',
             linestyle='-',
)
for ax in axes:
    ax.axvline(x=break_frequency, color='red')

plt.tight_layout()
plt.show()
