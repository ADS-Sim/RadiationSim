# MONTE CARLO SIMULATION

# IMPORTS
import time as t
import random
import matplotlib.patches as patches

import Component


class Simulation:
    def __init__(self, origin, simulation_radiation_type):
        self.origin = origin
        self.pcb = Component.PCB(self.origin)
        self.particle_shot_list = []
        self.particle_shot_list_x_hit = []
        self.particle_shot_list_y_hit = []
        self.particle_shot_list_x = []
        self.particle_shot_list_y = []

        self.simulation_radiation_type = simulation_radiation_type

    def create_pcb(self):
        self.pcb.create_components()

    def start(self):
        self.simulation_radiation_type.run(self.origin, self.pcb)
        self.particle_shot_list_x, self.particle_shot_list_y,\
            self.particle_shot_list_x_hit, self.particle_shot_list_y_hit = self.simulation_radiation_type.get_display_data()
