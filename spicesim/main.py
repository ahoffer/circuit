import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint


# This model does not account for rise and fall times of the MOSFET,
# or the rise time of the switch used to supply the gate voltage


def calculate_critical_resistance(L, C):
    return 2 * np.sqrt(L / C)


# Define the control signal for the MOSFET (example: a simple square wave)
def V_GS_func(t):
    # period = 2.0
    # return 1.0 if (t % period) < (period / 2) else 0.0\
    seconds_of_power = 0.05  # 5ms
    return t <= seconds_of_power


# Define the MOSFET behavior using Shockley equations
def mosfet_current(V_GS, V_DS, V_th, k):
    if V_GS <= V_th:
        return 0  # Cutoff region
    elif V_DS < V_GS - V_th:
        return k * ((V_GS - V_th) * V_DS - 0.5 * V_DS ** 2)  # Linear region
    else:
        return 0.5 * k * (V_GS - V_th) ** 2  # Saturation region


# Define the differential equation for the LRC circuit with a MOSFET
def lrc_circuit_with_mosfet(y, t, L, R, C, Vth, k, V_GS_func):
    V_circuit, I = y
    V_GS = V_GS_func(t)
    I_mosfet = mosfet_current(V_GS, V_circuit, Vth, k)
    dVdt = I
    dIdt = (-R * I - V_circuit / C - I_mosfet) / L
    return [dVdt, dIdt]


# Circuit parameters
L = 1.0  # Inductance in Henry
C = 1e-3  # Capacitance in Farads
Vth = 2.0  # Threshold voltage for the MOSFET
k = 0.01  # MOSFET transconductance parameter

# Initial conditions: initial voltage and current
V0 = -50.0  # Initial voltage in Volts
I0 = 0.0  # Initial current in Amperes

# Calculate the natural frequency and damping ratio
R_crit = calculate_critical_resistance(L, C)
print(f"Critical R: {R_crit}")
R = R_crit * 0.6  # Resistance in Ohms

# Time points where solution is computed
t = np.linspace(0, .2, 100)

# Solve the differential equations
solution = odeint(lrc_circuit_with_mosfet, [V0, I0], t, args=(L, R, C, Vth, k, V_GS_func))
V = solution[:, 0]
I = solution[:, 1]

# Calculate the control signal over time
V_GS_values = [V_GS_func(time) for time in t]

# Plot the results
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(t, V, label='Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, I, label='Current (I)', color='r')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, V_GS_values, label='Control Signal (V_GS)', color='b')
plt.xlabel('Time (s)')
plt.ylabel('Control Signal (V)')
plt.legend()

plt.tight_layout()
plt.show()
