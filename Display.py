# MONTE CARLO SIMULATION
import random
import time

# IMPORTS
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Display:
    def __init__(self):
        self.particle_figure, self.particle_ax = plt.subplots()
        self.failure_figure, self.failure_ax = plt.subplots()
        self.component_figure, self.component_ax = plt.subplots()

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
        plot_x_coord = [5, 15, 25, 35, 45, 55, 65, 75]
        plot_y_coord = [5, 15, 25, 35, 45, 55, 65, 75]

        plt.gca().set_aspect('equal', adjustable='box')  # Ensures equal aspect ratio
        self.component_figure, self.component_ax = plt.subplots(int(len(component_list) + 1 / 2), 2)
        for i, component in enumerate(component_list):
            patch_list = []
            self.component_ax[i][0].set_title(f"{component.name}")
            self.component_ax[i][0].set_xlim = [0, (len(component.failure_rate_matrix) + 1) * 10]
            self.component_ax[i][0].set_ylim = [0, (len(component.failure_rate_matrix[0]) + 1) * 10]
            for x in range(len(component.failure_rate_matrix)):
                for y in range(len(component.failure_rate_matrix[0])):
                    # color_failure = (component.failure_rate_matrix[x][y] * 255 / 255,
                    #                  component.failure_rate_matrix[x][y] * 255 / 255, 0.0)
                    color_failure = (random.randint(0, 255) / 255, random.randint(0, 255) / 255, random.randint(0, 255) / 255)
                    print(f"{int(i / 2)} : {i % 2}")
                    self.component_ax[int(i / 2), i % 2].add_patch(patches.Rectangle((x * 10 + 5, y * 10 + 5), 10, 10, edgecolor='k', facecolor=color_failure))
            print(patch_list)
        self.component_ax[0][0].plot(plot_x_coord, plot_y_coord)


    def display_graphs(self):
        plt.show()

    def simulation_time(self, simulation):
        print(f"Simulation Time : {round(time.time() - simulation.simulation_t0, 3)} s")
        print(f"Particle Shot Time : {round(simulation.particle_shot_t, 3)} s")
        print(f"Failure Calculation Time : {round(simulation.failure_t, 3)} s")
