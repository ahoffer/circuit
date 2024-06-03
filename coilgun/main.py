import matplotlib.pyplot as plt
from ipywidgets import Layout, interact, FloatSlider, FloatLogSlider, IntSlider
from plot_circuit import plot_circuit
from plot_position import plot_position
from basic_plot import basic_plot
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, FloatLogSlider, IntSlider
from scipy.integrate import solve_ivp, cumulative_trapezoid
import numpy as np
from collections import namedtuple
from interactive_plot import start

mu_0 = 4 * np.pi * 1e-7  # Permeability of free space in T·m/A

# Projectile properties
proj_diameter = 0.005  # Diameter in meters
proj_length = 0.010  # Length in meters
iron_density = 7870  # Density of iron in kg/m^3




# Define the differential equation for the RLC circuit
def circuit_model(t, y, params):
    # Destructure the state vector
    [voltage, current] = y

    # Rate of change in voltage
    dVdt = current / params.capacitance

    # Rate of change in current   # Compute inductance, L
    coil_area = np.pi * (params.coil_diameter / 2) ** 2  # Coil cross-section, in m^2
    L = (params.num_turns ** 2 * mu_0 * coil_area) / params.coil_length  # Inductance in Henrys
    dIdt = -(params.resistance * current + voltage) / L

    # if count % 100 == 0:
    #     print(f't={t:.1e} I={current:.1e} B={B:.1e} F={F:.1e} a={a:.1e} ')
    return [dVdt, dIdt]


def force_model(output, params):
    B_vals = []
    F_vals = []
    a_vals = []
    v_vals = []
    turns_density = params.num_turns / params.coil_length
    chi_iron = 1000
    slug_volume = np.pi * (params.slug_diameter / 2) ** 2 * params.slug_length  # Volume in cubic meters
    slug_mass = iron_density * slug_volume  # Mass in kg
    for idx in range(0, output['time'].size):

        # Ideally, we want to make the length of the coil such that all its energy is expended when the
        # projectile is in the middle of the coil. But for now, just set the the magnetic field to zero
        # when the projectile is 1/2 way through the coil

        B = mu_0 * turns_density * output['current'][idx]
        F = (chi_iron * B ** 2 * slug_volume) / (2 * mu_0 * (1 + chi_iron) ** 2)
        a = F / slug_mass

        v = 0
        if (idx > 0):
            v = (output['time'][idx] - output['time'][idx - 1]) / 2 * (a_vals[idx - 1] + a)
        B_vals.append(B)
        F_vals.append(F)
        a_vals.append(a)
        v_vals.append(v)
        # print(f'a={a:.6f}')
    return {'mag_field': np.array(B_vals),
            'force': np.array(F_vals),
            'acceleration': np.array(a_vals),
            'velocity': np.array(v_vals)}


time_step = 1e-6  # seconds






    output = run_sim(simulationParameters)
    # plot_circuit(output)
    plot_kinematics(output)
    # plot_position(output)
    basic_plot(output['time'], "time", output['v2'], "my velocity")


start(solve_and_plot)
