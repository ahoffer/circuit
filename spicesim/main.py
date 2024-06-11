import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Constants
mu_0 = 4 * math.pi * 10 ** -7  # Permeability of free space in T·m/A


def calculate_critical_resistance(L, C):
    return 2 * np.sqrt(L / C)


def calculate_magnetic_field(N, l, I):
    B = (mu_0 * N * I) / l
    return B


def calculate_inductance(turns, area, length):
    L = (mu_0 * turns ** 2 * area) / length
    return L


# Define the control signal for the MOSFET (example: a simple square wave)
def V_GS_func(t):
    seconds_of_power = 0.01  # 5ms
    return 10 if t <= seconds_of_power else 0  # Ensuring a clear on-off state for the MOSFET


# Define the MOSFET behavior using Shockley equations
def mosfet_current(V_GS, V_DS, V_th, k):
    if V_GS <= V_th:
        return 0  # Cutoff region
    elif V_DS < V_GS - V_th:
        return k * ((V_GS - V_th) * V_DS - 0.5 * V_DS ** 2)  # Linear region
    else:
        return 0.5 * k * (V_GS - V_th) ** 2  # Saturation region


# Define the differential equation for the LRC circuit with a MOSFET and flyback diode
def lrc_circuit_with_mosfet_and_diode(y, t, L, R, C, Vth, k, V_GS_func, N, A, l):
    V_circuit, I, Phi = y
    V_GS = V_GS_func(t)
    I_mosfet = mosfet_current(V_GS, V_circuit, Vth, k)

    # Flyback diode parameters
    V_diode_drop = 0.7  # Forward voltage drop of the diode
    if I < 0:  # Diode conducts if the current through the inductor reverses
        I_diode = I
    else:
        I_diode = 0

    # Calculate the magnetic field strength inside the inductor
    B = calculate_magnetic_field(N, l, I)

    # Calculate the rate of change of magnetic flux
    dPhidt = B * A

    dVdt = I
    dIdt = (-R * I - V_circuit / C - I_mosfet - I_diode) / L
    return [dVdt, dIdt, dPhidt]


# Coil parameters
l = 0.07  # 7 cm
dia = 0.05  # 5 cm
A = (0.5 * dia) ** 2 * math.pi
N = 250
L = calculate_inductance(N, A, l)
print(f"L={L:.2e}H Num turns={N} Length={l}m Diameter={dia}m")

# Circuit parameters
C = 1e-3  # Capacitance in Farads
Vth = 5.0  # Threshold voltage for the MOSFET
k = 0.01  # MOSFET transconductance parameter

# Initial conditions: initial voltage and current
V0 = -50.0  # Initial voltage in Volts (set to negative to represent a charged capacitor)
I0 = 0.0  # Initial current in Amperes

# Calculate the critical resistance
R_crit = calculate_critical_resistance(L, C)
print(f"Critical R: {R_crit}")
R = R_crit * 0.5  # Resistance in Ohms

# Time points where solution is computed
t = np.linspace(0, 0.05, 250)

# Solve the differential equations
solution = odeint(lrc_circuit_with_mosfet_and_diode, [V0, I0, 0], t, args=(L, R, C, Vth, k, V_GS_func, N, A, l))
V = solution[:, 0]
I = solution[:, 1]
Phi = solution[:, 2]

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
plt.plot(t, Phi, label='Magnetic Flux (Φ)', color='g')
plt.xlabel('Time (s)')
plt.ylabel('Magnetic Flux (Wb)')
plt.legend()

plt.tight_layout()
plt.show()
