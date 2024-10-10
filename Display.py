# MONTE CARLO SIMULATION
import time

# IMPORTS
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Display:
    def __init__(self):
        self.particle_figure, self.particle_ax = plt.subplots()
        self.failure_figure, self.failure_ax = plt.subplots()

        self.origin = [0, 0]

    def plot_pcb(self, pcb):
        self.particle_ax.add_patch(patches.Rectangle((self.origin[0], self.origin[1]),
                                                     pcb.size[0], pcb.size[1],
                                                     edgecolor=pcb.edge_color, facecolor=pcb.face_color))

    def plot_particles(self, component_list, particle_list_x, particle_list_y, particle_list_x_hit, particle_list_y_hit):
        plt.gca().set_aspect('equal', adjustable='box')  # Ensures equal aspect ratio
        self.particle_ax.set_title("RADIATION SPREAD")

        # Shots
        for component in component_list:
            self.particle_ax.add_patch(component.square)
        self.particle_ax.scatter(particle_list_x, particle_list_y, c='b', s=0.1)
        self.particle_ax.scatter(particle_list_x_hit, particle_list_y_hit, c='r', s=0.1)
        # for particle in particle_list:
        #     self.particle_ax.scatter(particle.pos_x, particle.pos_y, c=particle.color, s=0.1)

    def plot_failure(self, simulation):
        plt.gca().set_aspect('auto', adjustable='box')  # Ensures auto aspect ratio
        self.failure_ax.set_title("FAILURE OVER TIME")
        self.failure_ax.set_ylim([0, 1])
        x_list = [number for number in range(simulation.mission_time)]
        for component in simulation.pcb.component_list:
            y_list = component.sort_failure_rate_list(simulation.particle_rate)
            self.failure_ax.plot(x_list, y_list, color=component.color)
        self.failure_ax.plot([0, len(x_list) - 1], [0.4, 0.4], color='r', linestyle='-')

    def display_graphs(self):
        plt.show()

    def simulation_time(self, simulation):
        print(f"Simulation Time : {round(time.time() - simulation.simulation_t0, 3)} s")
        print(f"Particle Shot Time : {round(simulation.particle_shot_t, 3)} s")
        print(f"Failure Calculation Time : {round(simulation.failure_t, 3)} s")
