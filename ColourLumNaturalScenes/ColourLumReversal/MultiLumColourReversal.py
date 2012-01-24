# Reversing the colour and luminance values and then finding the blur detection threshold - Sept 2011
#All final RGB values are halved to ensure that they fall within -1-1. 

from psychopy import visual, event, log, misc, colors, filters, misc, core, sound, data, gui, monitors, log
import numpy as np
import pylab, scipy, copy, time, os, random
from scipy import ndimage
from numpy.random import shuffle
import Image

#Create a dialog box for participant information
try:
    info=misc.fromFile('lastParams.pickle')
except:
    info = {'participant' : 'RJS'}
info['dateStr']=time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Blur Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', info)
else:
    core.quit()
    
#Create the basic information
info['pictures'] = ["Pumpkin512.jpg"]#["Pansy512.jpg", "Leaf512.jpg", "Pelican512.jpg", "Pumpkin512.jpg"]
info['ISI'] = 0.5
info['displayT'] = 0.3
info['baseBlur'] = 0
counter=0

#Staircase Information
info['nTrials'] = 2
info['nReversals'] = 1
info['stepSizes'] = [8,8,4,4,2,2,1,1,0.5,0.5]
info['minVal'] = 0
info['maxVal'] = 100
info['startVal'] = 0
info['nUp'] = 1
info['nDown'] = 3

DEBUG=True
#Clocks and Sounds
trialClock = core.Clock()
tick = sound.Sound('A', octave=6, secs=0.01); tick.setVolume(0.3)

#Create window and fixation
if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', fullscr=False, allowGUI=True)
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

#Start Message
startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="Please press 1 or 2 to indicate whether the first or second image appears more blurred. Press any key when you are ready to continue.", )
                                                                                        
startMessage.draw()
myWin.flip()
junk = event.waitKeys()

#Create multiple staircases in order interleave them
stairs = []
dklPictures=[]
conditions=['lum']#['isolum', 'chrom', 'lum', 'achrom']

for thisCond in conditions:
    #Create copies of the info for each staircase
    thisInfo = copy.copy(info)
    if thisCond=='isolum':
        thisInfo['Chromaticity']=1
        thisInfo['Luminance']=0
        thisInfo['Chromatic Blur']='y'
        thisInfo['Luminance Blur']='n'
    if thisCond=='chrom':
        thisInfo['Chromaticity']=1
        thisInfo['Luminance']=1
        thisInfo['Chromatic Blur']='y'
        thisInfo['Luminance Blur']='n'
    if thisCond=='lum':
        thisInfo['Chromaticity']=1
        thisInfo['Luminance']=1
        thisInfo['Chromatic Blur']='n'
        thisInfo['Luminance Blur']='y'
    if thisCond=='achrom':
        thisInfo['Chromaticity']=0
        thisInfo['Luminance']=1
        thisInfo['Chromatic Blur']='n'
        thisInfo['Luminance Blur']='y'
    for thisPicture in info['pictures']:
        #Import a picture, turn into an array and change the range from 0-255 to (-1)-1
        picture=np.array(Image.open(thisPicture).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

        #Change the picture from RGB to DKL
        thisDklPicture = misc.rgb2dklCart(picture, conversionMatrix=conversionMatrix)
        thisDklPicture = np.array(thisDklPicture)
        

        #Specific info for this staircase
        picInfo=copy.copy(thisInfo)
    #    thisInfo['thisPicture'] = thisPicture
    #    info['images']={thisPicture:thisDklPicture}
    #    info['images'][thisPicture]=thisDklPicture
        
        thisStair = data.StairHandler(startVal=info['startVal'], 
                                                    nReversals=info['nReversals'],
                                                    stepSizes=info['stepSizes'],
                                                    stepType='lin', 
                                                    nTrials=info['nTrials'],
                                                    nUp=info['nUp'],
                                                    nDown=info['nDown'],
                                                    extraInfo=picInfo, #{thisPicture:thisDklPicture},
                                                    minVal=info['minVal'],
                                                    maxVal=info['maxVal']
                                                            )
        thisStair.extraInfo['images']={thisPicture:thisDklPicture}
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
        for p, d in thisStair.extraInfo['images'].iteritems():
            dklPicture = d
        
#        dklPicture = np.array(dklPicture)

#        lum = copy.copy(dklPicture[:,:,0])*info['Luminance']
#        lm = copy.copy(dklPicture[:,:,1])*info['Chromaticity']
#        s = copy.copy(dklPicture[:,:,2])*info['Chromaticity']
        
        lum = copy.copy(dklPicture[:,:,0])*thisStair.extraInfo['Chromaticity']
        lm = copy.copy(dklPicture[:,:,1])*thisStair.extraInfo['Luminance']
        s = copy.copy(dklPicture[:,:,2])*thisStair.extraInfo['Luminance']
        
        sigmaLumFirst=0
        sigmaLumSecond=0
        sigmaFirst=0
        sigmaSecond=0
        
        if thisStair.extraInfo['Luminance Blur']=='y':
            if order==1:
                sigmaFirst += thisIntensity
            if order==2:
                sigmaSecond += thisIntensity
            
        if thisStair.extraInfo['Chromatic Blur']=='y':
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
        rgbPictureFirst = misc.dklCart2rgb((lmFirst+sFirst)/2, lumFirst, lumFirst, conversionMatrix)
        rgbPictureSecond = misc.dklCart2rgb((lmSecond+sSecond)/2, lumSecond, lumSecond, conversionMatrix)

#        rgbPictureFirst = misc.dklCart2rgb(lumFirst, lmFirst, sFirst, conversionMatrix)
#        rgbPictureSecond = misc.dklCart2rgb(lumSecond, lmSecond, sSecond, conversionMatrix)
        
        #Divide all the values by 2 so that there is room for the increases caused by the Gaussian filter
        rgbPictureFirst=rgbPictureFirst/2
        rgbPictureSecond=rgbPictureSecond/2
               
    #    
        #Draw the picture
        imgFirst = visual.PatchStim(myWin, tex=rgbPictureFirst, units='deg', sf=(1/10.0), size=10.0)
        imgFirst.draw()
        myWin.flip()
        core.wait(info['displayT'])
#        junk = event.waitKeys()
        
        fixation.draw()
        myWin.flip()
        core.wait(info['ISI'])
        
        imgSecond = visual.PatchStim(myWin, tex=rgbPictureSecond, units='deg', sf=(1/10.0), size=10.0)
        imgSecond.draw()
        myWin.flip()
        myWin.getMovieFrame()
        myWin.saveMovieFrames('RevPumpkin.jpg')
        core.wait(info['displayT'])
#        junk = event.waitKeys()
        
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
        if counter ==4:
            breakMsg = startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="You are one third of the way through! Take a break! When you are ready press any key to continue.", )
            breakMsg.draw()
            myWin.flip()
            event.waitKeys()
        if counter ==8:
            breakMsg = startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="You are two thirds of the way through! Take a break! When you are ready press any key to continue.", )
            breakMsg.draw()
            myWin.flip()
            event.waitKeys()
        counter+=1
