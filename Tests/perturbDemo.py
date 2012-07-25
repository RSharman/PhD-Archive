#Demonstration code for perturbed stimuli (second year report) - May 2012

from psychopy import visual, core, misc, event, filters
import copy, Image
import numpy as np

def makeSineGrating(res,
            ori=0.0,    #in degrees
            cycles=1.0,
            phase=0.0,    #in degrees
            gratType="sin",
            contr=1.0):
    """Make an array containing a luminance grating of the specified params

    :Parameters:
        res: integer
            the size of the resulting matrix on both dimensions (e.g 256)
        ori: float or int (default=0.0)
            the orientation of the grating in degrees
        cycles:float or int (default=1.0)
            the number of grating cycles within the array
        phase: float or int (default=0.0)
            the phase of the grating in degrees (NB this differs to most
            PsychoPy phase arguments which use units of fraction of a cycle)
        gratType: 'sin', 'sqr', 'ramp' or 'sinXsin' (default="sin")
            the type of grating to be 'drawn'
        contr: float (default=1.0)
            contrast of the grating

    :Returns:
        a square numpy array of size resXres

    """
    tiny=0.0000000000001#to prevent the sinusoid ever being exactly at zero (for sqr wave)
    ori *= (-np.pi/180)
    phase *= (np.pi/180)
    xrange, yrange = np.mgrid[0.0 : cycles*2.0*np.pi : cycles*2.0*np.pi/res,
                                    0.0 : cycles*2.0*np.pi : cycles*2.0*np.pi/res]
    
    temp = range(0,res)
    print yrange[0].shape
                                   
    tempx, tempy = np.meshgrid(np.linspace(0.0, 127.0, num=128), np.linspace(0.0, np.pi*2, num=128))
    
    yrange = yrange+0.5*np.sin(4.0*tempy)
    xrange = xrange+tempx
#    
#    for n in range(len(temp)):
#        print temp[n]
#        temp[n] = round(temp[n])
#        print np.min(temp), np.max(temp)
#        
#    for n in range(len(temp)):
#        np.roll(yrange[n], temp[n])
#        np.roll(xrange[n], temp[n])

    
    if gratType is "none":
            res=2
            intensity = numpy.ones((res,res),Float)
    elif gratType is "sin":
            intensity= contr*(np.sin(xrange*np.sin(ori)+yrange*np.cos(ori) + phase))
    elif gratType is "ramp":
            intensity= contr*( xrange*numpy.cos(ori)+yrange*numpy.sin(ori) )/(2*numpy.pi)
    elif gratType is "sqr":#square wave (symmetric duty cycle)
            intensity = numpy.where(numpy.sin( xrange*numpy.sin(ori)+yrange*numpy.cos(ori) + phase + tiny)>=0, 1, -1)
    elif gratType is "sinXsin":
            intensity = numpy.sin(xrange)*numpy.sin(yrange)
    else:#might be a filename of an image
            try:
                    im = Image.open(gratType)
            except:
                    log.error( "couldn't find tex...",gratType)
                    return
    return intensity
#
myWin = visual.Window(size = (800,600), units = 'deg', monitor = 'testMonitor')

grating1 = makeSineGrating(128, cycles=10.0)
lumGrating = np.empty((128,128,3))
lumGrating[:,:,0] = copy.copy(grating1)
lumGrating[:,:,1] = copy.copy(grating1)
lumGrating[:,:,2] = copy.copy(grating1)
#lumGrating = np.array(lumGrating)

grating2 = filters.makeGrating(128, cycles=10.0)
lmGrating = np.empty((128,128,3))
lmGrating[:,:,0] = copy.copy(grating2)
lmGrating[:,:,1] = copy.copy(grating2)
lmGrating[:,:,2] = copy.copy(grating2)

print lumGrating.shape

#img = visual.PatchStim(myWin, tex = grating, size=10.0, sf=1/10.0)
#img.draw()
#myWin.flip()

dklGratingLum = misc.rgb2dklCart(lumGrating)
dklGratingLm = misc.rgb2dklCart(lmGrating)

lum1 = copy.copy(dklGratingLum[:,:,0])
lm1 = copy.copy(dklGratingLum[:,:,1])*0
s1 = copy.copy(dklGratingLum[:,:,2])*0

lum2 = copy.copy(dklGratingLm[:,:,0])
lm2 = copy.copy(dklGratingLm[:,:,1])
s2 = copy.copy(dklGratingLm[:,:,2])

rgbPictureLum = misc.dklCart2rgb(lum1, lm1, s1)
rgbPictureLm = misc.dklCart2rgb(lm2, lum2, s2)

#Values for lum wavy
lumlum = (lm2+lum1)/2.0
lmlum = (lum2 + lm1)/2.0
lmlum = np.rot90(lmlum)
slum = s1+s2

#Valyes for lm wavy
lumlm = (lum2 + lm1)/2.0
lmlm = (lm2 + lum1)/2.0
lmlm = np.rot90(lmlm)
slm = s1+s2

#LumWavy
rgbPictureAllLum = misc.dklCart2rgb(lumlum, lmlum, slum)
#LmWavy
rgbPictureAllLm = misc.dklCart2rgb(lumlm, lmlm, slm)

imgLum = visual.PatchStim(myWin, tex = rgbPictureLum, size = 10.0, sf = 1/10.0, opacity = 0.5)
imgLm = visual.PatchStim(myWin, tex = rgbPictureLm, size = 10.0, sf = 1/10.0, opacity = 0.5)
imgAllLum = visual.PatchStim(myWin, tex = rgbPictureAllLum, size = 10.0, sf = 1/10.0)
imgAllLm = visual.PatchStim(myWin, tex = rgbPictureAllLm, size = 10.0, sf = 1/10.0)

#imgLum.draw()
#imgLm.draw()
imgAllLm.draw()
myWin.flip()

myWin.getMovieFrame()
myWin.saveMovieFrames('OrthPerturbLm.jpg')

event.waitKeys()