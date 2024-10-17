# MONTE CARLO SIMULATION

# IMPORTS
import random
import numpy as np
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
        # stm_fm = 0.001 + (0.032 - 0.001) * np.random.rand(8, 8)
        # nan_fm = 0.001 + (0.032 - 0.001) * np.random.rand(8, 8)
        # iso_fm = 0.001 + (0.032 - 0.001) * np.random.rand(8, 8)
        # eth_fm = 0.001 + (0.032 - 0.001) * np.random.rand(8, 8)

        # Data for simulating the percentage of failure
        stm_fm = 0.001 + (0.1 - 0.001) * np.random.normal(loc=0, scale=1, size=(8, 8))
        nan_fm = 0.001 + (0.1 - 0.001) * np.random.normal(loc=0, scale=1, size=(8, 8))
        iso_fm = 0.001 + (0.1 - 0.001) * np.random.normal(loc=0, scale=1, size=(8, 8))
        eth_fm = 0.001 + (0.1 - 0.001) * np.random.normal(loc=0, scale=1, size=(8, 8))

        # Data simulating the depth of impact for a 3D simulation
        stm_depth_force = 0 + (1 - 0) * np.random.normal(loc=0, scale=1, size=(8, 8))
        nan_depth_force = 0 + (1 - 0) * np.random.normal(loc=0, scale=1, size=(8, 8))
        iso_depth_force = 0 + (1 - 0) * np.random.normal(loc=0, scale=1, size=(8, 8))
        eth_depth_force = 0 + (1 - 0) * np.random.normal(loc=0, scale=1, size=(8, 8))

        self.component_list.append(Component("STM32H7", 61.0, 77.5, [8.0, 8.0], '#5dade2'))  # STM32H7é
        self.component_list.append(Component("NAND", 82.0, 80.0, [10.5, 13.0], '#5499c7'))  # NAND
        self.component_list.append(Component("LAN8742", 40.0, 83.5, [5.0, 5.0], '#af7ac5'))  # ETH LAN8742A-CZ
        self.component_list.append(Component("ISO1044", 21.5, 90.5, [7.0, 5.5], '#f9e79f'))  # ISO1044
        self.component_list.append(Component("ISO1044", 21.5, 85.0, [7.0, 5.5], '#f7dc6f'))  # ISO1044
        self.component_list.append(Component("ISO1044", 21.5, 76.0, [7.0, 5.5], '#f4d03f'))  # ISO1044
        # self.component_list.append(Component("SNS Line", 23.0, 63, [38.0, 13.5], '#FFFFFF', iso_fm))  # SNS Line


class Component:
    def __init__(self, name, pos_x, pos_y, size, color):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.color = color
        self.edge_color = 'k'
        self.scale = 10

        self.borders_x = [self.pos_x - size[0] / 2, self.pos_x + size[0] / 2]
        self.borders_y = [self.pos_y - size[1] / 2, self.pos_y + size[1] / 2]

        self.failure_rate_margin = 0
        self.failure_rate_list = []
        self.is_not_dead = True

        self.time_list_failure = [1]
        self.failure_rate_matrix = 0.001 + (0.08 - 0.001) * np.random.rand(int(size[1] * self.scale) + 1,
                                                                           int(size[0] * self.scale) + 1)
        self.package_resistance_matrix = 0 + (1 - 0) * np.random.rand(int(size[1] * self.scale) + 1,
                                                                      int(size[0] * self.scale) + 1)
        self.failure_rate = np.max(self.failure_rate_matrix)
        self.rate_list_failure = [self.failure_rate]

    def hit_check(self, particle):
        out = False
        if self.borders_x[0] < particle.pos_x < self.borders_x[1] and self.borders_y[0] < particle.pos_y < \
                self.borders_y[1]:
            out = True
        return out

    def update_timeline(self):
        self.time_list_failure.append(self.time_list_failure[-1] + 1)

    def update_failure_rate(self, particle):
        section_x, section_y = self.check_component_section(particle)  # Tuple of X and Y axis coordinates in the matrix
        temporary_failure_rate = min(round(
            self.rate_list_failure[-1] * (1 + self.failure_rate_matrix[section_y][section_x]), 3), 1)
        self.failure_rate_matrix[section_y][section_x] = temporary_failure_rate
        self.rate_list_failure.append(temporary_failure_rate)

    def fill_failure_list(self):
        self.rate_list_failure.append(self.rate_list_failure[-1])

    def check_component_section(self, particle):
        # Change the coordinate referential of the particle
        translation_vector_x, translation_vector_y = (self.pos_x - self.size[0] / 2, self.pos_y - self.size[1] / 2)
        particle_pos_x = (particle.pos_x - translation_vector_x) * self.scale
        particle_pos_y = (particle.pos_y - translation_vector_y) * self.scale

        section_x = int(particle_pos_x)
        section_y = int(particle_pos_y)
        return section_x, section_y


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
