
def plot_kinematics(output):
    fig, ax1 = plt.subplots(figsize=(8, 3))
    # ax1.plot(output['time'], output['acceleration'], 'm', label='Acc (m/s^2)')
    # ax1.set_xlabel('Time (s)')
    # ax1.set_ylabel('Acc (m/s^2)', color='m')
    # ax1.tick_params(axis='y', labelcolor='m')
    ax2 = ax1.twinx()
    ax2.plot(output['time'], output['velocity'], 'g', label='Velocity (m/s)')
    ax2.set_xlabel('Time (s)')  # Set x-axis label to seconds
    ax2.set_ylabel('Velocity (m/s)', color='g')
    ax2.tick_params(axis='y', labelcolor='g')
    plt.show()

###########################################################################

# Test integration
# vel2 = cumulative_trapezoid(solution.acceleration, solution.time)
# Adjust the time array to match the length of the integrated array
# time_adjusted = solution.time[:-1]
# position = cumulative_trapezoid(solution.velocity, solution.time)
# plt.plot(time_adjusted, vel2, label='v(t)')
# plt.xlabel('Time (s)')
# plt.ylabel('V (m)/s')
# plt.legend()
# plt.show

