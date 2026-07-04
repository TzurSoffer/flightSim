from math import pi, sin, asin, cos, atan, atan2, sqrt
from typing import Self, TypeVar

Q = TypeVar('Q', bound='Qtrn')
V_xyz = TypeVar('V_xyz', bound='Vec_xyz')
V_pqr = TypeVar('V_pqr', bound='Vec_pqr')

PI = pi
RADtoDEG = 180/PI
DEGtoRAD = PI/180

def Sign( x ):
    if  x  < 0 :
        return -1
    return 1

class Vec_xyz():
    def __init__(self, x=0,y=0,z=0) -> Self:
        self.set(x,y,z) #< Forward, Right, Down

    def set(self, x, y, z) -> Self:
        self.x=x #< Forward
        self.y=y #< Right
        self.z=z #< Down
        return self

    def getVector(self) -> list:
        return [self.x, self.y, self.z]
    
    def copy(self) -> Self:
        return Vec_xyz(self.x, self.y, self.z)
        
    def mag(self) -> float:
        return sqrt(self.x**2 +self.y**2 +self.z**2)

    def __str__(self) -> str:
        s = ""
        for v in (self.x, self.y, self.z):
            s += "%1.3f, "%(v)
        return s[0:-2]

    def print(self) -> None:
        print("Vec_xyz:, " +self.__str__())

class Vec_pqr():
    def __init__(self, p=0,q=0,r=0) -> Self:
        self.set(p, q, r) #< Roll, Pitch, Yaw
        
    def set(self, p, q, r) -> Self:
        self.p=p #< Roll
        self.q=q #< Pitch
        self.r=r #< Yaw
        return self

    def copy(self) -> Self:
        return Vec_pqr(self.p, self.q, self.r)
        
    def mag(self) -> float:
        return sqrt(self.p**2 +self.q**2 +self.r**2)

    def getRotationTensor(self, dt ) -> list:
        wx = self.p*dt
        wy = self.q*dt
        wz = self.r*dt
        return [
            [  1,-wz,  wy],
            [ wz,  1, -wx],
            [-wy, wx,   1]
            ]

##    def getQuaternion(self, dt ) -> Q:
##        """  """
##        mag = self.mag()
##        if ( mag == 0.0 ):
##            return Qtrn( 1, 0, 0, 0 )
##
##        half_angle = 0.5 * mag * dt
##        sin_half = sin( half_angle )
##        cos_half = cos( half_angle )
##
##        return Qtrn(
##            w=cos_half,
##            x=sin_half * self.p / mag,
##            y=sin_half * self.q / mag,
##            z=sin_half * self.r / mag)

    def __str__(self) -> str:
        s = ""
        for v in (self.p, self.q, self.r):
            s += "%1.3f, "%(v)
        return s[0:-2]

    def print(self) -> None:
        print("Vec_pqr:, " +self.__str__())

##class Qtrn():
##    def __init__(self, w=0,x=0,y=0,z=0) -> Self:
##        self.w=w
##        self.x=x
##        self.y=y
##        self.z=z        
##
##    def copy(self) -> Self:
##        return Qtrn(self.w, self.x, self.y, self.z)
##        
##    def mag(self) -> float:
##        return sqrt(self.w**2 +self.x**2 +self.y**2 +self.z**2)
##
##    def conj(self) -> Self:
##        return Qtrn(self.w, -self.x, -self.y, -self.z)
##    
##    def multiply( self, q2 ) -> Self:
##        """Quaternion multiplication"""
##        q1 = self
##        w = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z
##        x = q1.w * q2.x + q1.x * q2.w + q1.y * q2.z - q1.z * q2.y
##        y = q1.w * q2.y - q1.x * q2.z + q1.y * q2.w + q1.z * q2.x
##        z = q1.w * q2.z + q1.x * q2.y - q1.y * q2.x + q1.z * q2.w
##        self.w, self.x, self.y, self.z  = (w,x,y,z)
##        return self
##
##    def normalize(self) -> Self:
##        """Normalize quaternion"""
##        mag = self.mag()
##        if mag > 0.0:
##            self.w /= mag
##            self.x /= mag
##            self.y /= mag
##            self.z /= mag
##        else:
##            printf("Error - normalize_quat() - something wrong with quaternion - divide by zero, mag = 0.0 \n")
##        return self
##
##    def getEuler(self) -> Vec_pqr: 
##        """Extract Euler angles from quaternion( roll, pitch, yaw in degrees )"""
##        ## Roll( X-axis rotation )
##        sinr_cosp = 2.0*( self.w * self.x + self.y * self.z )
##        cosr_cosp = 1.0 -2.0*( self.x**2 +self.y**2 )
##        roll = atan2( sinr_cosp, cosr_cosp )
##
##        ## Pitch( Y-axis rotation )
##        sinp = 2.0 * ( self.w * self.y - self.z * self.x )
##        if( abs(sinp) >= 1.0 ):
##            pitch = Sign(sinp)*M_PI / 2.0
##        else:
##            pitch = asin( sinp )
##
##        ## Yaw( Z-axis rotation )
##        siny_cosp = 2.0 * ( self.w * self.z + self.x * self.y )
##        cosy_cosp = 1.0 - 2.0 * ( self.y**2 + self.z**2 )
##        yaw = atan2( siny_cosp, cosy_cosp )
##        return Vec_pqr(p=roll, q=pitch, r=yaw)
##
##    def Heading(self) -> float: 
##        """Compute Heading Ang_le ( radians )"""
##        ## Rotate body x-axis ( 1,0,0 ) Int_o inrt frame
##        fx = 1 - 2*(self.y**2 +self.z**2)
##        fz = 2 * ( self.x*self.z - self.w*self.y )
##        return atan2( fx, fz ) #< atan2( east, north )
##
##    def __str__(self) -> str:
##        s = ""
##        for v in (self.w, self.x, self.y, self.z):
##            s += "%1.3f, "%(v)
##        return s[0:-2]
##
##    def print(self) -> None:
##        print("Qtrn_wxyz:, " +self.__str__())

