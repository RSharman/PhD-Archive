# Staircasing the chromatic blur of a natural scene to find the detection threshold - Oct 2010
#Including contrast modulation to ensure that contrast doesn't decrease as a function of blur.

from psychopy import visual, event, log, misc, colors, filters, misc, core, sound, data, gui, monitors, log
import numpy as np
import pylab, scipy, copy, time, os, random
from scipy import ndimage
from numpy.random import shuffle
import Image
import colorFunctions

#Create a dialog box for participant information
try:
    info=misc.fromFile('lastParams.pickle')
except:
    info = {'participant' : 'RJS',
                'Chromaticity':1,
                'Luminance':1,
                'Chromatic Blur' : 'y',
                'Luminance Blur' : 'n'}
info['dateStr']=time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Blur Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', info)
else:
    core.quit()
    
#Create the basic information
info['pictures'] = ["Leaf512.jpg", "Pansy512.jpg", "Pelican512.jpg", "Pumpkin512.jpg"]
info['ISI'] = 0.5
info['displayT'] = 0.5
info['baseBlur'] = 0

#Staircase Information
info['nTrials'] = 5
info['nReversals'] = 1
info['stepSizes'] = [20, 20, 10, 10, 5, 5, 2.5, 2.5, 1.25, 1.25, 0.06, 0.06]
info['minVal'] = 0
info['maxVal'] = 100
info['startVal'] = 20
info['nUp'] = 1
info['nDown'] = 3

DEBUG=True
#Clocks and Sounds
trialClock = core.Clock()
tick = sound.Sound('A', octave=6, secs=0.01); tick.setVolume(0.3)

#Create window and fixation
if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', 
        fullscr=False, allowGUI=True)
    conversionMatrix = None
    myMon= monitors.Monitor('testMonitor')
if DEBUG==False:
    myWin = visual.Window(size=(1024, 768), monitor = 'sparrow', units = 'degs',
        fullscr=True, allowGUI=False, bitsMode='fast')
    myMon=monitors.Monitor('sparrow')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
fixation = visual.PatchStim(myWin, size=0.1, tex=None, mask='circle', rgb=-1)


#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['1', '2']:
            if (key in ['1']) and order==1:
                return 1 #subject perceives the first image as more blurred
            if (key in ['2']) and order==1:
                return 0 #subject perceives the second image as more blurred
            if (key in ['1']) and order==2:
                return 0
            if (key in ['2']) and order==2:
                return 1
            else:
                print "hit 1 or 2 (or q) (you hit %s)" %key
                return None

