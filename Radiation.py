# MONTE CARLO SIMULATION
import random
import Component

# RADIATION EFFECTS
TID = 'TID'
SEGR = 'SEGR'
SEB = 'SEB'
SEE = 'SEE'
TNID = 'TNID'
SEU = 'SEU'
SET = 'SET'
SEL = 'SEL'


# CLASS

class SEE:
    # Definition of Single Event Effects for a defined dose applied for a defined time
    def __init__(self):
        # Mission Parameters
        self.orbit_type = 'LEO'
        self.mission_time = 6 * 30  # days
        self.mission_time_margin = 5  # days

        self.particle_rate_margin = 0.05  # 5%
        self.particle_rate = 1000  # particle per day per 100mm²  (LEO Orbit -> 10 particles in 1cm3)
        self.alpha_particle_rate_margin = 0.05  # 5%
        self.alpha_particle_rate = 0.14  # 14%
        self.destructive_particle_ratio = 0
        self.particle_number = 0

        self.particle_list = []
        self.alpha_particle_coordinates_x = []
        self.alpha_particle_coordinates_y = []
        self.particle_coordinates_x = []
        self.particle_coordinates_y = []
        self.particle_coordinates_x_hit = []
        self.particle_coordinates_y_hit = []

    def run(self, origin, pcb):
        """
        Standard Simulation
        :return:
        """
        # Implements the components associated to SEE verification
        self.check_component_relevance(pcb)

        # Spread the particles
        self.particle_shoot(origin, pcb)

        # Calculates the destruction probabilities
        for particle in self.particle_list:
            self.check_component_collision(pcb, particle)

    def check_component_relevance(self, pcb):
        for component in pcb.component_list:
            pass
        # raise NotImplementedError

    def particle_shoot(self, origin, pcb):
        # Check the mission time
        self.mission_time = random.randint(self.mission_time - self.mission_time_margin,
                                           self.mission_time + self.mission_time_margin)
        # Define particle rate
        self.particle_rate = int(random.randint(int(self.particle_rate * (1 - self.particle_rate_margin) * 1000),
                                                int(self.particle_rate * (1 + self.particle_rate_margin) * 1000)) / 1000)
        # Set the ratio of destructive particles
        self.destructive_particle_ratio = random.randint(int(self.alpha_particle_rate * (1 - self.alpha_particle_rate_margin) * 1000),
                                                         int(self.alpha_particle_rate * (1 + self.alpha_particle_rate_margin) * 1000)) / 1000
        # Defines the number of particle to shoot
        self.particle_number = int(self.mission_time * self.particle_rate * self.destructive_particle_ratio)
        # Shoot particles
        for _ in range(self.particle_number):
            self.particle_list.append(Component.Particle(origin, pcb))

        # Print Hypothesis
    def parameter_set(self):
        print(f"----------- MONTE CARLO RADIATION SIMULATION -----------")
        print(f"Mission Time               : {self.mission_time}")
        print(f"Orbit                      : {self.orbit_type}")
        print(f"Particle Rate              : {self.particle_rate}")
        print(f"Destructive Particle Ratio : {self.destructive_particle_ratio}")
        print(f"Particle Number            : {self.particle_number}")
        print(f"--------------------------------------------------------\n")

    def check_component_collision(self, pcb, particle):
        for component in pcb.component_list:
            if component.hit_check(particle):
                # Change particle color
                particle.color = 'r'
                # Add particle coordinates to hit list
                self.particle_coordinates_x_hit.append(particle.pos_x)
                self.particle_coordinates_y_hit.append(particle.pos_y)
                # Update Failure Rate of the component and the timeline
                component.update_timeline()
                component.update_failure_rate()

            else:
                # Add particle coordinates to no-hit list
                self.particle_coordinates_x.append(particle.pos_x)
                self.particle_coordinates_y.append(particle.pos_y)
                # Update Failure Rate of the component and the timeline
                component.fill_failure_list()
                component.update_timeline()

    def get_display_data(self):
        return self.particle_coordinates_x, self.particle_coordinates_y,\
            self.particle_coordinates_x_hit, self.particle_coordinates_y_hit


class TID:
    def __init__(self):
        self.particle_rate_margin = 5  # 5%
        self.particle_rate = 0
        self.alpha_particle_rate_margin = 5  # 5%
        self.alpha_particle_rate = 0
