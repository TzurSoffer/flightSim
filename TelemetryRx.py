"""
 * TelemetryRx.py
 * Created on: 8 April 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

import math, sys, time
import pygame
from GSOF_Cockpit.GraphicsLib import getMouse

from bus.BusINS import *
from bus.BusFcsCmds import *
from flightmodel import AeroModel, Controls
from flightmodel_ut import AeroModel as TestModel

from math import pi
radToDeg = 180/pi

class Wow():
    def __init__(self):
        self.left  = False
        self.right = False
        self.nose  = False

    def print(self):
        print("%d, %d, %d"%(self.left, self.nose, self.right))

class Buses():
    def __init__(self):
        self.mousePos     = (0,0)
        self.mousePos_Z1  = self.mousePos

        self.ins    = BusINS()
        self.cmds   = BusFcsCmds()
        self.time   = 0.0
        self.wow    = Wow()
        self.ctrls = Controls(
            Elevator_Cmd =  0.00,
            Aileron_Cmd  =  0.00,
            Rudder_Cmd   =  0.00,
            Throttle_Cmd =  0.00,
            GearExtend_Cmd = 0)
    
class Data():
    """Data source to drive gauges screen"""
    def __init__(self, screen_size):
        self.scrSize = screen_size
        self.scrCenter = (self.scrSize[0]/2, self.scrSize[1]/2)
        self.height_Z1 = 0.0
        self.time_Z1 = time.time()
        self.dt = 0.1
        self.data = Buses()
        self.navion = AeroModel(dt=0.05, altInit_m=0*20.0, speed_fps=0*76.0, weight_lbs=2750, units="Metric")
        self.test   = TestModel(dt=0.05, altInit_m=100.0, speed_fps=76.0, weight_lbs=2750, units="Metric")
        self.rud = 0.0
        
    def getData(self, test=False):
        """Generate and return new set of data"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Exiting....')
                sys.exit()   # end program.
        t = time.time()
        self.dt = t -self.time_Z1
        self.time_Z1 = t
        m_data = self.data
        cmds = m_data.cmds
        
        # Interactive test mode
        m_data.time += self.dt
        keys = pygame.key.get_pressed()

        ### FLIGHT CONTROLS AND THROTTLE
        m_data.mousePos_Z1 = m_data.mousePos
        m_data.mousePos = (getMouse())["pos"]
        roll = 2*(m_data.mousePos[0]/self.scrSize[0] -0.5) #< Stick left is negative
        elev = -2*(m_data.mousePos[1]/self.scrSize[1] -0.5) #< Stick up is negative
        self.rud = min(1, max(-1, self.rud -0.01*(keys[pygame.K_z] -keys[pygame.K_c]))) #< Rudder left is negative
        self.rud *= (1 -keys[pygame.K_x])
        cmds.rudderCmd_d = max(-1, min(1, 0.2*roll +self.rud))
        sb   = 0.5

        throttle = cmds.throttleCmd +0.02*(keys[pygame.K_q] -keys[pygame.K_a])
        cmds.throttleCmd = max(0, min(1, throttle))

        gearsDown = cmds.gearExtendCmd_b +(keys[pygame.K_b] -keys[pygame.K_g])
        cmds.gearExtendCmd_b = max(0, min(1, gearsDown))

        self.data.ctrls.Elevator_Cmd = -elev
        self.data.ctrls.Aileron_Cmd  =  roll
        self.data.ctrls.Rudder_Cmd   = cmds.rudderCmd_d
        self.data.ctrls.Throttle_Cmd = cmds.throttleCmd
        self.data.ctrls.GearExtend_Cmd = cmds.gearExtendCmd_b

        ### 6DOF MODEL
        self.physics(test)

        cmds.lElevonCmd_d = 25*(-roll +elev)
        cmds.rElevonCmd_d = 25*(+roll +elev)
        cmds.rudderCmd_d *= 25

        ### WEIGHT ON WHEELS
        m_data.wow.left  = bool(keys[pygame.K_1])
        m_data.wow.nose  = bool(keys[pygame.K_2])
        m_data.wow.right = bool(keys[pygame.K_3])

        ### Weight On Wheels (WOW) detection
        m_data.wow.left   |= (m_data.ins.height < 0.2) and (m_data.ins.roll < 0.5)
        m_data.wow.right  |= (m_data.ins.height < 0.2) and (m_data.ins.roll > -0.5)
        m_data.wow.nose   |= (m_data.ins.height < 0.2) and (m_data.ins.pitch < 0.5)

        return m_data

    def physics(self, mode) -> None:
        if mode == "arcade":
            mdl = self.test
        elif mode == "navion":
            mdl = self.navion
        else:
            mdl = None
    
        mdl.step(self.data.ctrls, dt=self.dt)

        ### Update instrumentation
        ins = self.data.ins
        ins.roll    = radToDeg*mdl.attitude.roll_r
        ins.pitch   = radToDeg*mdl.attitude.pitch_r
        ins.azimuth = radToDeg*mdl.attitude.yaw_r

        #mdl.position.print()
        ins.north      =  mdl.position.x
        ins.east       =  mdl.position.y
        ins.height     =  -mdl.position.z

        ins.vel_north  =  mdl.Ve.x
        ins.vel_east   =  mdl.Ve.y
        ins.vel_up     =  -mdl.Ve.z

        ins.forwardAcc =  mdl.Ab.x
        ins.rightAcc   =  mdl.Ab.y
        ins.upAcc      =  -mdl.Ab.z

        airSpeed = mdl.Vb.mag()
        ins.mach = airSpeed*0.002

        ### Ground collision detection
        if ins.height < 0.0:
            mdl.position.z = 0.0
            mdl.Ve.z = min(0.0, mdl.Ve.z) #< Only negative (up)
            mdl.W.p = 0.0
            ins.upAcc = 0

            pitch_r = mdl.attitude.pitch_r
            if pitch_r >= 0.0:
                ### Nose up
                pitch_r = min(0.3, pitch_r) #< 17 deg 
                mdl.attitude.set( 0.0, pitch_r, mdl.attitude.yaw_r )
            else:
                ### Nose down
                mdl.attitude.set( 0.0, 0.0, mdl.attitude.yaw_r )
                mdl.W.q = max(0.0, mdl.W.q) #< Only pitch up
