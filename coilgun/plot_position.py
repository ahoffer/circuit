def plot_position(output):
    fig, ax1 = plt.subplots(figsize=(8, 3))
    ax1.plot(output['time'], output['position'], 'b', label='Pos (m)')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Pos (m)', color='m')
    ax1.tick_params(axis='y', labelcolor='m')
    plt.show
