# MONTE CARLO SIMULATION
# ECSS-E-ST-10-12C

# IMPORTS
import time as t
import Simulation
import Display
import Radiation

# GLOBAL VARIABLES
ORIGIN = [0, 0]


def main():
    simulation = Simulation.Simulation(ORIGIN, Radiation.SEE())
    simulation.create_pcb()
    simulation.start()

    display = Display.Display()
    display.plot_pcb(simulation.pcb)
    display.plot_particles(simulation.particle_shot_list_x, simulation.particle_shot_list_y,
                           simulation.particle_shot_list_x_hit, simulation.particle_shot_list_y_hit)
    display.plot_failure(simulation)
    display.plot_component_failure_rate(simulation.pcb.component_list)
    display.display_graphs()


if __name__ == '__main__':
    main()
