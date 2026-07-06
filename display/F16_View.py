import os, math
from display.objects.F16_assy import F16
try:
    from GSOF_3dWireFrame.Lib3D.Object_WireFrame import Object_wireFrame as Object
    from GSOF_3dWireFrame.Lib3D.Assembly import Assembly
    from GSOF_3dWireFrame.Lib3D import Objects
    from GSOF_Cockpit.Wireframe3D.Model3D import Model3D
except:
   _3D_active = False
   print("GSOF_Wireframe3D module isn't installed")

PI = math.pi

class WorldState():
    def __init__(self,
                 scale=(1,1,1),
                 rotate=(0,0,0),
                 translate=(0,0,0)):
        self.scale = scale
        self.rotate = rotate
        self.translate = translate

class PlaneState():
    def __init__(self,
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
        self.north = north
        self.east = east
        self.up = up
        self.heading_d = heading_d
        self.pitch_d = pitch_d
        self.roll_d = roll_d
        self.leftAileron_d = leftAileron_d
        self.rightAileron_d = rightAileron_d
        self.leftElevator_d = leftElevator_d
        self.rightElevator_d = rightElevator_d
        self.rudder_d = rudder_d
        self.speedbrake_d = speedbrake_d
        self.throttle = throttle
        self.gearsDown_b = gearsDown_b
        self.wowNose_b = wowNose_b
        self.wowLeft_b = wowLeft_b
        self.wowRight_b = wowRight_b
                 
class F16_View():
    """Constructs X"""
    def __init__(self, screen, pos, size, frame, folder):
        ###Initialise the gauges.
        objPath = os.path.join(folder, "objects")
        self.plane = F16(folder=folder)
        net = Object(obj=Objects.net(40,40), color=(0,100,0), name="NET")\
                 .setCenter(pos=(-50, 4050, 0), rotate=(PI/2, 0, 0), scale=4.0 )
        axis = Object(filename=os.path.join(objPath,"Axis.json"), color=(10,10,10), name="WorldAxis" )\
           .scale(30.0)\
           .setOrigin()

        sun = Object(obj=Objects.sphere(500, 15, color=(225,220,50)), name="SUN")
        sun.setCenter(scale=0.15, rotate=(PI/2,0,0))
        sun.translate(0, 3000, 0)  #< More up (Y) and forward (Z) to the center of the net 
        sun.setOrigin()

        self.world = Assembly(
            objects=(Assembly(objects=(net, axis), name="Ground").translate(0, 0, 0).setOrigin(),
                     Assembly(objects=[self.plane], name="Plane").translate(0,35,0).setOrigin(),
                     sun),
            name="World")    
        self.world.rotate(0, 0, 0).translate(0,0,0).setOrigin()

        self.model = Model3D(
        screen,
        pos=pos,
        size=size,
        world=self.world,
        bodyImage=frame,
        scale=500, minViewDistance=50, maxViewDistance=5000
        )

    def update(self, time, planeState, worldState) -> None:
        self.model.reset()
        self._updateWorld(worldState.scale,
                          worldState.rotate,
                          worldState.translate)
        self._updatePlane(planeState)

    def _updateWorld(self, scale, rotation, translation) -> None:
        """ """
        #self.world.transform(scale=scale, rotate=rotation, translate=translation) #< TODO BUG IN ROTATION ORDER
        self.world.translate(*translation).rotate(*rotation) 
        #self.world.rotate(*rotation).translate(*translation) 

    def _updatePlane(self, state) -> None:
        """ """
        self.plane._update(
            north=state.north, east=state.east, up=state.up,
            heading_d=state.heading_d, pitch_d=state.pitch_d, roll_d=state.roll_d,
            throttle=state.throttle,
            gearsDown_b=state.gearsDown_b,
            wowNose_b=state.wowNose_b, wowLeft_b=state.wowLeft_b, wowRight_b=state.wowRight_b)

    def draw(self):
        """Draw all the dials. The update method should be called before to update all gauges"""
        self.model.draw()
