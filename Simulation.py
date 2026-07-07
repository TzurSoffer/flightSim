#!/usr/bin/python
"""
 * Simulation.py
 * Created on: 19 June 2026
 * Improved for: 21 June 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

import sys, os, random
from math import pi, cos, sin, atan, atan2, sqrt
from GSOF_Cockpit.Aerospace import ArtificialHorizon as AH
from GSOF_Cockpit.Aerospace import TurnCoordinator_Analog as TC
from GSOF_Cockpit.Aerospace import AltMeter_Analog as ALT
#from GSOF_Cockpit.Aerospace import MachMeter_Analog as MACH
from GSOF_Cockpit.Aerospace import GMeter_Analog as G
from GSOF_Cockpit.Aerospace import AirSpeedMeter_Analog as AS
from GSOF_Cockpit.Aerospace import VsiMeter_Analog as VSI
from GSOF_Cockpit.Aerospace import Heading_Analog as HEAD
from GSOF_Cockpit.Generic import Map as MAP

##from GSOF_Cockpit.Button import Button_Rect
from GSOF_Cockpit.Text import Text
from GSOF_Cockpit.GraphicsLib import imageLoad, getScreen, init, fillScreen, update
from GSOF_Cockpit import Pygame_Colors as COLOR
from GSOF_Cockpit.Clock_base import Clock

from display.F16_View import F16_View, PlaneState, WorldState

class CockpitView():
    """Constructs the gauges screen"""
    def __init__(self, screen, pos=(0,0), scale=1.0, colorBG=COLOR.BLACK, gap=0, folder='./'):
        self.cameraMode = "follow"   
        #self.cameraMode = "static"   
        #self.cameraMode = "chase"   
        #self.cameraMode = "pilot"   

        self.screen = screen
        self.colorBG = colorBG

        ###Scaling the indicators
        world_size   = (int(900*scale), int(300*scale))
        turn_size    = (int(150*scale), int(150*scale))
        horizon_size = (int(150*scale), int(150*scale))
        alt_size     = (int(150*scale), int(150*scale))
        vsi_size     = (int(150*scale), int(150*scale))
        head_size    = (int(150*scale), int(150*scale))
        as_size      = (int(150*scale), int(150*scale))
        mach_size    = (int(150*scale), int(150*scale))
        stick_size   = (int(150*scale), int(150*scale))
        minimap_size = (int(300*scale), int(300*scale))
        bckgnd_size  = (int(750*scale), int(600*scale))

        ###Positioning the gauges
        X0, Y0 = pos
        world_pos   = (X0 +gap, Y0 +gap)
        as_pos      = (world_pos[0] +0, world_pos[1] +world_size[1] +gap)
        horizon_pos = (as_pos[0] +as_size[0] +gap, as_pos[1])
        alt_pos     = (horizon_pos[0] +horizon_size[0] +gap, horizon_pos[1])
        mach_pos    = (alt_pos[0] +alt_size[0] +gap, alt_pos[1])
        minimap_pos = (mach_pos[0] +mach_size[0] +gap, mach_pos[1])

        turn_pos  = (as_pos[0], as_pos[1] +as_size[1] +gap)
        head_pos  = (turn_pos[0] +turn_size[0] +gap, turn_pos[1])
        vsi_pos   = (head_pos[0] +head_size[0] +gap, head_pos[1])
        stick_pos = (vsi_pos[0] +vsi_size[0] +gap, vsi_pos[1])

        ###Initialise the gauges.
        self.background = Text( screen=self.screen, pos=pos, size=bckgnd_size, color=colorBG, name='' )
        self.world = F16_View(
           self.screen,
           pos=world_pos,
           size=world_size,
           frame=imageLoad('%s/skin/Frame_Rect900x300.png'%folder),
           folder=os.path.join(folder,"display/")
           )

        self.airSpd  = AS.AirSpeedMeter( self.screen, pos=as_pos, size=as_size)
        self.horizon = AH.ArtificialHorizon( self.screen, pos=horizon_pos, size=horizon_size,
                                             rollToDeg=180/pi, pitchToDeg=180/pi)
        self.alt     = ALT.AltMeter( self.screen, pos=alt_pos, size=alt_size)    
        #self.mach    = MACH.MachMeter( self.screen, pos=mach_pos, size=mach_size )
        self.gm      = G.GMeter_Analog( self.screen, pos=mach_pos, size=mach_size )
        self.minimap = MAP.Map( screen, pos=minimap_pos, size=minimap_size,
                                kp = 0.9,
                                bodyImage=imageLoad("%s/skin/Frame_Rect.png" % path),
                                mapImage=imageLoad("%s/skin/Grid_White300x300.png" % path),
                                markerImage=imageLoad("%s/skin/f16_icon.png" % path),
                                )
        self.turn    = TC.TurnCoord( self.screen, pos=turn_pos, size=turn_size,
                                     turnRateToDeg=180/pi, #< 360 deg in 2 minutes should result in 20 deg
                                     slipToDeg=1.0)
        self.head    = HEAD.Heading( self.screen, pos=head_pos, size=head_size)
        self.vsi     = VSI.VsiMeter( self.screen, pos=vsi_pos, size=vsi_size)
        self.stck    = MAP.Map( screen, pos=stick_pos, size=stick_size,
                                kp = 0.9,
                                bodyImage   = imageLoad("%s/skin/Joystick_background_400.png"%path),
                                mapImage    = imageLoad("%s/skin/Grid_White300x300.png"%path),
                                markerImage = imageLoad("%s/skin/Joystick_handle_100.png"%path),
                                )

        self.time_Z1 = 0
        self.heading_Z1 = 0
        self.turnRate_rps = 0

    def update(self, newData):
        """
        Update all the dials. Usually done in a different rate then the actuale display refresh.
        Also each dial can have a behaviour model (e.g: LPF, Min/Max detectors, Moving-Average, Delay...) 
        """
        ins = newData.ins
        time = newData.time
        mpsToKnots = 1.944
        speed_knots = mpsToKnots*sqrt(ins.vel_north**2 +ins.vel_east**2 +ins.vel_up**2)
        if speed_knots > 900:
           speed_knots = 900

        heading = pi*ins.azimuth/180
        pitch   = pi*ins.pitch/180
        roll    = pi*ins.roll/180

        mToFt = 3.28
        alt_ft = mToFt*ins.height

        dt = time -self.time_Z1
        if dt > 0.005:
           self.turnRate_rps = (heading -self.heading_Z1)/dt
           self.heading_Z1 = heading
        self.time_Z1 = time
        
        cmds = newData.cmds
        throttle = cmds.throttleCmd
        accZ = ins.upAcc
        accX = ins.forwardAcc
        accY = ins.rightAcc
        sideslip = accY / (sqrt(accZ**2 +accX**2) +0.01) #< Missing g vector

        lElev = cmds.lElevonCmd_d
        rElev = cmds.rElevonCmd_d
        rollCmd =  -20*(lElev -rElev)/2
        pitchCmd = -10*(lElev +rElev)/2
        rudderCmd = cmds.rudderCmd_d
        wow  = newData.wow

        ### MODEL TO 3D-GRAPHICS
        ### X-FOWARD, Y-RIGHT, Z-DOWN TO X-RIGHT, Z-UP
        posFact = 1
        planeState = PlaneState(north=ins.north, east=ins.east, up=ins.height,
                                heading_d=-heading*180/pi, pitch_d=pitch*180/pi, roll_d=-roll*180/pi,
                                throttle=throttle,
                                gearsDown_b=cmds.gearExtendCmd_b,
                                wowNose_b=wow.nose,
                                wowLeft_b=wow.left,
                                wowRight_b=wow.right)

        if self.cameraMode == "chase":
            cameraDistance = 400
            worldState = WorldState(translate=(-ins.east, -ins.height, +ins.north), rotate=(0,heading,0)) #< Chase plane
            self.world.update( time, planeState, worldState)
            self.world.world.translate(0,-70,-cameraDistance)

        elif self.cameraMode == "pilot":
            cameraDistance = -50 #< Move forward
            worldState = WorldState(translate=(-ins.east, -ins.height, ins.north))
            self.world.update( time, planeState, worldState)
            self.world.world.rotate(0,heading,0)
            self.world.world.rotate(-pitch,0,0)
            self.world.world.rotate(0,0,roll)
            self.world.world.translate(0,-50,-cameraDistance)

        elif self.cameraMode == "follow":
            cameraDistance = 1000
            worldState = WorldState(translate=(-ins.east, -(ins.height +50), ins.north -cameraDistance)) #< Camera relative to airplane
            self.world.update( time, planeState, worldState)

        elif self.cameraMode == "above":
            cameraAltitude = 10000
            worldState = WorldState(translate=(-ins.east, -(ins.height +cameraAltitude), ins.north)) #< Camera follow from above
            self.world.update( time, planeState, worldState)
            self.world.world.rotate(pi/2,0,0) #< Look down

        elif self.cameraMode == "static":
            azimuth = atan2(ins.east, ins.north)
            distance = sqrt((ins.east**2) +(ins.north**2))
            if abs(distance) > 0.01: 
                elevation = atan(ins.height/distance)
            else:
                elevation = pi/2
            worldState = WorldState(translate=(0, 0, 0),rotate=(0, 0, 0)) #< TODO DEBUG ROTATION ORDER
            self.world.update( time, planeState, worldState) 
            self.world.world.rotate(0, azimuth, 0)    #< 1st azimuth
            self.world.world.rotate(-elevation, 0, 0) #< 2nd elevation
            self.world.world.translate(0, -50, 0)     #< 3rd camera height
        
        self.horizon.update( roll, pitch )
        self.turn.update( -self.turnRate_rps, sideslip )
        mToFt = 3.2808
        self.alt.update( ins.height)#*mToFt )
        #self.mach.update( ins.mach )
        self.gm.update( -9.8*(1 +ins.upAcc/9.81) )
        self.minimap.update(x=ins.east/100, y=-ins.north/100, deg=ins.azimuth)
        self.vsi.update( mToFt*60*ins.vel_up/1000 )
        self.head.update( ins.azimuth, ins.azimuth )
        self.airSpd.update( speed_knots )
        self.stck.update(x=rollCmd, y=pitchCmd, deg=rudderCmd*20)

    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.background.draw()
        self.world.draw()

        self.horizon.draw()
        self.turn.draw()
        self.alt.draw()
        #self.mach.draw()
        self.gm.draw()
        self.minimap.draw()
        self.vsi.draw()
        self.head.draw()
        self.airSpd.draw()
        self.stck.draw()

if __name__ == "__main__":
    import time, pygame
    from TelemetryRx import Data
    def help(mode):
        print("Simulation mode: %s"%mode)
        print("Move mouse to control elevator and ailerons")

        print("Press 'Q' and 'A' to increase and decrease throttle")
        print("Press 'G' and 'B' to retract and extend landing gears")
        print("Press 'Z' and 'C' to trim rudder, 'X' to reset")
        print("Press '1' to '3' to select point of view")

    # Initialise screen.
    BG_color = COLOR.DARK
    screen_size=(900,600)
    init()
    screen = getScreen(screen_size)
    fillScreen( screen, COLOR.WHITE )

    # Initialise Dials.
    path = './'
    cockpit = CockpitView(screen, colorBG=BG_color, scale=1.0, folder=path)
    data = Data(screen_size)
    clock = Clock()

    #mode = "arcade" # False, "navion", "arcade"
    mode = "navion" # False, "navion", "arcade"

    help(mode)
    calcFrame = 5
    while True:
        ###Loop to update gauges
        #T0 = time.time()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            cockpit.cameraMode = "chase"
        elif keys[pygame.K_2]:
            cockpit.cameraMode = "pilot"
        elif keys[pygame.K_3]:
            cockpit.cameraMode = "follow"
        elif keys[pygame.K_4]:
            cockpit.cameraMode = "above"
        elif keys[pygame.K_5]:
            cockpit.cameraMode = "static"
        
        newData = data.getData(test=mode)
        calcFrame -= 1
        if calcFrame == 0:
            calcFrame = 5
            cockpit.update(newData)
            cockpit.draw()
        else:
            ##print(time.time() -T0)
            update()
            clock.tick(Fs=100)
