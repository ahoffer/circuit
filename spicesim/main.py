import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the MOSFET gate charge dynamics
def gate_charge(V_gate, V_control, R_g, C_g):
    # Calculate the current through the gate resistor
    I_g = (V_control - V_gate) / R_g
    # Voltage change rate across the gate capacitance
    dV_gate_dt = I_g / C_g
    return dV_gate_dt

def calculate_critical_resistance(L, C):
    return 2 * np.sqrt(L / C)

# Define the MOSFET behavior using Shockley equations with gate voltage dynamics
def mosfet_current(V_GS, V_DS, V_th, k):
    if V_GS <= V_th:
        return 0  # Cutoff region
    elif V_DS < V_GS - V_th:
        return k * ((V_GS - V_th) * V_DS - 0.5 * V_DS ** 2)  # Linear region
    else:
        return 0.5 * k * (V_GS - V_th) ** 2  # Saturation region

# Define the differential equation for the LRC circuit with a realistic MOSFET
def lrc_circuit_with_mosfet(y, t, L, R, C, Vth, k, R_g, C_g, V_control_func):
    V, I, V_gate = y
    V_control = V_control_func(t)
    # Update gate voltage considering the gate charge dynamics
    dV_gate_dt = gate_charge(V_gate, V_control, R_g, C_g)
    I_mosfet = mosfet_current(V_gate, V, Vth, k)
    dVdt = I
    dIdt = (-R * I - V / C - I_mosfet) / L
    return [dVdt, dIdt, dV_gate_dt]

# Circuit parameters
L = 1.0  # Inductance in Henry
C = 1e-3  # Capacitance in Farads
Vth = 5.0  # Threshold voltage for the MOSFET
k = 0.01  # MOSFET transconductance parameter
R_g = 100  # Gate resistor in Ohms (increased to better observe charging effects)
C_g = 1e-9  # Gate capacitance in Farads

# Initial conditions: initial voltage, current, and gate voltage
V0 = -50.0  # Initial voltage in Volts
I0 = 0.0  # Initial current in Amperes
V_gate0 = 0.0  # Initial gate voltage in Volts

# Calculate the natural frequency and damping ratio
R_crit = calculate_critical_resistance(L, C)
print(f"Critical R: {R_crit}")
R = R_crit * 0.6  # Resistance in Ohms

# Time points where solution is computed
t = np.linspace(0, 0.2, 1000)

# Define the control signal for the MOSFET (example: a simple square wave)
def control_signal(t):
    seconds_of_power = 0.05  # 5ms
    return 10.0 if t <= seconds_of_power else 0.0

# Solve the differential equations
solution = odeint(lrc_circuit_with_mosfet, [V0, I0, V_gate0], t, args=(L, R, C, Vth, k, R_g, C_g, control_signal))
V = solution[:, 0]
I = solution[:, 1]
V_gate = solution[:, 2]

# Calculate the control signal over time
V_control_values = [control_signal(time) for time in t]

# Plot the results
fig, axs = plt.subplots(4, 1, figsize=(10, 12))
fig.tight_layout(pad=4.0)

axs[0].plot(t, V, label='Voltage (V)')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Voltage (V)')
axs[0].legend()
axs[0].grid(True)

axs[1].plot(t, I, label='Current (I)', color='r')
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Current (A)')
axs[1].legend()
axs[1].grid(True)

axs[2].plot(t, V_gate, label='Gate Voltage (V_gate)', color='g')
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Gate Voltage (V)')
axs[2].legend()
axs[2].grid(True)

axs[3].plot(t, V_control_values, label='Control Signal (V_control)', color='b')
axs[3].set_xlabel('Time (s)')
axs[3].set_ylabel('Control Signal (V)')
axs[3].legend()
axs[3].grid(True)

plt.show()
