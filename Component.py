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
        stm_fm = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                           [0.00, 0.01, 0.02, 0.02, 0.03, 0.02, 0.01, 0.00],
                           [0.00, 0.01, 0.04, 0.05, 0.05, 0.03, 0.01, 0.00],
                           [0.00, 0.02, 0.06, 0.08, 0.09, 0.05, 0.02, 0.00],
                           [0.00, 0.03, 0.06, 0.09, 0.09, 0.05, 0.03, 0.00],
                           [0.00, 0.02, 0.04, 0.05, 0.07, 0.05, 0.06, 0.00],
                           [0.00, 0.01, 0.02, 0.03, 0.02, 0.01, 0.01, 0.00],
                           [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])
        nan_fm = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                           [0.00, 0.01, 0.02, 0.02, 0.03, 0.02, 0.01, 0.00],
                           [0.00, 0.01, 0.04, 0.05, 0.05, 0.03, 0.01, 0.00],
                           [0.00, 0.02, 0.06, 0.08, 0.09, 0.05, 0.02, 0.00],
                           [0.00, 0.03, 0.06, 0.09, 0.09, 0.05, 0.03, 0.00],
                           [0.00, 0.02, 0.04, 0.05, 0.07, 0.05, 0.06, 0.00],
                           [0.00, 0.01, 0.02, 0.03, 0.02, 0.01, 0.01, 0.00],
                           [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])
        iso_fm = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                           [0.00, 0.01, 0.02, 0.02, 0.03, 0.02, 0.01, 0.00],
                           [0.00, 0.01, 0.04, 0.05, 0.05, 0.03, 0.01, 0.00],
                           [0.00, 0.02, 0.06, 0.08, 0.09, 0.05, 0.02, 0.00],
                           [0.00, 0.03, 0.06, 0.09, 0.09, 0.05, 0.03, 0.00],
                           [0.00, 0.02, 0.04, 0.05, 0.07, 0.05, 0.06, 0.00],
                           [0.00, 0.01, 0.02, 0.03, 0.02, 0.01, 0.01, 0.00],
                           [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])
        eth_fm = np.array([[0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                           [0.00, 0.01, 0.02, 0.02, 0.03, 0.02, 0.01, 0.00],
                           [0.00, 0.01, 0.04, 0.05, 0.05, 0.03, 0.01, 0.00],
                           [0.00, 0.02, 0.06, 0.08, 0.09, 0.05, 0.02, 0.00],
                           [0.00, 0.03, 0.06, 0.09, 0.09, 0.05, 0.03, 0.00],
                           [0.00, 0.02, 0.04, 0.05, 0.07, 0.05, 0.06, 0.00],
                           [0.00, 0.01, 0.02, 0.03, 0.02, 0.01, 0.01, 0.00],
                           [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]])

        self.component_list.append(Component("STM32H7", 61.0, 77.5, [8.0, 8.0], '#5dade2', stm_fm))  # STM32H7é
        self.component_list.append(Component("NAND", 82.0, 80.0, [10.5, 13.0], '#5499c7', nan_fm))  # NAND
        # self.component_list.append(Component("LAN8742", 40.0, 83.5, [5.0, 5.0], '#af7ac5', eth_fm))  # ETH LAN8742A-CZ
        # self.component_list.append(Component("ISO1044", 21.5, 90.5, [7.0, 5.5], '#f9e79f', iso_fm))  # ISO1044
        # self.component_list.append(Component("ISO1044", 21.5, 85.0, [7.0, 5.5], '#f7dc6f', iso_fm))  # ISO1044
        # self.component_list.append(Component("ISO1044", 21.5, 76.0, [7.0, 5.5], '#f4d03f', iso_fm))  # ISO1044
        # self.component_list.append(Component("SNS Line", 23.0, 63, [38.0, 13.5], '#FFFFFF', iso_fm))  # SNS Line


class Component:
    def __init__(self, name, pos_x, pos_y, size, color, failure_rate_matrix):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size = size
        self.color = color
        self.edge_color = 'k'

        self.borders_x = [self.pos_x - size[0] / 2, self.pos_x + size[0] / 2]
        self.borders_y = [self.pos_y - size[1] / 2, self.pos_y + size[1] / 2]

        self.failure_rate = np.mean(failure_rate_matrix)
        self.failure_rate_margin = 0
        self.failure_rate_list = []
        self.is_not_dead = True

        self.time_list_failure = [1]
        self.rate_list_failure = [self.failure_rate]
        self.failure_rate_matrix = failure_rate_matrix

    def hit_check(self, particle):
        out = False
        if self.borders_x[0] < particle.pos_x < self.borders_x[1] and self.borders_y[0] < particle.pos_y < \
                self.borders_y[1]:
            out = True
        return out

    def update_timeline(self):
        self.time_list_failure.append(self.time_list_failure[-1] + 1)

    def update_failure_rate(self, particle):
        section_x, section_y = self.check_component_section(
            particle)  # a tuple of an X and Y axis coordinates in the matrix
        temporary_failure_rate = min(round(
            self.rate_list_failure[-1] * (1 + self.failure_rate_matrix[section_y][section_x]), 3), 1)
        self.failure_rate_matrix[section_y][section_x] = temporary_failure_rate
        self.rate_list_failure.append(temporary_failure_rate)

    def fill_failure_list(self):
        self.rate_list_failure.append(self.rate_list_failure[-1])

    def check_component_section(self, particle):
        section_x = 0
        section_y = 0

        slot_size_x = self.size[0] / len(self.failure_rate_matrix[0])
        slot_size_y = self.size[1] / len(self.failure_rate_matrix)

        # Change the coordinate referential of the particle
        translation_vector_x, translation_vector_y = (self.pos_x - self.size[0] / 2, self.pos_y - self.size[1] / 2)
        particle_pos_x = particle.pos_x - translation_vector_x
        particle_pos_y = particle.pos_y - translation_vector_y

        x_index = 0
        y_index = 0

        for x in range(len(self.failure_rate_matrix)):
            for y in range(len(self.failure_rate_matrix[0])):
                # print(f"X, Y : ({x}, {y})")
                # print(f"Section checked : [{x_index}; {slot_size_x}] [{y_index}; {slot_size_y}]")
                if x_index <= particle_pos_x < slot_size_x and y_index <= particle_pos_y < slot_size_y:
                    section_x = x
                    section_y = y
                    return section_x, section_y
                else:
                    # Modify the conditions of incrementation
                    y_index += self.size[1] / len(self.failure_rate_matrix)
                    slot_size_y += self.size[1] / len(self.failure_rate_matrix)
                # print(f"Section : ({section_x}, {section_y})")
            x_index += self.size[0] / len(self.failure_rate_matrix[0])
            slot_size_x += self.size[0] / len(self.failure_rate_matrix[0])
            y_index = 0
            slot_size_y = self.size[1] / len(self.failure_rate_matrix)
        print(f"No correspondence found... ({particle_pos_x}, {particle_pos_y})")
        print(f"Component Size : ({self.size[0]}, {self.size[1]})")

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
