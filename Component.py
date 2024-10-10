# MONTE CARLO SIMULATION

# IMPORTS
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# GLOBAL VARIABLES
PARTICLE_SPREAD_ACCURACY = 1000  # mm

# Class
class PCB:
    def __init__(self, origin):
        self.size = [100, 100]
        self.component_list = []  # List of components

        self.edge_color = 'k'
        self.face_color = 'g'

    def create_components(self):
        self.component_list.append(Component(10, 20, [10, 10], 'b'))
        self.component_list.append(Component(50, 50, [20, 20], 'cyan'))
        self.component_list.append(Component(70, 70, [10, 10], 'purple'))
        self.component_list.append(Component(30, 20, [10, 15], 'y'))


class Component:
    def __init__(self, pos_x, pos_y, size, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.square = patches.Rectangle((self.pos_x - size[0] / 2, self.pos_y - size[1] / 2),
                                        size[0], size[1], edgecolor='k', facecolor=color)
        self.borders_x = [self.pos_x - size[0] / 2, self.pos_x + size[0] / 2]
        self.borders_y = [self.pos_y - size[1] / 2, self.pos_y + size[1] / 2]

        self.failure_rate = 0
        self.failure_rate_margin = 0
        self.failure_rate_list = []

    def failure_recalculation(self):
        self.failure_rate_margin += round(random.randint(0, 2) / 100, 2)
        return self.failure_rate_margin

    def sort_failure_rate_list(self, particle_rate):
        temporary_failure_rate_list = []
        for i, failure_rate in enumerate(self.failure_rate_list):
            if i % particle_rate == 0:
                temporary_failure_rate_list.append(failure_rate)
        return temporary_failure_rate_list


class Particle:
    def __init__(self, origin, pcb):
        self.pos_x = round(random.randint(origin[0] * PARTICLE_SPREAD_ACCURACY,
                                          pcb.size[0] * PARTICLE_SPREAD_ACCURACY) / PARTICLE_SPREAD_ACCURACY, 3)
        self.pos_y = round(random.randint(origin[1] * PARTICLE_SPREAD_ACCURACY,
                                          pcb.size[1] * PARTICLE_SPREAD_ACCURACY) / PARTICLE_SPREAD_ACCURACY, 3)

        self.touched_component = False
        self.color = 'b'


class ComponentImporter:
    """
    Importer using a pick and place file.
    TODO
    """

    def __init__(self):
        self.file = None
        self.component_list = []

    def import_components(self):
        # Import the XLSX file

        # Get data for each component

        # TODO: Temporary
        self.component_list.append(Component(10, 20, [10, 10]))
        self.component_list.append(Component(50, 50, [20, 20]))
        self.component_list.append(Component(70, 70, [10, 10]))
        self.component_list.append(Component(30, 20, [10, 15]))
        raise NotImplementedError
