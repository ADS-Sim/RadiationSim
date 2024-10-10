# MONTE CARLO SIMULATION

# IMPORTS
import time as t
import Simulation
import Display
import Radiation

# GLOBAL VARIABLES
ORIGIN = [0, 0]


def main():
    simulation = Simulation.Simulation(ORIGIN, Radiation.SEE())
    simulation.parameter_set()
    simulation.create_pcb()
    simulation.shoot_particle()

    display = Display.Display()
    display.plot_pcb(simulation.pcb)
    display.plot_particles(simulation.pcb.component_list,
                           simulation.particle_shot_list_x, simulation.particle_shot_list_y,
                           simulation.particle_shot_list_x_hit, simulation.particle_shot_list_y_hit)
    display.plot_failure(simulation)
    display.simulation_time(simulation)
    display.display_graphs()


if __name__ == '__main__':
    main()