class Attitude():
    """
    Right hand role. Z-down, Y-right, X-forward
    +Pitch up
    +Roll right
    +Yaw clockwise
    """
    def __init__(self, roll_r=0.0, pitch_r=0.0, yaw_r=0.0):
        self.set(roll_r, pitch_r, yaw_r)
        
    def set(self, roll_r, pitch_r, yaw_r):
        """yaw is around Z, pitch is around Y, and roll is around X"""
        self.roll_r  = roll_r
        self.pitch_r = pitch_r
        self.yaw_r   = yaw_r
        self._updateDCM()
        return self

    def _updateDCM(self) -> None:
        """ X-Fwd, Y-right, Z-Down"""
        p = PI/2
        a,b,c = self.yaw_r, self.pitch_r, self.roll_r
        ca,cb,cc = cos(a), cos(b), cos(c)
        sa,sb,sc = cos(a -p), cos(b -p),cos(c -p) #< sin(a), sin(b), sin(c)

        self.dcm = [ [ca*cb, ca*sb*sc-cc*sa, sa*sc+ca*sb*cc],
                   [sa*cb, sa*sb*sc+ca*cc, cc*sa*sb-ca*sc],
                   [ -sb,       cb*sc,          cb*cc    ]]

    def addW(self, W, dt):
        """W[0] around X (roll), W[1] around Y (pitch), W[3] around Z (yaw)"""
        WxDT = W.getRotationTensor(dt)
        self.dcm = MxM(self.dcm, WxDT)
        self._normalize()._updateAngles()
        return self

    def inv(self) -> list:
        return T(self.dcm)
    
    def _normalize(self):
        i = 0
        error = -V_dot_V( self.dcm[0], self.dcm[1])*0.5
        while (error > 0.0001) and (i<5):
            i += 1
            #print("%d, %1.4f"%(i,error))
            temporary = matrix(3,3)
            temporary[0] = Vxk( self.dcm[1], error)
            temporary[1] = Vxk( self.dcm[0], error)

            temporary[0] = V_add_V(temporary[0], self.dcm[0])
            temporary[1] = V_add_V(temporary[1], self.dcm[1])

            temporary[2] = VxV3( temporary[0], temporary[1] )

            renorm= 0.5 *(3 -V_dot_V(temporary[0], temporary[0]) )
            self.dcm[0] = Vxk(temporary[0], renorm)

            renorm = 0.5 *(3 -V_dot_V(temporary[1], temporary[1]) )
            self.dcm[1] = Vxk(temporary[1], renorm)

            renorm = 0.5 *(3 - V_dot_V(temporary[2], temporary[2]) )
            self.dcm[2] = Vxk(temporary[2], renorm)
            error = -V_dot_V( self.dcm[0], self.dcm[1])*0.5
        return self

    def _updateAngles(self) -> None:
        """yaw is around Z, pitch is around Y, and roll is around X"""
        dcm = self.dcm
        R11 = dcm[0][0]
        R21 = dcm[1][0]
        R31 = dcm[2][0]
        R32 = dcm[2][1]
        R33 = dcm[2][2]
        self.yaw_r   = atan2(R21,R11)
        self.roll_r  = atan2(R32,R33)
        self.pitch_r = atan(-R31/sqrt(R32**2 +R33**2) )

    def __str__(self) -> str:
        s = ""
        for v in (self.roll_r, self.pitch_r, self.roll_r):
            s += "%1.3f, "%(v)
        return s[0:-2]

    def print(self) -> None:
        print("Roll, Pitch, Roll (rad):, " +self.__str__())

def V_add_V(V1, V2) -> list:
    """ Return the result of vector addition """
    O = [0]*len(V1)
    for i, (v1,v2) in enumerate(zip(V1, V2)):
        O[i] = v1+v2
    return O

def Vxk( V, scale ):
    """Multiply the vector by a scalar"""
    vectorOut = [0]*len(V)
    for i,v in enumerate(V):
        vectorOut[i] = v*scale
    return vectorOut

def V_dot_V(V1, V2) -> float:
    product = 0.0
    for v1, v2 in zip(V1, V2):
        product += v1*v2
    return product

