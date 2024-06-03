def basic_plot(x, x_name, y, y_name):
    fig, ax1 = plt.subplots(figsize=(8, 3))
    ax1.plot(x, y)
    ax1.set_xlabel(x_name)
    ax1.set_ylabel(y_name, color='m')
    ax1.tick_params(axis='y', labelcolor='m')
    plt.show()
