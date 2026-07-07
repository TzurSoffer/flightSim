from Atmos import Atmos, RHO_0

class PropSimple():
    def getThrust(thrust, hae_m=0.0, rho=None) -> float:
        if rho == None:
            return thrust*Atmos.getRho(hae_m)/RHO_0
        return thrust*rho/RHO_0

##class Prop():
##    DIV_BY60 = 1/60.0
##    def __init__(self, diameter_m):
##        self.D_4 = diameter_m**2
##
##    def getThrust(self, rpm, pitch_deg, hae_m) -> float:
##        factor = 0.1
##        rho = Atmos.getRho(hae_m)
##        rps = rpm*Prop.DIV_BY60
##        return rho*(rps**2)*self.D_4

if __name__ == "__main__":
    for i in range(0,25000, 1000):
        print("Thrust (at %d m), %1.2f"%(i, PropSimple.getThrust(360, i)))

    for i in range(0,25000, 1000):
        rho = 1.225*i/25000
        print("Thrust (at rho=%1.3f), %1.2f"%(rho, PropSimple.getThrust(360, rho=rho)))
