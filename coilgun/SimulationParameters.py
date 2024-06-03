from collections import namedtuple

SimulationParameters = namedtuple('SimulationParameters',
                                  ['init_volts',
                                   'capacitance',
                                   'resistance',
                                   'num_turns',
                                   'coil_diameter',
                                   'coil_length',
                                   'slug_diameter',
                                   'slug_length',
                                   'duration_s',
                                   'time_step',
                                   ])
