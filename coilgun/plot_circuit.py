def plot_circuit(solution):
    fig, ax1 = plt.subplots(figsize=(8, 4))
    # Plot current
    ax1.plot(solution['time'], solution['current'], 'r', label='Current (A)')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Current (A)', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1.grid(True)
    # ax2 = ax1.twinx()
    # ax2.plot(solution.time, solution.acceleration, 'b', label='B')
    # ax2.set_ylabel('Acceleration', color='b')
    # ax2.tick_params(axis='y', labelcolor='b')
    plt.show()