#Saving Files - Save to a different folder for each participant, then within the folder labelled by datestamp
#Saving a different file for each picture condition and identify the display and blur conditions
#Saved to xlsx and psydat

print info['participant']

if not os.path.isdir('ReverseBlur_%s' %info['participant']):
    os.mkdir('ReverseBlur_%s' %info['participant'])
#
#log.console.setLevel(log.DEBUG)

for thisStair in stairs:
    if thisStair.extraInfo['Chromaticity']==1 and thisStair.extraInfo['Luminance']==1:
        dispInfo='LumChrom'
    if thisStair.extraInfo['Chromaticity']==1 and thisStair.extraInfo['Luminance']==0:
        dispInfo='Isolum'
    if thisStair.extraInfo['Chromaticity']==0 and thisStair.extraInfo['Luminance']==1:
        dispInfo='Achrom'
        
    if thisStair.extraInfo['Chromatic Blur']=='y' and thisStair.extraInfo['Luminance Blur']=='y':
        blurInfo='AllBlur'
    if thisStair.extraInfo['Chromatic Blur']=='y' and thisStair.extraInfo['Luminance Blur']=='n':
        blurInfo='ChromBlur'
    if thisStair.extraInfo['Chromatic Blur']=='n' and thisStair.extraInfo['Luminance Blur']=='y':
        blurInfo='LumBlur'
#    for p, d in thisStair.extraInfo['images'].iteritems():
#        Picture = p
    Picture = thisStair.extraInfo['images'].keys()
    Picture = Picture[0]
    fName = 'ReverseBlur_%s//ReverseBlur_%s_%s_%s_%s_%s' %(thisStair.extraInfo['participant'], thisStair.extraInfo['participant'], Picture, dispInfo, blurInfo, info['dateStr'])
    print fName
    thisStair.saveAsExcel(fileName=fName, sheetName='RawData', matrixOnly = False, appendFile=True)
    thisStair.saveAsPickle(fName)

    #    #stairs.saveAsText(fName)


core.quit()
