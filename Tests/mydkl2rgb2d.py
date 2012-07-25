from psychopy import visual, misc, core, event, monitors, logging
import colorFunctions, copy
import numpy

def dkl2rgb2d(dkl, conversionMatrix=None):
    if conversionMatrix==None:
        conversionMatrix = numpy.asarray([ \
            #LUMIN    %L-M    %L+M-S  (note that dkl has to be in cartesian coords first!)
            [1.0000, 1.0000, -0.1462],#R
            [1.0000, -0.3900, 0.2094],#G
            [1.0000, 0.0180, -1.0000]])#B
        logging.warning('This monitor has not been color-calibrated. Using default DKL conversion matrix.')

    if len(dkl.shape)==3:

        origShape = dkl.shape
        elevation = dkl[:,:,0]
        azimuth = dkl[:,:,1]
        radius = dkl[:,:,2]
        dkl = numpy.asarray([elevation.reshape([-1]), azimuth.reshape([-1]), radius.reshape([-1])])
        LM, S, Lum = misc.sph2cart(elevation, azimuth, radius)

        rgb = misc.dklCart2rgb(LUM = Lum, LM = LM, S = S, conversionMatrix = conversionMatrix)
        rgb.reshape(origShape)