#Create multiple staircases in order interleave them
stairs = []
dklPictures=[]
for thisPicture in info['pictures']:
    #Import a picture, turn into an array and change the range from 0-255 to (-1)-1
    picture=np.array(Image.open(thisPicture).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

    #Change the picture from RGB to DKL
    thisDklPicture = colorFunctions.rgb2dklCart(picture, conversionMatrix=conversionMatrix)
    thisDklPicture = np.array(thisDklPicture)
    
    #Create copies of the info for each staircase
    thisInfo = copy.copy(info)
    #Specific info for this staircase
#    thisInfo['thisPicture'] = thisPicture

    thisStair = data.StairHandler(startVal=info['startVal'], 
                                                nReversals=info['nReversals'],
                                                stepSizes=info['stepSizes'],
                                                stepType='lin', 
                                                nTrials=info['nTrials'],
                                                nUp=info['nUp'],
                                                nDown=info['nDown'],
                                                extraInfo={thisPicture:thisDklPicture},
                                                minVal=info['minVal'],
                                                maxVal=info['maxVal']
                                                        )
    stairs.append(thisStair)

for trialN in range(info['nTrials']):
    shuffle(stairs) #randomise the order

    #Loop through the randomised staircases
    for thisStair in stairs:
        thisIntensity = thisStair.next()
#        print 'here', thisPicture
#For Loop to run through the trials 

#    for thisBlur in stairs:
        trialClock.reset()
        
        order = random.randint(1.0, 2.0)
        print 'order', order
        
        # extract the picture array from the dictionary
        for p, d in thisStair.extraInfo.iteritems():
            dklPicture = d
        
#        dklPicture = np.array(dklPicture)

        lum = copy.copy(dklPicture[:,:,0])*info['Luminance']
        lm = copy.copy(dklPicture[:,:,1])*info['Chromaticity']
        s = copy.copy(dklPicture[:,:,2])*info['Chromaticity']
        
        sigmaLumFirst=0
        sigmaLumSecond=0
        sigmaFirst=0
        sigmaSecond=0
        
        if info['Chromatic Blur']=='y':
            if order==1:
                sigmaFirst += thisIntensity
            if order==2:
                sigmaSecond += thisIntensity
            
        if info['Luminance Blur']=='y':
            if order==1:
                sigmaLumFirst +=thisIntensity
            if order==2:
                sigmaLumSecond += thisIntensity
        
    #    print sigma
        
        #Staircase chromatic blur for first image
        lmFirst = ndimage.gaussian_filter(lm, sigma=sigmaFirst, order=0, output=None, mode='reflect', cval=0.0)
        sFirst = ndimage.gaussian_filter(s, sigma=sigmaFirst, order=0, output=None, mode='reflect', cval=0.0)
        lumFirst = ndimage.gaussian_filter(lum, sigma=sigmaLumFirst)
        #Staircase chromatic blur for second image
        lmSecond = ndimage.gaussian_filter(lm, sigma=sigmaSecond, order=0, output=None, mode='reflect', cval=0.0)
        sSecond = ndimage.gaussian_filter(s, sigma=sigmaSecond, order=0, output=None, mode='reflect', cval=0.0)
        lumSecond = ndimage.gaussian_filter(lum, sigma=sigmaLumSecond)
        
        #change back to RGB
        rgbPictureFirst = colorFunctions.dklCartToRGB_2d(lumFirst, lmFirst, sFirst, conversionMatrix)
        rgbPictureSecond = colorFunctions.dklCartToRGB_2d(lumSecond, lmSecond, sSecond, conversionMatrix)
        
        #Divide all the values by 2 so that there is room for the increases caused by the Gaussian filter
        rgbPictureFirst=rgbPictureFirst/2
        rgbPictureSecond=rgbPictureSecond/2
               
    #    
        #Draw the picture
        imgFirst = visual.PatchStim(myWin, tex=rgbPictureFirst, units='deg', sf=(1/10.0), size=10.0)
        imgFirst.draw()
        myWin.flip()
        core.wait(info['displayT'])

        fixation.draw()
        myWin.flip()
        core.wait(info['ISI'])
        
        imgSecond = visual.PatchStim(myWin, tex=rgbPictureSecond, units='deg', sf=(1/10.0), size=10.0)
        imgSecond.draw()
        myWin.flip()
        core.wait(info['displayT'])
        
        if DEBUG==False: #Play a sound to indicate response is required
            tick.play()
        
        fixation.draw()
        myWin.flip()
        
        #Take Participant Response
        thisResp = None
        while thisResp==None:
            keys = event.waitKeys()
            thisResp = checkCorrect(keys)
            
        print 'thisResp', thisResp
        
        thisStair.addData(thisResp)
    
#Saving Files - Save to a different folder for each participant, then within the folder labelled by datestamp
#Saving a different file for each picture condition and identify the display and blur conditions
#Saved to xlsx and psydat

print info['participant']

if info['Chromaticity']==1 and info['Luminance']==1:
    dispInfo='LumChrom'
if info['Chromaticity']==1 and info['Luminance']==0:
    dispInfo='Isolum'
if info['Chromaticity']==0 and info['Luminance']==1:
    dispInfo='Achrom'
    
if info['Chromatic Blur']=='y' and info['Luminance Blur']=='y':
    blurInfo='AllBlur'
if info['Chromatic Blur']=='y' and info['Luminance Blur']=='n':
    blurInfo='ChromBlur'
if info['Chromatic Blur']=='n' and info['Luminance Blur']=='y':
    blurInfo='LumBlur'

if not os.path.isdir('Blur_%s' %info['participant']):
    os.mkdir('Blur_%s' %info['participant'])
#
#log.console.setLevel(log.DEBUG)

for thisStair in stairs:
    for p, d in thisStair.extraInfo.iteritems():
        Picture = p
        fName = 'Blur_%s//Blur_%s_%s_%s_%s_%s' %(info['participant'], info['participant'], Picture, dispInfo, blurInfo, info['dateStr'])
    thisStair.saveAsExcel(fileName=fName, sheetName='RawData', matrixOnly = False, appendFile=True)
    thisStair.saveAsPickle(fName)

    #    #stairs.saveAsText(fName)


core.quit()
