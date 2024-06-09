import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint


# This model does not account for rise and fall of the switch used to supply the gate voltage

# Define the MOSFET gate charge dynamics
def gate_charge(V_gate, V_control, R_g, C_g, t):
    # Calculate the current through the gate resistor
    I_g = (V_control - V_gate) / R_g
    # Voltage change rate across the gate capacitance
    dV_gate_dt = I_g / C_g
    return dV_gate_dt


def calculate_critical_resistance(L, C):
    return 2 * np.sqrt(L / C)


# Define the control signal for the MOSFET (example: a simple square wave)
def control_signal(t):
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
def lrc_circuit_with_mosfet(y, t, L, R, C_power, Vth, k, R_g, C_g, V_control_func):
    V_circuit, I, V_gate = y
    V_control = V_control_func(t)
    # Update gate voltage considering the gate charge dynamics
    dV_gate_dt = gate_charge(V_gate, V_control, R_g, C_g, t)
    I_mosfet = mosfet_current(V_gate, V_circuit, Vth, k)
    dVdt = I
    dIdt = (-R * I - V_circuit / C_power - I_mosfet) / L
    return [dVdt, dIdt, dV_gate_dt]


# Circuit parameters
L = 1.0  # Inductance in Henry
C = 1e-3  # Capacitance in Farads
Vth = 5.0  # Threshold voltage for the MOSFET
k = 0.01  # MOSFET transconductance parameter
R_g = 10  # Gate resistor in Ohms
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
t = np.linspace(0, .2, 100)

# Solve the differential equations
solution = odeint(lrc_circuit_with_mosfet, [V0, I0, V_gate0], t, args=(L, R, C, Vth, k, R_g, C_g, control_signal))
V = solution[:, 0]
I = solution[:, 1]
V_gate = solution[:, 2]

# Calculate the control signal over time
V_control_values = [control_signal(time) for time in t]

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

plt.subplot(4, 1, 3)
plt.plot(t, V_gate, label='Gate Voltage (V_gate)', color='g')
plt.xlabel('Time (s)')
plt.ylabel('Gate Voltage (V)')
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(t, V_control_values, label='Control Signal (V_control)', color='b')
plt.xlabel('Time (s)')
plt.ylabel('Control Signal (V)')
plt.legend()

plt.tight_layout()
plt.show()
