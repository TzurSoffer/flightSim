
from mathLib import *

class Solver_6DOF():
    def __init__(self, position, Ve, mass, attitude, Wb, inertia):
        self.position = position
        self.Ve = Ve
        self.attitude = attitude
        self.Wb = Wb
        self.I = inertia
        self.mass = mass
        
    def step(self, Fext, Fb, Tb, dt) -> list:
        ## Next state - Angular velocity integration in body coordinates
        self.Wb.p += (Tb.p / self.I.x) * dt
        self.Wb.q += (Tb.q / self.I.y) * dt
        self.Wb.r += (Tb.r / self.I.z) * dt

        self.attitude.addW(self.Wb, dt)

        ## Next state - Body to earth transform
        mass = self.mass[0]
        Fe = MxV(self.attitude.dcm, Fb.getVector())
        Ab = Vec_xyz(((Fe[0] +Fext.x)/mass), ((Fe[1] +Fext.y)/mass), ((Fe[2] +Fext.z)/mass))
        self.Ve.x += Ab.x * dt
        self.Ve.y += Ab.y * dt
        self.Ve.z += Ab.z * dt

        ## Next state - Position in earth coordinates
        self.position.x += self.Ve.x * dt
        self.position.y += self.Ve.y * dt
        self.position.z += self.Ve.z * dt

        return Ab
