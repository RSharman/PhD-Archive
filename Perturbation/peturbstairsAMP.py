#Demonstration code for perturbed stimuli (second year report) - May 2012

from psychopy import visual, data, core, misc, event, filters, gui
import copy, Image, random
import numpy as np

expinfo = {'observer':''}
dlg = gui.DlgFromDict(dictionary=expinfo, title='simple JND Exp', fixed=['dateStr'])
expinfo['dateStr']= data.getDateStr()
filename = 'AMP' + expinfo['observer'] + expinfo['dateStr']

    #setup staircase
stairs=data.StairHandler(startVal=0.5, stepType='lin', maxVal=5, minVal=0, nUp=1, nDown=3, nReversals=4, nTrials=5, stepSizes=[0.1,0.1,0.05,0.05])

def makeSineGrating(res,
            ori=0.0,    #in degrees
            cycles=1.0,
            phase=0.0,    #in degrees
            gratType="sin",
            contr=1.0,
            amplitude=0.5,
            frequency=4.0):
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
    
    
    # The number added to yrange = amplitude, the number multiplied by tempy is the frequency.
    yrange = yrange+amplitude*np.sin(frequency*tempy)
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
questionText=visual.TextStim(myWin, text='Was the perturbed image 1st(1) or 2nd(2)?')


for amp in stairs:
    
    grating2 = filters.makeGrating(128, cycles=10.0)
    lmGrating = np.empty((128,128,3))
    lmGrating[:,:,0] = copy.copy(grating2)
    lmGrating[:,:,1] = copy.copy(grating2)
    lmGrating[:,:,2] = copy.copy(grating2)
    
    
    grating1 = makeSineGrating(128, cycles=10.0, amplitude=amp, frequency=5)
    lumGrating = np.empty((128,128,3))
    lumGrating[:,:,0] = copy.copy(grating1)
    lumGrating[:,:,1] = copy.copy(grating1)
    lumGrating[:,:,2] = copy.copy(grating1)
    
    
    print amp     #Current amplitude

    dklGratingLum = misc.rgb2dklCart(lumGrating)
    dklGratingLm = misc.rgb2dklCart(lmGrating)
    
    lum1 = copy.copy(dklGratingLum[:,:,0])
    lm1 = copy.copy(dklGratingLum[:,:,1])*0
    s1 = copy.copy(dklGratingLum[:,:,2])*0
    
    lum2 = copy.copy(dklGratingLm[:,:,0])
    lm2 = copy.copy(dklGratingLm[:,:,1])*0
    s2 = copy.copy(dklGratingLm[:,:,2])*0
    

    
    lumlm = (lum2)/2.0              #peturb
    lmlm = (lum1)/2.0                #straight
    lmlm = np.rot90(lmlm)           #rotated perturb
    lumlm2 = np.rot90(lumlm)       #rotated straight 
    slm = np.empty((128,128))
    

    rgbPictureAllLm = misc.dklCart2rgb(lumlm, lmlm, slm)        #peturb full image
    rgbPictureStraight = misc.dklCart2rgb(lumlm, lumlm2, slm)   #straight full image

    imgAllLm = visual.PatchStim(myWin, tex = rgbPictureAllLm, size = 10.0, sf = 1/10.0)
    imgAllSt = visual.PatchStim(myWin, tex = rgbPictureStraight, size=10.0, sf=1/10.0)
    

    
    targettime= random.choice([0,1])        #set random order
    
    if targettime == 1:    
        img1 = imgAllLm
        img2 = imgAllSt
    else:
        img2 = imgAllLm  
        img1 = imgAllSt
    
    img1.draw()          #present stim
    myWin.flip()
    core.wait(0.5)
    
    myWin.flip()
    core.wait(1)
    
    img2.draw()
    myWin.flip()
    core.wait(0.5)
    
    
    questionText.draw()
    myWin.flip()  
    
    
    keys = event.waitKeys()     #get response
    if 'num_1' in keys:
        if targettime==1:
            thisResp=1
        else:
            thisResp=0
    elif 'num_2' in keys:
        if targettime==0:
            thisResp=1
        else:
            thisResp=0
        
    stairs.addData(thisResp) 
stairs.saveAsPickle(filename)
stairs.saveAsExcel(filename)