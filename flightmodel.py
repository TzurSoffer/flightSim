##==============================================================================
##
##       SIMULATION X-Fwd, Y-right, Z-Down
##
##==============================================================================

from math import sin, cos, atan
from mathLib import *
import AircraftParameters as airMdl
from Atmos import Atmos
from Solver_6DOF import Solver_6DOF

class Controls():
    def __init__(self, Elevator_Cmd, Aileron_Cmd, Rudder_Cmd, Throttle_Cmd, GearExtend_Cmd):
        self.Elevator_Cmd = Elevator_Cmd
        self.Aileron_Cmd  = Aileron_Cmd
        self.Rudder_Cmd   = Rudder_Cmd
        self.Throttle_Cmd = Throttle_Cmd
        self.GearExtend_Cmd = int(GearExtend_Cmd)

class AeroModel():
    def __init__(self, dt, altInit_m, speed_fps, weight_lbs, units):
        self.params = airMdl.Params()
        self.dt = dt
        self.time = 0.0

        self.attitude = Attitude(0,0,0) #< Initial orientation
        self.W = Vec_pqr()              #< p, q, r (xyz) angular velocity
        self.T = Vec_pqr()              #< Torque

        self.position = Vec_xyz(0.0, 0.0, -altInit_m) 
        self.Vb = Vec_xyz(speed_fps, 0.0, 0.0) #< u, v, w  linear Velocity 
        self.Ve = Vec_xyz(*MxV(self.attitude.dcm, self.Vb.getVector()))
        self.Ab = Vec_xyz() #< Acceleration (u, v, w)
        self.Fb = Vec_xyz() #< Force (forward, right, down )
        self.Weight = self.params.WEIGHT  #< Weight lbs : mass (lbs/G slugs )
        self.Thrust = 0.0 

        self.alpha_r, self.beta_r = (0.0, 0.0)
        self.Lift, self.Drag = (0.0, 0.0)

        self.elevatorCmd = 0.0  #< Elevator deflection (radians)
        self.elevatorTrim_deg = self.params.ELV_TRIM_D

        self.aileronCmd = 0.0   #< Aileron deflection (radians)
        self.aileronTrim_deg = self.params.AIL_TRIM_D

        self.rudderCmd = 0.0    #< Rudder deflection (degrees)
        self.rudderTrim_deg = self.params.RUD_TRIM_D

        self.gearExtendCmd = 0

        self.solver = Solver_6DOF(
            position = self.position, #< All values are passed by reference
            Ve = self.Ve,
            mass = (self.params.MASS,),
            attitude = self.attitude,
            Wb = self.W,
            inertia = Vec_xyz(self.params._Ixx,
                              self.params._Iyy,
                              self.params._Izz)
            )

    def step(self, ctrls, dt=None ):
        dt = self.dt if dt==None else dt
        self.time += dt
        
        ##================ Controls ================================================================================================
        self.elevatorCmd  = -(ctrls.Elevator_Cmd * self.params.ELV_MAX_ANG_D ) #< Pitch stick y axis range -1.0 to 1.0
        self.elevatorCmd += self.elevatorTrim_deg
        self.elevatorCmd *= DEGtoRAD

        self.aileronCmd  = -(ctrls.Aileron_Cmd * self.params.AIL_MAX_ANG_D )   #< Roll stick x axis range -1.0 to 1.0
        self.aileronCmd += self.aileronTrim_deg
        self.aileronCmd *= DEGtoRAD

        self.rudderCmd  = -(ctrls.Rudder_Cmd * self.params.RUD_MAX_ANG_D )     #< Roll stick x axis range -1.0 to 1.0
        self.rudderCmd += self.rudderTrim_deg
        self.rudderCmd *= DEGtoRAD
        self.gearExtendCmd = max(0, min(1, ctrls.GearExtend_Cmd))
        self.Thrust = ctrls.Throttle_Cmd * self.params.MAX_THRUST              #< Throttle Command setting [ 0, 1]

        ##================== Airspeed, Alpha, Beta, Flight Path ======================================================================
        ## Update the airspeed 
        self.Vb = Vec_xyz(*MxV(self.attitude.inv(), self.Ve.getVector()))
        Vabs = max(1.0,self.Vb.mag())
        #print("Vabs protection") if Vabs == 1.0 else None
        
        if abs(self.Vb.x) < 1.0:
            self.alpha_r = 0.0 #< No AOA and Sideslip at low speed
            self.beta_r  = 0.0
        else:
            self.alpha_r =  min(0.52, max(-0.52, atan( self.Vb.z/self.Vb.x ))) #< Limited to +/-30 deg
            self.beta_r  = min(0.707, max(-0.707, (asin( self.Vb.y/Vabs ))))   #< Limited to +/-45 deg

        ##========================== Momenets and rotation============================================================================
        rho = Atmos.getRho(-self.position.z)
        qS  = 0.5 * rho * (Vabs**2) * self.params._S #< S is wing area
        _B  = self.params._B
        qSc = qS * self.params._C
        qSb = qS * _B
        Wp, Wq, Wr = self.W.p, self.W.q, self.W.r #< Current state

        ## X axis
        Clo   = self.params.Cl_0       #< Roll, Zero-control moment ( typically small or zero in symmetric flight )
        Clda  = self.params.Cl_DA      #< Roll, Aileron effectiveness 9 change in Cl per radian of aileron deflection )
        Clr   = self.params.Cl_R       #< Roll, Yaw-roll coupling ( change in Cl per unti of yaw rate. )
        Clp   = self.params.Cl_P       #< Roll, Damping ( change in Cl per unit of roll rate ) 
        self.T.p  = Clda*self.aileronCmd     #< Roll command
        self.T.p += Clo -0.02*self.rudderCmd #< Rudder command to roll moment (Counter roll)
        self.T.p += Clr*Wr*_B/(2*Vabs)       #< Yaw rate to roll moment (roll into the turn)
        self.T.p += Clp*Wp*_B/(2*Vabs)       #< Rate resistance
        self.T.p *= qSb                      #< Factor due to air speed 
        
        ## Y axis
        Cmo   = self.params.CM_0       #< Baseline pitching moment coefficient
        Gmo   = self.params.GM_0       #< Baseline pitching moment coefficient due to gears down
        Cmde  = self.params.CM_DELTA_E #< Pitching moment slope due to elevator deflection (per radian)
        Cma   = self.params.CM_ALPHA   #< Pitching moment slope due to AoA (per radian)
        Cmq   = self.params.CM_Q       #< Pitch Damping coefficient#-0.7, -0.15
        self.T.q  = Cmde*self.elevatorCmd #< Command to pitch moment
        self.T.q += Cmo +Cma*self.alpha_r #< Wing pitch moment (baseline and angle of attack)
        self.T.q += Cmq*Wq                #< Rate resistance
        self.T.q += self.gearExtendCmd*Gmo
        self.T.q *= qSc                   #< Factor due to air speed 
        
        ## Z axis 
        Cno   = self.params.CN_0       #< Baseline yaw moment coefficient
        Cnb   = self.params.CN_b       #< Yaw, sideslip moment, yaw stability
        Cnp   = self.params.CN_p       #< Yaw, roll moment, rikk-yaw coupling 
        Cndr  = self.params.CN_dr      #< Yaw, rudder deflection moment, rudder effectiveness
        Cnda  = self.params.CN_da      #< Yaw, aileron defection moment, aileron inducted yaw
        Cnr   = self.params.CN_r       #< Yaw, Damping coefficient
        self.T.r  = Cndr*self.rudderCmd   #< Command to yaw moment
        self.T.r += Cno +Cnb*self.beta_r  #< Side slip (Beta) to moment (yaw stability)
        self.T.r += -Cnp*Wp*_B/(2*Vabs)   #< Roll rate to Yaw moment (will roll into the turn)
        self.T.r += Cnr*Wr*_B/(2*Vabs)    #< Rate resistance
        self.T.r *= qSb                   #< Factor due to air speed 
        ##=======================================================================================================================   

        ## Lift and drag forces - linear
        CL = self.params.CL_0 +self.params.CL_ALPHA*self.alpha_r
        self.Lift = qS * CL
        Cd = self.params.CD_0 +self.params.K*self.alpha_r #< Prsuming CD_0 and K are normalized to wing area
        Cd += self.gearExtendCmd*self.params.G_CD_0
        self.Drag = qS * Cd

        ## X Axis
        self.Fb.x  = self.Thrust
        self.Fb.x += -self.Lift * sin(self.alpha_r) #< Lift component that pulls back
        self.Fb.x += -self.Drag * cos(self.alpha_r) #< Drag

        ## Y Axis
        Cy  = self.params.CY_DELTA_R*self.rudderCmd  #< Rudder to side movement
        Cy += self.params.CY_B * self.beta_r         #< Side force due to side slip
        #Cy += self.params.CY_p*Wp*self.Vb.z/(2*Vabs) #< ??
        #Cy += self.params.CY_r*Wr*self.Vb.z/(2*Vabs) #< ??

        self.Fb.y = qS * Cy
        self.Ab.y  = self.Fb.y / self.params.MASS
        #self.Ab.y += Wr * self.Vb.x #< Side force due to roll rate  ??
        #self.Ab.y -= Wp * self.Vb.z #< Side force due to pitch rate ??
        self.Fb.y = self.Ab.y * self.params.MASS

        ## Z axis, (-) to flip for Z axis sign convention, right hand rule
        self.Fb.z  = -self.Lift * cos(self.alpha_r) #< Lift component up
        self.Fb.z += -self.Drag * sin(self.alpha_r) #< Drag component up

        Fext = Vec_xyz(0,0,self.params.G* self.params.MASS)
        ##=======================================================================================================================   
        #min(0.01, dt)
        if dt > 0.035:
            print("dt too high %1.3f"%dt)
            dt = 0.01
        self.Ab = self.solver.step(Fext, self.Fb, self.T, dt)

        #print("AOA,Beta: %1.2f, %1.2f"%(self.alpha_r*RADtoDEG, self.beta_r*RADtoDEG))
        #print("Torque : %s"%(self.T))
        #print("Vb: %s"%(self.Vb))
        #print("Ve: %s"%(self.Ve))
        #print("Fb: %s"%(self.Fb))

        ##=================================================================================================================

    def __str__(self):
        s = "="*10 +" %1.2f sec "%(self.time) +"="*10 +"\n"
        Pos = self.position
        s += "X-Forward; Y-Right; Z-Down\n"
        s += "Position    :, %1.2f, %1.2f, %1.2f\n"%(   Pos.x,    Pos.y,    Pos.z)
        s += "Velosity    :, %s1.2f, %1.2f, %1.2f\n"%(self.Vb.x, self.Vb.y, self.Vb.z)
        s += "Accel       :, %1.2f, %1.2f, %1.2f\n"%(self.Ab.x, self.Ab.y, self.Ab.z)
        s += "Ele,Ail,RudA:, %1.2f, %1.2f, %1.2f\n"%(self.elevatorCmd*RADtoDEG, self.aileronCmd*RADtoDEG, self.rudderCmd*RADtoDEG)
        s += "Lift,Drag   :, %1.2f, %1.2f\n"%(self.Lift, self.Drag)
        s += "AOA,Beta    :, %1.2f, %1.2f\n"%(self.alpha_r, self.beta_r)

        Att = self.attitude
        s += "\n"
        s += "p-Roll; q-Pitch; r-Yaw\n"
        s += "Attitude :, %1.1f, %1.1f, %1.1f\n"%(Att.roll_r, Att.pitch_r, Att.yaw_r)
        s += "Omega    :, %1.3f, %1.3f, %1.3f\n"%(self.W.p, self.W.q, self.W.r)
        #s += "Omega_dot:, %1.3f, %1.3f, %1.3f\n"%(self.W_dot.p, self.W_dot.q, self.W_dot.r)
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
    ctrl = Controls(Elevator_Cmd= 0.01, Aileron_Cmd=-0.0, Rudder_Cmd=.0, Throttle_Cmd=0.0, GearExtend_Cmd=0.0)
    mdl.print()
    for i in range(0,20):
        mdl.step(ctrl, dt=0.01)
        mdl.print()
        print("rho (at %d): %1.4f"%(i*2000, Atmos.getRho(i*2000)))

