import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, FloatLogSlider, IntSlider

def plot_circuit(solution):
    [voltage, current, acceleration] = solution.y
    time_sim = solution.t
    # Plot Current
    plt.figure(figsize=(8, 4))
    plt.plot(time_sim, current, 'r', label='Current (A)')
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.legend()
    plt.title('Current vs. Time')
    plt.grid(True)
    plt.tick_params(axis='y', labelcolor='r')
    plt.show()
    return solution

def plot_velocity_and_magnetism(time, vel, mag):
    fig, ax1 = plt.subplots(figsize=(8, 3))
    ax1.plot(time, vel, 'm', label='Velocity (m/s)')
    ax1.set_xlabel('Time (s)')  # Set x-axis label to seconds
    ax1.set_ylabel('Velocity (m/s)', color='m')
    ax1.tick_params(axis='y', labelcolor='m')
    ax2 = ax1.twinx()
    ax2.plot(time, mag, 'g', label='Magnetism (T)')
    ax2.set_xlabel('Time (s)')  # Set x-axis label to seconds
    ax2.set_ylabel('Magnetism (T)', color='g')
    ax2.tick_params(axis='y', labelcolor='g')
    plt.show()