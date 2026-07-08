import struct

class State():
    def __init__(self):
        self.timeTag_ms = 0 #< UINT32 Elapsed Time (msec)

        self.latY_m = 0.0  #< Double Latitude (m)
        self.lonX_m = 0.0  #< Double Longitude (m)
        self.hae_m  = 0.0  #< Float Height above earth (m)

        self.velNorth_mps = 0.0  #< Float Velocity North (m/s)
        self.velEast_mps  = 0.0  #< Float Velocity East (m/s)
        self.velDown_mps  = 0.0  #< Float Velocity downward (m/s)

        self.accForward_mps2 = 0.0  #< Float Accelaration forward (m/s^2)
        self.accRight_mps2   = 0.0  #< Float Accelaration right (m/s^2)
        self.accDown_mps2    = 0.0  #< Float Accelaration down (m/s^2)

        self.roll_r    = 0.0  #< Float Right-handed rotation around Y-axis (rad)
        self.pitch_r   = 0.0  #< Float Right-handed rotation around X-axis (rad)
        self.heading_r = 0.0  #< Float Right-handed rotation around z-axis clockwise from North

        self.roll_rps    = 0.0  #< Float Right-handed rotation rate around Y-axis (rad)
        self.pitch_rps   = 0.0  #< Float Right-handed rotation rate around X-axis (rad)
        self.yaw_rps     = 0.0  #< Float Right-handed rotation rate around z-axis clockwise from North

        self.fcsAileron_deg     = 0.0  #< Float 
        self.fcsElevator_deg    = 0.0  #< Float 
        self.fcsRudder_deg      = 0.0  #< Float 
        self.fcsFlaps_deg       = 0.0  #< Float 
        self.fcsSpeedbrakes_deg = 0.0  #< Float 
        self.throttleFbk  = 0.0  #< Float 0.0 to 1.0
        self.thrust_N= 0.0    #< Float
        self.fuelLevel = 0.0  #< Float 0.0 to 1.0
        self.aoa_deg= 0.0    #< Float
        self.beta_deg= 0.0    #< Float
        self.gearsDownFbk = 0    #< UINT8
        self.wowNose = 0    #< UINT8
        self.wowLeft = 0    #< UINT8
        self.wowRight= 0    #< UINT8

    def serialize(self) ->bytes:
        serialized = []
        serialized.append(struct.pack('<I', self.timeTag_ms))
        
        serialized.append(struct.pack('<d', self.latY_m))
        serialized.append(struct.pack('<d', self.lonX_m))
        serialized.append(struct.pack('<f', self.hae_m))
        
        serialized.append(struct.pack('<f', self.velNorth_mps))
        serialized.append(struct.pack('<f', self.velEast_mps))
        serialized.append(struct.pack('<f', self.velDown_mps))
        
        serialized.append(struct.pack('<f', self.accForward_mps2))
        serialized.append(struct.pack('<f', self.accRight_mps2))
        serialized.append(struct.pack('<f', self.accDown_mps2))
        
        serialized.append(struct.pack('<f', self.roll_r))
        serialized.append(struct.pack('<f', self.pitch_r))
        serialized.append(struct.pack('<f', self.heading_r))
        
        serialized.append(struct.pack('<f', self.roll_rps))
        serialized.append(struct.pack('<f', self.pitch_rps))
        serialized.append(struct.pack('<f', self.yaw_rps))
        
        serialized.append(struct.pack('<f', self.fcsAileron_deg))
        serialized.append(struct.pack('<f', self.fcsElevator_deg))
        serialized.append(struct.pack('<f', self.fcsRudder_deg))
        serialized.append(struct.pack('<f', self.fcsFlaps_deg))
        serialized.append(struct.pack('<f', self.fcsSpeedbrakes_deg))
        serialized.append(struct.pack('<f', self.throttleFbk))
        serialized.append(struct.pack('<f', self.thrust_N))
        serialized.append(struct.pack('<f', self.fuelLevel))
        serialized.append(struct.pack('<f', self.aoa_deg))
        serialized.append(struct.pack('<f', self.beta_deg))
        
        serialized.append(struct.pack('<B', self.gearsDownFbk))
        serialized.append(struct.pack('<B', self.wowNose))
        serialized.append(struct.pack('<B', self.wowLeft))
        serialized.append(struct.pack('<B', self.wowRight))
        return b''.join(serialized)

    def deserialize(self, buf) -> None:
        offset = 0
        self.timeTag_ms = struct.unpack_from('<I', buf, offset)[0]
        offset += 4
        
        self.latY_m = struct.unpack_from('<d', buf, offset)[0]
        offset += 8
        self.lonX_m = struct.unpack_from('<d', buf, offset)[0]
        offset += 8
        self.hae_m = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        
        self.velNorth_mps = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.velEast_mps = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.velDown_mps = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        
        self.accForward_mps2 = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.velRight_mps2 = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.accDown_mps2 = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        
        self.roll_r = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.pitch_r = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.heading_r = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        
        self.roll_rps = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.pitch_rps = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.yaw_rps = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        
        self.fcsAileron_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.fcsElevator_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.fcsRudder_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.fcsFlaps_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.fcsSpeedbrake_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.throttleFbk = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.thrust_N = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.fuelLevel = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.aoa_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        self.beta_deg = struct.unpack_from('<f', buf, offset)[0]
        offset += 4
        
        self.gearsDownFbk = struct.unpack_from('<B', buf, offset)[0]
        offset += 1
        self.wowNose = struct.unpack_from('<B', buf, offset)[0]
        offset += 1
        self.wowLeft = struct.unpack_from('<B', buf, offset)[0]
        offset += 1
        self.wowRight = struct.unpack_from('<B', buf, offset)[0]
        offset += 1

    def __str__(self):
        s = ""
        s += "Elapsed Time (msec): %d\n"%self.timeTag_ms 

        s += "Latitude-Y (m): %1.6f\n"%self.latY_m
        s += "Longitude-X (m): %1.6f\n"%self.lonX_m
        s += "Height above earth (m): %1.2f\n"%self.hae_m 

        s += "Velocity North (m/s): %1.2f\n"%self.velNorth_mps
        s += "Velocity East (m/s): %1.2f\n"%self.velEast_mps
        s += "Velocity downward (m/s): %1.2f\n"%self.velDown_mps

        s += "Accelaration forward (m/s^2): %1.2f\n"%self.accForward_mps2
        s += "Accelaration right (m/s^2): %1.2f\n"%self.accRight_mps2
        s += "Accelaration down (m/s^2): %1.2f\n"%self.accDown_mps2

        s += "Roll (rad): %1.2f\n"%self.roll_r
        s += "Pitch (rad): %1.2f\n"%self.pitch_r
        s += "Heading (rad): %1.2f\n"%self.heading_r

        s += "Roll rate (rps): %1.2f\n"%self.roll_rps
        s += "Pitch rate (rps): %1.2f\n"%self.pitch_rps
        s += "Yaw rate (rps): %1.2f\n"%self.yaw_rps

        s += "Aileron (deg): %1.2f\n"%self.fcsAileron_deg
        s += "Elevator (deg): %1.2f\n"%self.fcsElevator_deg
        s += "Rudder (deg): %1.2f\n"%self.fcsRudder_deg
        s += "Flaps (deg): %1.2f\n"%self.fcsFlaps_deg
        s += "Speedbrakes (deg): %1.2f\n"%self.fcsSpeedbrakes_deg
        s += "Throttle (%%): %1.2f\n"%(self.throttleFbk*100)
        s += "Thrust (N): %1.2f\n"%(self.thrust_N)
        s += "Fuel (%%): %1.2f\n"%(self.fuelLevel*100)
        s += "AOA (deg): %1.2f\n"%(self.aoa_deg)
        s += "Beta (deg): %1.2f\n"%(self.beta_deg)
        
        s += "Gears down (bool): %d\n"%self.gearsDownFbk
        s += "WOW nose (bool): %d\n"%self.wowNose
        s += "WOW left (bool): %d\n"%self.wowLeft
        s += "WOW right(bool): %d\n"%self.wowRight
        return s
        
