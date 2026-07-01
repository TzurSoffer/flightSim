class Params():
    ## Constants
    UNITS = "Imperial"
    G     =  32.1740  #< ft/sec^2
    #G     =  9.81     #< m/sec^2

#    FTStoKNOTS = 0.592      #< ft/sec = 0.592 knots
#    dt = 0.01 #< Time step for integration (s)
#    MAX_DELTA_E = 10.0  #< Max elevator deflection (degrees)
#    THRTL_INIT = 0.7

    ELV_TRIM_D    =  0.0 #< degrees
    ELV_MAX_ANG_D = 20.0 #< degrees

    AIL_TRIM_D    =  0.0 #< degrees
    AIL_MAX_ANG_D = 30.0 #< degrees

    RUD_TRIM_D    =  0.0 #< degrees
    RUD_MAX_ANG_D = 20.0 #< degrees

    MAX_THRUST = 360.0*3  #< Thrust in lbs_F
    #MAX_THRUST = 1601.36  #< Thrust in Newtons

    ALT_INIT    = 5000.0
    #ALT_INIT    = 1500.0 #< meters
    V_CRUISE    = 210.0 #< Cruise speed (ft/s) 170 mph 147.8 knots
    #V_CRUISE     = 76.0 #< Cruise speed (m/s)


#    RHO_0 = 0.002377  #< Air density (slugs/ft³)
#    #RHO_0 1.2041     #<[kg/m3] #< density of air( at sea level and standard pressure )
#    RHO_0_m = 1.2041        #<[kg/m3] #< density of air( at sea level and standard pressure )
    RHO_10000 = 0.001756
    RHO = RHO_10000


    ## Aircraft Parameters
    _Ixx        =  948.0 #< Roll inertia
    #_Ixx        = 1285.0 #< Roll inertia (kg*m^2)
    _Iyy        = 1346.0 #< Pitch inertia ( slugs*ft^2 )
    #_Iyy        = 1824.0 #< Pitch inertia ( kg*m^2 )
    _Izz        = 1967.0 #< Yaw inertia
    #_Izz        = 2666.0 #< Yaw inertia ( kg*m^2 )

    WEIGHT      = 2750.0 #< lbs
    #WEIGHT      = 1247.0 #< Kg
    MASS        = (WEIGHT/G) #< Aircraft mass

    _C          =   4.9 #< Mean aerodynamic chord (ft)
    #_C          =   1.49 #< Mean aerodynamic chord (m)
    _S          = 184.0 #< Main Wing area (ft^2)
    #_S          =  17.0 #< Wing area (m^2)
    _B          =  33.4 #< Rudder Wing area (ft^2)
    #_B          =   3.07 #< Wing area (m^2)

    ## Aerodynamic Parameters (dimentionless)
    CL_0       = 0.270   #< Lift coefficient 0.27, 0.38
    CD_0       = 0.025   #< Drag coefficient
    G_CD_0     = 0.025   #< Drag coefficient
    K          = 0.061   #< Induced Drag Factor

    CL_ALPHA    = 4.44   #< Lift coefficient slope due to AoA (per radian)
#    CL_DELTA_E = 0.335   #< -0.923 Lift coefficient slope due to elevator deflection (per radian)


    CM_0       =  0.0    #< Baseline pitching moment coefficient
    GM_0       = -0.2    #< Baseline pitching moment coefficient
    CM_Q       = -0.7    #< Pitch damping coefficient#-0.7, -0.15
    CM_DELTA_E = -0.923  #< Pitching moment slope due to elevator deflection (per radian)
    CM_ALPHA   = -0.683  #< Pitching moment slope due to AoA (per radian)

    Cl_0       =  0.0    #< Roll, Zero-control moment ( typically small or zero in symmetric flight )
    Cl_DA      = -0.134  #< Roll, Aileron effectiveness 9 change in Cl per radian of aileron deflection )
    Cl_P       = -0.410  #< Roll, Damping ( change in Cl per unit of roll rate )
    Cl_R       =  0.107  #< Roll, Yaw-roll coupling ( change in Cl per unti of yaw rate )

    CN_0       = -0.0    #< Yaw, sideslip moment, yaw stability
    CN_b       =  0.0907 #< Yaw, sideslip moment, yaw stability
    CN_p       = -0.0649 #< Yaw, roll-rate moment, rikk-yaw coupling
    CN_r       = -0.1199 #< Yaw, yaw-rate moment, yaw damping
    CN_dr      = -0.0805 #< Yaw, rudder deflection moment, rudder effectiveness
    CN_da      = -0.0504 #< Yaw, aileron defection moment, aileron inducted yaw

    CY_B       = -0.404  #< Side Slip Beta
    CY_DELTA_R =  0.185  #<
    CY_r       =  0.267  #<
    CY_p       = -0.145  #<
