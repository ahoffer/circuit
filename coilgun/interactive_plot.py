from ipywidgets import interact, IntSlider, FloatLogSlider, FloatSlider

from SimulationParameters import SimulationParameters


def start(f):
    interact(
        f,
        V0=IntSlider(value=100, min=0, max=100000, step=5, description='V0 (Volts)'),
        C=FloatLogSlider(value=0.1, base=10, min=-6, max=2, step=0.1, description='C (Farads)'),
        R=FloatSlider(value=3, min=0.1, max=10, step=0.1, description='R'),
        N=IntSlider(value=100, min=1, max=1000, description='Turns'),
        D=FloatSlider(value=.01, min=.001, max=.1, step=0.001, description='Diameter of coil (m)', layout=Layout(width='400px'), style={'description_width': '250px'}),
        l=FloatSlider(value=.06, min=.01, max=.3, step=0.01, description='Length of coil (m)'),
        sd=FloatSlider(value=0.005, min=0.001, max=.1, step=0.001, description='Diameter of slug (m)'),
        sl=FloatLogSlider(value=0.010, base=10, min=-3, max=1, step=0.01, description='Length of slug (m)'),
        duration_s=FloatLogSlider(value=.2, base=10, min=-3, max=2, step=0.1, description='Duration')
    )

def solve_and_plot(V0, C, R, N, D, l, sd, sl, duration_s):
    simulationParameters = SimulationParameters(init_volts=V0,
                                     capacitance=C,
                                     resistance=R,
                                     num_turns=N,
                                     coil_diameter=D,
                                     coil_length=l,
                                     slug_diameter=sd,
                                     slug_length=sl,
                                     duration_s=duration_s)
    output = run_sim(simulationParameters)
