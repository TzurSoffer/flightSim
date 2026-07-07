class Params():
    ## Constants
    G          = 9.81      #< m/sec^2
    WEIGHT     = 1247.0    #< Kg
    MAX_THRUST = 163.0*3   #< Thrust in Newtons
    MASS       = WEIGHT/G  #< Aircraft mass

    ALT_INIT    = 1500.0 #< meters
    V_CRUISE    = 76.0   #< Cruise speed (m/s)

    ELV_TRIM_D    =  0.0 #< degrees
    ELV_MAX_ANG_D = 20.0 #< degrees

    AIL_TRIM_D    =  0.0 #< degrees
    AIL_MAX_ANG_D = 30.0 #< degrees

    RUD_TRIM_D    =  0.0 #< degrees
    RUD_MAX_ANG_D = 20.0 #< degrees

    ## Aircraft Parameters
    _Ixx        = 1285.0 #< Roll inertia (kg*m^2)
    _Iyy        = 1825.0 #< Pitch inertia ( kg*m^2 )
    _Izz        = 2667.0 #< Yaw inertia ( kg*m^2 )

    _C          = 1.49 #< Mean aerodynamic chord (m)
    _S          = 17.0 #< Wing area (m^2)
    _B          = 3.07 #< Wing area (m^2)

    ## Aerodynamic Parameters (dimentionless)
    CL_0       = 0.270   #< Lift coefficient 0.27, 0.38
    CD_0       = 0.025   #< Drag coefficient
    G_CD_0     = 0.025   #< Drag coefficient
    K          = 0.061   #< Induced Drag Factor

    CL_ALPHA    = 4.44   #< Lift coefficient slope due to AoA (per radian)
    #CL_DELTA_E = 0.335  #< -0.923 Lift coefficient slope due to elevator deflection (per radian)


    CM_0       =  0.0    #< Baseline pitching moment coefficient
    GM_0       = -0.05   #< Baseline pitching moment coefficient
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