if __name__ == "__main__":
    bus = State()
    bus.timeTag_ms = 123
    bus.latY_m = 345.0  #< latitude  (m)
    bus.lonX_m = 678.0  #< longitude (m)
    bus.hae_m  = 1023.0  #< height above earth (m)

    bus.velNorth_mps = 11.0  #< Velocity North (m/s)
    bus.velEast_mps  = 12.0  #< Velocity East (m/s)
    bus.velDown_mps  = 13.0  #< Velocity downward (m/s)

    bus.accForward_mps2 = 0.1  #< Accelaration forward (m/s^2)
    bus.accRight_mps2   = 0.2  #< Accelaration right (m/s^2)
    bus.accDown_mps2    = 0.3  #< Accelaration down (m/s^2)

    bus.roll_r    = 1.2  #< Right-handed rotation around Y-axis (rad)
    bus.pitch_r   = 2.3  #< Right-handed rotation around X-axis (rad)
    bus.heading_r = 2.1  #< Right-handed rotation around z-axis clockwise from North

    bus.roll_rps    = 0.5  #< Right-handed rotation rate around Y-axis (rad)
    bus.pitch_rps   = 0.6  #< Right-handed rotation rate around X-axis (rad)
    bus.yaw_rps     = 0.7  #< Right-handed rotation rate around z-axis clockwise from North

    bus.fcsAileron_deg     =  5.0  #< 
    bus.fcsElevator_deg    = -5.0  #< 
    bus.fcsRudder_deg      =  2.5  #< 
    bus.fcsSpeedbrakes_deg = 45.0
    bus.fcsFlaps_deg = 15.0
    bus.throttleFbk = 0.99
    bus.thrust_N = 120
    bus.fuelLevel = 0.573
    bus.aoa_deg = 7.6
    bus.beta_deg = 1.5
    
    bus.gearsDownFbk = 1
    bus.wowNose  = 0
    bus.wowLeft  = 1
    bus.wowRight = 0
    pkt = bus.serialize()
    bus.deserialize(pkt)
    print(bus)
