import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def calculate_critical_resistance(L, C):
    return 2 * np.sqrt(L / C)

# Define the control signal for the MOSFET (example: a simple square wave)
def control_signal(t):
    # period = 2.0
    # return 1.0 if (t % period) < (period / 2) else 0.0\
    seconds_of_power = 0.1 # 5ms
    return t <= seconds_of_power

# Define the differential equation for the LRC circuit with a MOSFET
def lrc_circuit_with_mosfet(y, t, L, R, C, Vth, control):
    V, I = y
    # Control signal to turn MOSFET on or off (1 for on, 0 for off)
    mosfet_on = 1 if control(t) > Vth else 0
    dVdt = I
    dIdt = (-R * I - V / C) / L if mosfet_on else 0
    return [dVdt, dIdt]

# Circuit parameters
L = 1.0  # Inductance in Henry
C = 1e-3  # Capacitance in Farads
Vth = 0.5  # Threshold voltage for the MOSFET

# Initial conditions: initial voltage and current
V0 = -50.0  # Initial voltage in Volts
I0 = 0.0  # Initial current in Amperes

# Calculate the natural frequency and damping ratio
R_crit = calculate_critical_resistance(L, C)
print(f"Critical R: {R_crit}")
R = R_crit * 0.6  # Resistance in Ohms

# Time points where solution is computed
t = np.linspace(0, 1, 100)

# Solve the differential equations
solution = odeint(lrc_circuit_with_mosfet, [V0, I0], t, args=(L, R, C, Vth, control_signal))
V = solution[:, 0]
I = solution[:, 1]

# Calculate the control signal over time
V_GS_values = [control_signal(time) for time in t]

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
