"""
 * F16_assy.py
 * Created on: 6 Jan 2025
 * Improved for: 25 May 2026
 * Author: Guy Soffer
 * Copyright (C) 2026 Guy Soffer
"""

from math import pi
try:
    from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
    from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
    from GSOF_3dWireFrame.Lib3D import Objects
    _3D_active = True
except:
    _3D_active = False
    print("GSOF_Wireframe3D module isn't installed")

degToRad = pi/180

#YELLOW = (255,255,140)
YELLOW = (125,125,0)
BLACK  = (0,0,0)
RED    = (255,0,0)
GREEN  = (0,170,0)
BLUE   = (0,0,255)
GRAY   = (50,50,50)

class F16(Assembly):
    """Constructs the gauges screen"""
    def __init__(self, folder='./'):
        self.time = 0.0
        axis  = Object(
           filename="%s/objects/axis.json"%folder, color=GREEN)\
           .scale(50.0)\
           .translate(0, 0, 150)\
           .setOrigin()

        self.plane = Object(
            filename="%s/objects/f16.stl"%folder, color=BLUE, name="F16")\
            .setCenter(rotate=(0,pi,0), scale=1.0, method="arithCenter")
        
        self.plume = objects=Object(
           filename="%s/objects/Plume.json"%folder, color=RED)\
           .setCenter(scale=30, rotate=(0, 0, 0))
        plume = Assembly(objects=(self.plume,))   
        plume.translate(0, 0, +90).setOrigin()

        self.nw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="NW")
        self.nwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW, name="NWOW").setCenter(rotate=(0,pi,0))
        nw = Assembly(objects=(self.nw, self.nwow), name="NW-Assy")\
           .translate(0, -2, 0).scale(8).translate(0, -30, -80).setOrigin()           

        self.lw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="LW")
        self.lwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW).setCenter(rotate=(0,pi,0))
        lw = Assembly(objects=(self.lw, self.lwow), name="LW-Assy")\
           .translate(0, -2, 0).rotate(x=0, y=0, z=-degToRad*15)\
           .scale(8).translate(-14, -30, 0).setOrigin()           

        self.rw = Object(
           filename="%s/objects/LandingGear.json"%folder, color=BLACK, name="RW")
        self.rwow = Object(
           filename="%s/objects/Spark.json"%folder, color=YELLOW).setCenter(rotate=(0,pi,0))
        rw = Assembly(objects=(self.rw, self.rwow), name="RW-Assy")\
           .translate(0, -2, 0).rotate(x=0, y=0, z=degToRad*15)\
           .scale(8).translate(14, -30, 0).setOrigin()           

        self.gears = Assembly(objects=(nw, rw,lw))
        super().__init__(objects=(axis, self.plane, plume, self.gears))

    def _update( self,
                north=0, east=0, up=0,
                heading_d=0, pitch_d=0, roll_d=0,
                leftAileron_d=0, rightAileron_d=0,
                leftElevator_d=0, rightElevator_d=0,
                rudder_d=0, speedbrake_d=0,
                throttle=0,
                gearsDown_b=True,
                wowNose_b=False,
                wowLeft_b=False,
                wowRight_b=False):
        """Update all elements"""
        self.time += 0.1
        self.setFCS(leftAileron_d,  rightAileron_d,
                    leftElevator_d, rightElevator_d,
                    rudder_d,
                    speedbrake_d)
        self.setExahustPlume(throttle)
        self.setGears(gearsDown_b)
        self.setWOW(wowNose_b, wowLeft_b, wowRight_b)
        self.setAttitude(heading_d, pitch_d, roll_d)
        self.setPosition(north, east, up)
       
    def setAttitude(self, heading, pitch, roll) -> None:
        self.rotate( y= heading*degToRad,
                     x= pitch*degToRad,
                     z= roll*degToRad )

    def setPosition(self, north, east, up) -> None:
        self.translate(east, up, -north)

    def setExahustPlume(self, plume) -> None:
        if plume > 1:
            plume = 1
        elif plume < 0:
            plume = 0
        plumeColor = (255, 255*(1-plume), 255*(1-plume))
        self.plume.rotate(x=0, y=0, z=self.time*plume)
        self.plume.scale(plume).color = plumeColor
       
    def setFCS(self, lAileron_deg, rAileron_deg, lElevator, rElevator, rudder_deg, sb_deg) -> None:
        self.nw.rotate(0,-degToRad*rudder_deg,0)
      
    def setGears(self, downCmd) -> None:
        if downCmd == False:
           self.gears.scale(0.0)
        else:
           self.gears.scale(1.0)

    def setWOW(self, nose, left, right) -> None:
        self.nwow.rotate(x=0, y=0, z=4*self.time).scale(int(nose))
        self.lwow.rotate(x=0, y=0, z=4*self.time).scale(int(left))
        self.rwow.rotate(x=0, y=0, z=4*self.time).scale(int(right))