def VxV3( V1, V2 ) -> list:
    """Computes the cross product of two vectors"""
    vectorOut = [0]*3
    vectorOut[0]= (V1[1]*V2[2]) - (V1[2]*V2[1])
    vectorOut[1]= (V1[2]*V2[0]) - (V1[0]*V2[2])
    vectorOut[2]= (V1[0]*V2[1]) - (V1[1]*V2[0])
    return vectorOut

def printM(M, title="") -> None:
    out = title
    if title != "":
        out += ":\n"
    try:    
        for row in M:
            out += "|"
            first = True
            for elm in row:
                if not first:
                    out += ", "
                first = False
                out += "% 1.3f"%(elm)
            out += "|\n"
    except:
        print(str(M))
    print(out)

def matrix(rows, cols, val=0) -> list:
    """ Returns the rows by cols matrix M filled with value val """
    M = [0]*rows
    for row in range(0,rows):
        M[row] = [val]*cols
    return M

def zeros(rows, cols) -> list:
    """ Returns the rows by cols zero matrix Z """
    return matrix(rows, cols, val=0)

def MxV(M,V) -> list:
    """
    Return the result of NxM matrix and M vector multiplication
    Matrix structure: M[row][col]
    """
    rows = len(M)
    O = [0]*rows
    for r,row in enumerate(M):
        for m,v in zip(row,V):
            O[r] += m*v
    return O

def MxM( A, B ) -> list:
    """
    Multiply two matrices 3x3.
    Matrix structure: M[row][col]
    """
    rows = len(A)
    cols = len(B[0])
    matrixOut = zeros(rows, cols)
    for y in range(0,rows):
        for x in range(0,cols):
            for i in range(len(B)):
                matrixOut[y][x] += A[y][i]*B[i][x]
    return matrixOut

def getCol(M, col) -> list:
    """ Returns a copy of column 'col' from the matrix 'M' """
    rows = len(M)
    V = [0]*rows
    for i, row in enumerate(M):
        V[i] = row[col]
    return V

def T(M) -> list:
    """ Returns the transposed Matrix of M """
    cols = len(M[0])
    O = [0]*cols
    for i in range(0,cols):
        O[i] = getCol(M,i)
    return O

##def DCM_ZYX(a, b, c) -> list:
##    """ a is around Z, b is around Y, and c is around X"""
##    ca = cos(a)
##    cb = cos(b)
##    cc = cos(c)
##
##    p = PI/2
##    sa = cos(a -p) #<sin(a)
##    sb = cos(b -p) #<sin(b)
##    sc = cos(c -p) #<sin(c)
##
##    DCM = [ [ca*cb, ca*sb*sc-cc*sa, sa*sc+ca*sb*cc],
##            [sa*cb, sa*sb*sc+ca*cc, cc*sa*sb-ca*sc],
##            [ -sb,       cb*sc,          cb*cc    ]]
##    return DCM
##
##def get_abc_ZYX(dcm) -> list:
##    R11 = dcm[0][0]
##    R21 = dcm[1][0]
##    R31 = dcm[2][0]
##    R32 = dcm[2][1]
##    R33 = dcm[2][2]
##    a = atan(R21/R11)
##    b = asin(-R31)
##    c = atan(R32/R33)
##    return (a,b,c)
##    
##def body_to_earth_M( body, q ) -> Vec_xyz:
##    """Rotate vector by a quaternion using matrix math"""
##    x = q.x
##    y = q.y
##    z = q.z
##    w = q.w
##
##    R11 = 1 - 2 * ( y * y + z * z )
##    R12 = 2     * ( x * y - z * w )
##    R13 = 2     * ( x * z + y * w )
##
##    R21 = 2     * ( x * y + z * w )
##    R22 = 1 - 2 * ( x * x + z * z )
##    R23 = 2     * ( y * z - x * w )
##
##    R31 = 2     * ( x * z - y * w )
##    R32 = 2     * ( y * z + x * w )
##    R33 = 1 - 2 * ( x * x + y * y )
##
##    return Vec_xyz(
##        R11 * body.x + R12 * body.y + R13 * body.z,
##        R21 * body.x + R22 * body.y + R23 * body.z,
##        R31 * body.x + R32 * body.y + R33 * body.z)
##
##def body_to_earth_Q( body, q ) -> Vec_xyz:
##    """Rotate vector by a quaternion using Quaternion math"""
##    p = Qtrn(w=0, x=body.x, y=body.y, z=body.z)
##    q = q.copy()
##    q_conj = q.conj()
##    q.multiply( p ).multiply( q_conj )
##    return Vec_xyz(x=q.x, y=q.y, z=q.z)
 
##================================================================================================================= 

if __name__ == "__main__":
    print("Still missing unit-tests")
    Vec_xyz(1.1, 2.2, 3.3).print()
    Vec_pqr(1.1, 2.2, 3.3).print()
    Qtrn(1.1, 2.2, 3.3, 4.4).print()
    M = [[1,2,3],
         [4,5,6],
         [7,8,9]
         ]
    printM(M)
    printM(T(M))
    
