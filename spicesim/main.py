import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the MOSFET gate charge dynamics
def gate_charge(V_gate, V_control, R_g, C_g):
    I_g = (V_control - V_gate) / R_g
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
def lrc_circuit_with_mosfet(y, t, L, R, C, Vth, k, R_g, C_g, V_control_func, R_DS_on, R_L):
    V, I, V_gate, P_mosfet, P_inductor = y
    V_control = V_control_func(t)
    dV_gate_dt = gate_charge(V_gate, V_control, R_g, C_g)
    I_mosfet = mosfet_current(V_gate, V, Vth, k)
    dVdt = I
    dIdt = (-R * I - V / C - I_mosfet) / L
    P_conduction_mosfet = I_mosfet**2 * R_DS_on
    P_inductor = I**2 * R_L
    P_total_mosfet = P_conduction_mosfet  # Approximate for now, add switching losses if needed
    return [dVdt, dIdt, dV_gate_dt, P_total_mosfet, P_inductor]

# Circuit parameters
L = 1.0  # Inductance in Henry
C = 1e-3  # Capacitance in Farads
Vth = 5.0  # Threshold voltage for the MOSFET
k = 0.01  # MOSFET transconductance parameter
R_g = 100  # Gate resistor in Ohms
C_g = 1e-9  # Gate capacitance in Farads
R_DS_on = 0.05  # MOSFET on-resistance in Ohms
R_L = 0.1  # Inductor internal resistance in Ohms

# Initial conditions: initial voltage, current, gate voltage, and power dissipation
V0 = -50.0  # Initial voltage in Volts
I0 = 0.0  # Initial current in Amperes
V_gate0 = 0.0  # Initial gate voltage in Volts
P_mosfet0 = 0.0  # Initial MOSFET power dissipation
P_inductor0 = 0.0  # Initial inductor power dissipation

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
solution = odeint(lrc_circuit_with_mosfet, [V0, I0, V_gate0, P_mosfet0, P_inductor0], t, args=(L, R, C, Vth, k, R_g, C_g, control_signal, R_DS_on, R_L))
V = solution[:, 0]
I = solution[:, 1]
V_gate = solution[:, 2]
P_mosfet = solution[:, 3]
P_inductor = solution[:, 4]

# Calculate the control signal over time
V_control_values = [control_signal(time) for time in t]

# Calculate total heat energy produced
heat_energy_mosfet = np.trapz(P_mosfet, t)  # Integrate power over time to get energy
heat_energy_inductor = np.trapz(P_inductor, t)  # Integrate power over time to get energy
total_heat_energy = heat_energy_mosfet + heat_energy_inductor
initial_energy = 0.5 * C * V0**2
efficiency = (initial_energy-total_heat_energy)/initial_energy

print(f"Total heat energy produced by the MOSFET: {heat_energy_mosfet:.3f} J")
print(f"Total heat energy produced by the inductor: {heat_energy_inductor:.3f} J")
print(f"Total heat energy produced in the system: {total_heat_energy:.3f} J")
print(f"Initial energy in the system: {initial_energy:.3f} J")
print(f"Efficiency: {efficiency:.2f}%")

# Plot the results
fig, axs = plt.subplots(5, 1, figsize=(10, 15))
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

axs[3].plot(t, P_mosfet, label='MOSFET Power Dissipation (P_mosfet)', color='m')
axs[3].set_xlabel('Time (s)')
axs[3].set_ylabel('Power (W)')
axs[3].legend()
axs[3].grid(True)

axs[4].plot(t, P_inductor, label='Inductor Power Dissipation (P_inductor)', color='c')
axs[4].set_xlabel('Time (s)')
axs[4].set_ylabel('Power (W)')
axs[4].legend()
axs[4].grid(True)

plt.show()
