class BusINS():
    def __init__(self):
        self.lat = 0.0    #< Latitude (deg)
        self.long = 0.0   #<Longitude (deg)
        self.height = 0.0 #<Height (m)
        self.vel_north = 0.0 #<Velocity north (m/s)
        self.vel_east = 0.0 #< Velisity east (m/s)
        self.vel_up = 0.0 #< Velosity up (m/s)
        self.roll = 0.0 #< Roll angle (deg) Right-handed rotation around y-axis
        self.pitch = 0.0 #< Pitch angle (deg) Right-handed rotation around x-axis
        self.azimuth = 0.0 #< Azimuth (deg) Left-handed rotation around z-axis clockwise from North
        self.pitchRate = 0.0 #< Pitch Rate (rad/s)
        self.rollRate = 0.0 #< Roll Rate (rad/s)
        self.yawRate = 0.0 #< Yaw Rate (rad/s)
        self.rightAcc = 0.0 #< Right Acceleration (m/s^2)
        self.forwardAcc = 0.0 #< Forward Acceleration (m/s^2)
        self.upAcc = 0.0 #< Up Acceleration (m/s^2)
        self.mach = 0.0 #< Mach number estimated
