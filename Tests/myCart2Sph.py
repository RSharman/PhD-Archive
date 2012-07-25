import numpy

def cart2sph(z, y, x):
    """Convert from cartesian coordinates (x,y,z) to spherical (elevation,
    azimuth, radius). Output is in radians. 
    
    usage:
        array3xN[el,az,rad] = cart2sph(array3xN[x,y,z])
        OR
        elevation, azimuth, radius = cart2sph(x,y,z)
        
        If working in DKL space, z = Luminance, y = S and x = LM"""
    
    elevation = numpy.empty([512,512])
    radius = numpy.empty([512,512])
    azimuth = numpy.empty([512,512])
    
    radius = numpy.sqrt(x**2 + y**2 + z**2)
    azimuth = numpy.arctan2(y, x)
    #Calculating the elevation from x,y up
    elevation = numpy.arctan2(z, numpy.sqrt(x**2+y**2))

#convert azimuth and elevation angles into degrees
    azimuth *=(180.0/numpy.pi)
    elevation *=(180.0/numpy.pi)

    sphere = numpy.array([elevation, azimuth, radius])
    sphere = numpy.rollaxis(sphere, 0, 3)

    return sphere