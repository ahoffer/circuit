import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the differential equation for the RL circuit
def rl_circuit(y, t, L, R):
    I = y
    dIdt = - (R / L) * I
    return dIdt

# Parameters
L = 0.1  # Inductance in henries
R = 10  # Resistance in ohms

# Initial conditions: initial current
I0 = 1.0  # Initial current in Amperes

# Time points where solution is computed
t = np.linspace(0, 1, 1000)  # simulate for 1 second

# Solve the differential equation
I = odeint(rl_circuit, I0, t, args=(L, R))

# Calculate the voltage across the inductor
V_L = L * np.gradient(I[:,0], t)

# Plot the results
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, I, label='Current (I)')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, V_L, label='Voltage (V_L)', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()

plt.tight_layout()
plt.show()
