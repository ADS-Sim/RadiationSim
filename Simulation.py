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
        self.simulation_t0 = t.time()
        self.particle_shot_t = 0
        self.failure_t = 0

        # MONTE CARLO PARAMETERS
        self.margin_time = 5  # days
        self.mission_time = 6 * 30 + random.randint(self.margin_time * -1, self.margin_time)  # days
        self.orbit_type = 'LEO'
        self.alpha_particle_rate_margin = 5  # 5%
        self.alpha_particle_rate = random.randint(14 - self.alpha_particle_rate_margin,
                                                  14 + self.alpha_particle_rate_margin) / 100  # 14%
        self.particle_rate = int(1000 * self.alpha_particle_rate)  # particle per day per 100mm² (10 particles in 1cm3)
        self.particle_number = self.particle_rate * self.mission_time

    def parameter_set(self):
        print(f"----------- MONTE CARLO RADIATION SIMULATION -----------")
        print(f"Mission Time    : {self.mission_time} days")
        print(f"Orbit           : {self.orbit_type}")
        print(f"Particle rate   : {self.particle_rate} per day for 100mm²")
        print(f"Particle Number : {self.particle_number}")
        print(f"--------------------------------------------------------\n")

    def create_pcb(self):
        self.pcb.create_components()

    def shoot_particle(self):
        t_temporary = t.time()
        for _ in range(self.particle_number):
            self.particle_shot_list.append(Component.Particle(self.origin, self.pcb))
            self.check_critical_components(self.particle_shot_list[-1])
        self.particle_shot_t = t.time() - t_temporary

    def check_critical_components(self, particle):
        t_temporary = t.time()
        out = False
        for component in self.pcb.component_list:
            if component.borders_x[0] < particle.pos_x < component.borders_x[1] and component.borders_y[0] < particle.pos_y < component.borders_y[1]:
                particle.color = 'r'
                self.particle_shot_list_x_hit.append(particle.pos_x)
                self.particle_shot_list_y_hit.append(particle.pos_y)
                if component.failure_rate < 1:
                    component.failure_rate = round(component.failure_rate + component.failure_recalculation(), 2)
                else:
                    component.failure_rate = 1
                out = True
            else:
                self.particle_shot_list_x.append(particle.pos_x)
                self.particle_shot_list_y.append(particle.pos_y)
            component.failure_rate_list.append(component.failure_rate)
        self.failure_t = t.time() - t_temporary
        return out
