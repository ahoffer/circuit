import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, FloatLogSlider, IntSlider

def plot_circuit(time, velocity, acceleration, voltage, current):
    plt.figure(figsize=(8, 4))
    plt.plot(time, current, 'r', label='Current (A)')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.title('Current vs. Time')
    plt.grid(True)
    plt.tick_params(axis='y', labelcolor='r')
    plt.show()

def plot_velocity(time, vel):
    fig, ax1 = plt.subplots(figsize=(8, 3))
    ax1.plot(time, vel, 'm', label='Velocity (m/s)')
    ax1.set_xlabel('Time (s)')  # Set x-axis label to seconds
    ax1.set_ylabel('Velocity (m/s)', color='m')
    ax1.tick_params(axis='y', labelcolor='m')
    # ax2 = ax1.twinx()
    # ax2.plot(time, mag, 'g', label='Magnetism (T)')
    # ax2.set_xlabel('Time (s)')  # Set x-axis label to seconds
    # ax2.set_ylabel('Magnetism (T)', color='g')
    # ax2.tic_params(axis='y', labelcolor='g')
    plt.show()

def start(f):
    interact(
        f,
        V0=IntSlider(value=100, min=0, max=1000, step=5, description='V0 (Volts)'),
        C=FloatLogSlider(value=0.01, base=10, min=-6, max=2, step=0.1, description='C (Farads)'),
        R=FloatSlider(value=1, min=0.1, max=10, step=0.1, description='R'),
        N=FloatSlider(value=100, min=1, max=1000, description='Turns'),
        D=FloatSlider(value=.01, min=.001, max=.1, step=0.001, description='Diameter of coil (m)'),
        l=FloatSlider(value=.06, min=.01, max=.3, step=0.01, description='Length of coil (m)'),
        sd=FloatSlider(value=0.005, min=0.001, max=.1, step=0.001, description='Diameter of slug (m)'),
        sl=FloatSlider(value=0.020, min=0.0001, max=0.5, step=0.001, description='Length of slug (m)'),
        duration_s=FloatLogSlider(value=.2, base=10, min=-3, max=2, step=0.1, description='Duration')
    )
