# MONTE CARLO SIMULATION
import random
import time

# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Display:
    def __init__(self):
        self.particle_figure, self.particle_ax = plt.subplots()
        self.failure_figure, self.failure_ax = plt.subplots()
        self.component_figure, self.component_ax = None, None

        self.origin = [0, 0]

        self.failure_x_axis = []
        self.failure_y_axis = []

    def plot_pcb(self, pcb):
        self.particle_ax.add_patch(patches.Rectangle((self.origin[0], self.origin[1]),
                                                     pcb.size[0], pcb.size[1],
                                                     edgecolor=pcb.edge_color, facecolor=pcb.face_color))
        # Shots
        for component in pcb.component_list:
            self.particle_ax.add_patch(patches.Rectangle((component.pos_x - component.size[0] / 2,
                                                          component.pos_y - component.size[1] / 2),
                                                         component.size[0], component.size[1],
                                                         edgecolor=component.edge_color, facecolor=component.color))

    def plot_particles(self, particle_list_x, particle_list_y, particle_list_x_hit, particle_list_y_hit):
        plt.gca().set_aspect('equal', adjustable='box')  # Ensures equal aspect ratio
        self.particle_ax.set_title("RADIATION SPREAD")

        # self.particle_ax.scatter(particle_list_x, particle_list_y, c='b', s=0.1)
        self.particle_ax.scatter(particle_list_x_hit, particle_list_y_hit, c='r', s=0.1)

    def plot_failure(self, simulation):
        plt.gca().set_aspect('auto', adjustable='box')  # Ensures auto aspect ratio
        self.failure_ax.set_title("FAILURE OVER TIME")
        self.failure_ax.set_ylim([0, 1])

        for component in simulation.pcb.component_list:
            self.failure_ax.plot(component.time_list_failure, component.rate_list_failure, color=component.color)  # LA
            self.failure_ax.plot([0, len(component.time_list_failure) - 1], [0.4, 0.4], color='r', linestyle='-')

    def plot_component_failure_rate(self, component_list):
        style = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']
        self.component_figure, self.component_ax = plt.subplots(2, int((len(component_list) + 1) / 2), figsize=(8, 8))
        line = 0
        index = 0
        for component in component_list:
            grid_size_x = len(component.failure_rate_matrix) + 1
            grid_size_y = len(component.failure_rate_matrix[0]) + 1

            if index >= int((len(component_list) + 1) / 2):
                line = 1
                index = 0
            cax = self.component_ax[line][index].imshow(component.failure_rate_matrix, cmap=style[1], vmin=0, vmax=1)
            self.component_figure.colorbar(cax, shrink=0.7)

            self.component_ax[line][index].set_title(component.name)
            self.component_ax[line][index].set_xticks([])
            self.component_ax[line][index].set_yticks([])
            self.component_ax[line][index].grid(which='both', color='white', linestyle='-', linewidth=1.5)

            index += 1

    def display_graphs(self):
        plt.show()

    def simulation_time(self, simulation):
        print(f"Simulation Time : {round(time.time() - simulation.simulation_t0, 3)} s")
        print(f"Particle Shot Time : {round(simulation.particle_shot_t, 3)} s")
        print(f"Failure Calculation Time : {round(simulation.failure_t, 3)} s")
