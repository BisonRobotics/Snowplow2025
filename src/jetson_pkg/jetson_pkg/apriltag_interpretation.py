import math

def apriltag_interpretation(xa, ya, thetaa, xc, zc, thetac):
    thetar = math.radians(thetaa) + math.pi + math.radians(thetac) + math.atan(xc / zc)
   
    dist = math.sqrt(xc**2 + zc**2)
    xr = xa + math.cos(math.radians(thetaa) + math.radians(thetac)) * dist
    yr = ya + math.sin(math.radians(thetaa) + math.radians(thetac)) * dist
    return (xr, yr, (thetar * (180 / math.pi)) % 360)
