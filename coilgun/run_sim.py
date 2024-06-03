def run_sim(params):
    output = {}
    t_span = (0, params.duration_s)  # Simulation time span
    t_eval = np.arange(0, params.duration_s, time_step)  # Set simulation time step
    # Solve the differential equation
    circuit_soln = solve_ivp(
        circuit_model,
        t_span,
        [params.init_volts, 0],
        t_eval=t_eval,
        args=(params,))
    output['time'] = circuit_soln.t
    output['voltage'] = circuit_soln.y[0]
    output['current'] = circuit_soln.y[1]
    output = output | force_model(output, params)
    output['v2'] = cumulative_trapezoid(output['acceleration'], output['time'], initial=0)
    output['position'] = cumulative_trapezoid(output['velocity'], output['time'], initial=0)
    return output