import matplotlib.pyplot as plt
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Define the circuit
circuit = Circuit('LRC Circuit')

# Add components
circuit.C(1, 'n1', circuit.gnd, 10@u_F)  # 10µF capacitor
circuit.L(1, 'n1', 'n2', 100@u_H)        # 100µH inductor
circuit.R(1, 'n2', circuit.gnd, 10@u_Ohm) # 10 Ohm resistor
circuit.V(1, 'gate', circuit.gnd, 5@u_V)    # Gate voltage for MOSFET

# Add a MOSFET model definition directly in the circuit
circuit.model('nmos', 'NMOS', Vto=2.0, Kp=1e-3)
circuit.M(1, 'n2', 'gate', circuit.gnd, circuit.gnd, model='nmos')  # Power MOSFET

# Add initial conditions
circuit.initial_conditions['n1'] = 100@u_V  # Initial capacitor voltage

# Define the simulation parameters
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1@u_s, end_time=1@m_s)

# Plot the results
fig, ax = plt.subplots()
plot(analysis['n1'], axis=ax)
ax.grid()
plt.title('LRC Circuit with Capacitor Discharge through MOSFET')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.show()
