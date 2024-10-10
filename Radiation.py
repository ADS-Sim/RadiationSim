# MONTE CARLO SIMULATION

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
    def __init__(self):
        self.particle_rate_margin = 5  # 5%
        self.particle_rate = 0
        self.alpha_particle_rate_margin = 5  # 5%
        self.alpha_particle_rate = 0

    def run(self):
        """
        Standard Simulation
        :return:
        """

class TID:
    def __init__(self):
        self.particle_rate_margin = 5  # 5%
        self.particle_rate = 0
        self.alpha_particle_rate_margin = 5  # 5%
        self.alpha_particle_rate = 0