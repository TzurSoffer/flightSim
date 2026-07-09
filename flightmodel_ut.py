##==============================================================================
##
##       SIMULATION Function,  X-Fwd, Y-right, Z-Down
##
##==============================================================================

from mathLib import *
from Solver_6DOF import Solver_6DOF

class Controls():
    def __init__(self, elevatorCmd, aileronCmd, rudderCmd, throttleCmd, gearsDownCmd):
        self.elevatorCmd = elevatorCmd
        self.aileronCmd  = aileronCmd
        self.rudderCmd   = rudderCmd
        self.throttleCmd = throttleCmd
        self.gearsDownCmd = int(gearsDownCmd)
        
class AeroModel():
    def __init__(self, dt, altInit_m, speed_fps, weight_lbs, units):
        self.dt = dt
        self.time = 0.0

        self.attitude = Attitude(0,0,0) #< Initial orientation
        self.W = Vec_pqr()              #< p, q, r (xyz) angular velocity
        self.T = Vec_pqr()              #< Torque

        self.position = Vec_xyz(0.0, 0.0, -altInit_m)  #< X-Fwd, Y-right, Z-Down
        self.Vb = Vec_xyz(speed_fps, 0.0, 0.0) #< u, v, w  linear Velocity 
        self.Ve = Vec_xyz(*MxV(self.attitude.dcm, self.Vb.getVector()))
        self.Ab = Vec_xyz() #< Acceleration (u, v, w)
        self.Fb = Vec_xyz() #< Force (forward, right, down )

        self.mass = 1 #weight_lbs  #< Weight lbs : mass (lbs/G slugs )
        self.Thrust_N = 0.0
        self.alpha_r = 0.0
        self.beta_r = 0.0
        
        self.solver = Solver_6DOF(
            position = self.position, #< All values are passed by reference
            Ve = self.Ve,
            mass = (self.mass,),
            attitude = self.attitude,
            Wb = self.W,
            inertia = Vec_xyz(0.025,0.05,0.05)
            )
    
        self.elevatorCmd = 0.0 #< Elevator deflection (+/-1)
        self.aileronCmd  = 0.0 #< Aileron deflection (+/-1)
        self.rudderCmd   = 0.0 #< Rudder deflection (+/-1)
        self.throttleCmd = 0.0 #< Throttle 0 to 1
        self.gearsDownCmd= 0.0 #< Throttle 0 to 1

    def step(self, ctrls, dt=None ):
        dt = self.dt if dt==None else dt
        self.time += dt
        
        ## Update the airspeed 
        self.Vb = Vec_xyz(*MxV(self.attitude.inv(), self.Ve.getVector()))
        Vabs = self.Vb.mag()

        self.elevatorCmd = ctrls.elevatorCmd
        self.aileronCmd  = ctrls.aileronCmd
        self.rudderCmd   = ctrls.rudderCmd
        self.throttleCmd = ctrls.throttleCmd

        ##=======================================================================================================================
        ## Momenets and rotation
        ## X axis
        self.T.p  = self.aileronCmd
        
        ## Y axis
        self.T.q  = self.elevatorCmd

        ## Z axis 
        self.T.r  = self.rudderCmd
        ##=======================================================================================================================   

        ## X Axis
        self.Fb.x = 360*self.throttleCmd -Sign(self.Vb.x)*0.002*(self.Vb.x**2)

        ## Y Axis
        self.Fb.y =  -0.02*Sign(self.Vb.y)*(self.Vb.y**2)
    
        ## Z axis, (-) to flip for Z axis sign convention, right hand rule
        self.Fb.z =  -0.02*Sign(self.Vb.z)*(self.Vb.z**2)
        ##=======================================================================================================================   

        ### 6-DOF SOLVER
        _6DOF_ACTIVE = True
        if _6DOF_ACTIVE:
            self.W.p, self.W.q, self.W.r = 0,0,0
            Fext = Vec_xyz(0,0,21*self.mass) 
            self.Ab = self.solver.step(Fext, self.Fb, self.T, dt)
        else:
            self.attitude.roll_r  = 6.28*self.W.p
            self.attitude.pitch_r = 6.28*self.W.q
            self.attitude.yaw_r   = 6.28*self.W.r
        ##=======================================================================================================================   

        #print("Torque : %s"%(self.T))
        #print("Wb: %s"%(self.W))
        #print("Vb: %s"%(self.Vb))
        #print("Ve: %s"%(self.Ve))
        #print("Ab: %s"%(self.Ab))
##        Att = self.attitude
##        print("Attitude:, %1.1f, %1.1f, %1.1f\n"%(Att.roll_r, Att.pitch_r, Att.yaw_r))
##        Pos = self.position
##        print("Position:, %1.1f, %1.1f, %1.1f\n"%(Pos.x, Pos.y, Pos.z))

        ##=================================================================================================================

    def __str__(self):
        s = "="*10 +" %1.2f sec "%(self.time) +"="*10 +"\n"
        Pos = self.position
        s += "X-Forward; Y-Right; Z-Down\n"
        s += "Position    :, %1.2f, %1.2f, %1.2f\n"%(   Pos.x,    Pos.y,    Pos.z)
        s += "Velosity    :, %s1.2f, %1.2f, %1.2f\n"%(self.Vb.x, self.Vb.y, self.Vb.z)
        s += "Accel       :, %1.2f, %1.2f, %1.2f\n"%(self.Ab.x, self.Ab.y, self.Ab.z)
        s += "Ele,Ail,RudA:, %1.2f, %1.2f, %1.2f\n"%(self.elevatorCmd*RADtoDEG, self.aileronCmd*RADtoDEG, self.rudderCmd*RADtoDEG)

        Att = self.attitude
        s += "\n"
        s += "p-Roll; q-Pitch; r-Yaw\n"
        s += "Attitude :, %1.1f, %1.1f, %1.1f\n"%(Att.roll_r, Att.pitch_r, Att.yaw_r)
        s += "Omega    :, %1.3f, %1.3f, %1.3f\n"%(self.W.p, self.W.q, self.W.r)
        s += "Torque   :, %1.2f, %1.2f, %1.2f\n"%(self.T.p, self.T.q, self.T.r)
        return s

    def print(self):
        print(self)

    def getAttitude(self):
        """Return Vector3( roll_rad, pitch_rad, yaw_rad )"""
        return Vec3(self.roll_r, self.pitch_r, self.yaw_r)

    def getPosition(self):
        """Return Vector3(x, y, z)"""
        return Vec3(self.position.x, self.position.y, self.position.z)


if __name__ == "__main__":
    mdl = AeroModel(dt=0.1, altInit_m=0.0, speed_fps=210.0, weight_lbs=2750, units="Metric")
    ctrl = Controls(elevatorCmd=0.1, aileronCmd=-0.0, rudderCmd=0.0, throttleCmd=0.0, gearsDownCmd=0.0)
    mdl.print()
    for i in range(0,20):
        mdl.step(ctrl, dt=0.05)
        mdl.print()
