import numpy as np
import Image

picture = np.array(Image.open('Leaf512.jpg').transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

flat = picture[:,:,0]
print picture.shape[3-1]
print flat.shape[3-1]

def dkl2rgb(dkl_NxNxN, conversionMatrix=None):
    #Convert from DKL color space (cone-opponent space from Derrington,
    #Krauskopf & Lennie) to RGB. 

    #Requires a conversion matrix, which will be generated from generic
    #Sony Trinitron phosphors if not supplied (note that this will not be
    #an accurate representation of the color space unless you supply a 
    #conversion matrix
    #
    #usage:
        #rgb(Nx3) = dkl2rgb(dkl_Nx3(el,az,radius), conversionMatrix)
    
    if len(dkl_NxNxN[0,0,:])==2:
    
        dkl_3xN = numpy.transpose(dkl_Nx3)#its easier to use in the other orientation!
        if numpy.size(dkl_3xN)==3:
            RG, BY, LUM = sph2cart(dkl_3xN[0],dkl_3xN[1],dkl_3xN[2])
        else:
            RG, BY, LUM = sph2cart(dkl_3xN[0,:],dkl_3xN[1,:],dkl_3xN[2,:])
        dkl_cartesian = numpy.asarray([LUM, RG, BY])
        
        if conversionMatrix==None:
            conversionMatrix = numpy.asarray([ \
                #LUMIN	%L-M	%L+M-S  (note that dkl has to be in cartesian coords first!)
                [1.0000, 1.0000, -0.1462],#R
                [1.0000, -0.3900, 0.2094],#G
                [1.0000, 0.0180, -1.0000]])#B
            log.warning('This monitor has not been color-calibrated. Using default DKL conversion matrix.')
            
        rgb = numpy.dot(conversionMatrix, dkl_cartesian)
        
        return numpy.transpose(rgb)#return in the shape we received it
    if dkl_NxNxN[2]==3:
        klj
       
dkl2rgb(flat)