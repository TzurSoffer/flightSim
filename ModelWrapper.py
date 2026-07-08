"""
 * ModelWrapper.py
 * Created on: 7 July 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

import math, sys, time
import pygame
from GSOF_Cockpit.GraphicsLib import getMouse

from bus.State import State
from flightmodel import AeroModel, Controls
from flightmodel_ut import AeroModel as TestModel

from math import pi
radToDeg = 180/pi

class Buses():
    def __init__(self):
        self.mousePos     = (0,0)
        self.mousePos_Z1  = self.mousePos

        self.time   = 0.0
        self.state = State()
        self.cmds = Controls(
            elevatorCmd =  0.00,
            aileronCmd  =  0.00,
            rudderCmd   =  0.00,
            throttleCmd =  0.00,
            gearsDownCmd = 0)
    
class Model():
    """Data source to drive gauges screen"""
    def __init__(self, screen_size):
        self.scrSize = screen_size
        self.scrCenter = (self.scrSize[0]/2, self.scrSize[1]/2)
        self.height_Z1 = 0.0
        self.time_Z1 = time.time()
        self.dt = 0.1
        self.data = Buses()
        self.navion = AeroModel(dt=0.05, altInit_m=20.0, speed_fps=76.0, weight_lbs=2750, units="Metric")
        self.test   = TestModel(dt=0.05, altInit_m=100.0, speed_fps=76.0, weight_lbs=2750, units="Metric")
        self.rud = 0.0
        
    def step(self, test=False):
        """Generate and return new set of data"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting....')
                sys.exit()   # end program.
        data = self.data
        t = time.time()
        self.dt = t -self.time_Z1
        self.time_Z1 = t
        data.time += self.dt
        
        ### FLIGHT CONTROLS AND THROTTLE
        keys = pygame.key.get_pressed()
        cmds  = data.cmds
        data.mousePos_Z1 = data.mousePos
        data.mousePos = (getMouse())["pos"]
        cmds.aileronCmd  = 2*(data.mousePos[0]/self.scrSize[0] -0.5) #< Stick left is negative
        cmds.elevatorCmd = 2*(data.mousePos[1]/self.scrSize[1] -0.5) #< Stick up is negative

        self.rud = min(1, max(-1, self.rud -0.01*(keys[pygame.K_z] -keys[pygame.K_c]))) #< Rudder left is negative
        self.rud *= (1 -keys[pygame.K_x])
        cmds.rudderCmd = max(-1, min(1, 0.1*cmds.aileronCmd +self.rud))

        throttle = cmds.throttleCmd +0.02*(keys[pygame.K_q] -keys[pygame.K_a])
        cmds.throttleCmd = max(0, min(1, throttle))

        gearsDown = cmds.gearsDownCmd +(keys[pygame.K_b] -keys[pygame.K_g])
        cmds.gearsDownCmd = max(0, min(1, gearsDown))

        ### STEP MODEL
        self.physics(test)

        ### WEIGHT ON WHEELS
        state = data.state
        state.wowLeft  |= bool(keys[pygame.K_1])
        state.wowNose  |= bool(keys[pygame.K_2])
        state.wowRight |= bool(keys[pygame.K_3])

        return data

    def physics(self, mode) -> None:
        if mode == "arcade":
            mdl = self.test
        elif mode == "navion":
            mdl = self.navion
        else:
            mdl = None

        mdl.step(self.data.cmds, dt=self.dt)

        ### Ground collision detection
        if -mdl.position.z < 0.0:
            mdl.position.z = 0.0
            mdl.Ve.z = min(0.0, mdl.Ve.z) #< Only negative (up)
            mdl.W.p = 0.0
            mdl.Ab.z = 0

            pitch_r = mdl.attitude.pitch_r
            if pitch_r >= 0.0:
                ### Nose up
                pitch_r = min(0.3, pitch_r) #< 17 deg 
                mdl.attitude.set( 0.0, pitch_r, mdl.attitude.yaw_r )
            else:
                ### Nose down
                mdl.attitude.set( 0.0, 0.0, mdl.attitude.yaw_r )
                mdl.W.q = max(0.0, mdl.W.q) #< Only pitch up

        ### Update state bus
        state = self.data.state
        state.latY_m   =  mdl.position.x
        state.lonX_m   =  mdl.position.y
        state.hae_m    = -mdl.position.z

        state.velNorth_mps =  mdl.Ve.x
        state.velEast_mps  =  mdl.Ve.y
        state.velUp_mps    = -mdl.Ve.z

        state.accForward_mps2 =  mdl.Ab.x
        state.accRight_mps2   =  mdl.Ab.y
        state.accUp_mps2      = -mdl.Ab.z

        state.roll_r    = mdl.attitude.roll_r
        state.pitch_r   = mdl.attitude.pitch_r
        state.azimuth_r = mdl.attitude.yaw_r

        state.roll_rps    = mdl.W.p
        state.pitch_rps   = mdl.W.q
        state.azimuth_rps = mdl.W.r

        radToDeg = 180/pi
        state.fcsAileron_deg     = mdl.aileronCmd*radToDeg
        state.fcsElevator_deg    = mdl.elevatorCmd*radToDeg
        state.fcsRudder_deg      = mdl.rudderCmd*radToDeg
        state.fcsFlaps_deg       = 0.0*radToDeg
        state.fcsSpeedbrakes_deg = 0.0*radToDeg
        state.throttleFbk        = self.data.cmds.throttleCmd
        state.thrust             = mdl.Thrust_N
        state.aoa_deg            = mdl.alpha_r*radToDeg
        state.beta_deg           = mdl.beta_r*radToDeg

        state.gearsDownFbk       = mdl.gearsDownCmd

        ### Weight On Wheels (WOW) detection
        state.wowLeft   = (state.hae_m < 0.2) and (state.roll_r < 0.01)
        state.wowRight  = (state.hae_m < 0.2) and (state.roll_r > -0.01)
        state.wowNose   = (state.hae_m < 0.2) and (state.pitch_r < 0.01)
