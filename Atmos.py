from math import exp

class Atmos():
    def getPa(hae_m) -> float:
        """Returns the air pressure (pa)"""
        if hae_m < 11000:
            ### Troposphare
            T = 15.04 -0.00649*hae_m
            return 101.29 * ((T+273.1)/288.08)**(5.256)

        elif hae_m < 25000:
            ### Lower Stratosphare
            T = -56.46
            return 22.65 * exp(1.73 -0.000157*hae_m)

        else:
            ### Upper Stratosphare
            T = -131.21 +0.00299*hae_m
            return 2.488 * ((T +273.1)/216.6)**(-11.388)

    def getRho(hae_m, temp_C=25.0) -> float:
        """Returns the density of air (kg/m3)"""
        p = Atmos.getPa(hae_m)
        return p/(0.2869*(temp_C +273.1))

RHO_0 = Atmos.getRho(hae_m=0.0, temp_C=25.0)
