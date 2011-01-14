# Staircasing the chromatic blur of a natural scene to find the discrimination threshold - Oct 2010

from psychopy import visual, event, log, misc, colors, filters, misc, core, sound, data, gui, monitors
import numpy as np
import pylab, scipy, copy, time, os, random
from scipy import ndimage
from numpy.random import shuffle
import Image
import colorFunctions

#Create a dialog box for participant information
try:
    info=misc.fromFile('detParams.pickle')
except:
    info = {'participant' : 'RJS',
                'Achromatic' : 1,
                'Isoluminant' : 0}
info['dateStr'] = time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Detection Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('detParams.pickle', info)
else:
    core.quit()
   
#Create the basic information
info['pictures'] = ["Leaf512.jpg", "Pansy512.jpg", "Pelican512.jpg", "Pumpkin512.jpg"]
info['ISI'] = 0.5
info['displayT'] = 0.5
info['baseContrast'] = 0

#Staircase Information
info['nTrials'] = 1
info['nReversals'] = 1
info['stepSizes'] = [0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.025, 0.025]
info['minVal'] = 0
info['maxVal'] = 1
info['startVal'] = 0.3
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

def drawPicture(contr, picture):
    """Function to Set Contrast"""
    screenContr = float(max([contr]))
    print 'contr', contr, 'screenContr', screenContr
    if DEBUG == False:
        myWin.bits.setContrast(screenContr, LUTrange=0.9)
    if contr==0:
        picture.setContrast(0)
    else:
        picture.setContrast(0.9*contr/screenContr)
    picture.draw()

#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['1', '2']:
            if (key in ['1']) and order==1:
                return 1 #subject thinks the image appeared in the first interval
            if (key in ['2']) and order==1:
                return 0 #subject thinks the image appeared in the second interval
            if (key in ['1']) and order==2:
                return 0
            if (key in ['2']) and order==2:
                return 1
            else:
                print "hit 1 or 2 (or q) (you hit %s)" %key
                return None

#Start Message
startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="Please press 1 or 2 to indicate whether the stimulus is present in the first or second interval. Press any key when you are ready to continue.", )
                                                                                        
startMessage.draw()
fixation.draw()
myWin.update()
junk = event.waitKeys()

#Create multiple staircases in order interleave them
stairs = []
dklPictures=[]

for thisPicture in info['pictures']:

    #Import a picture, turn into an array and change the range from 0-255 to (-1)-1
    picture=np.array(Image.open(thisPicture).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1
    print 'min orig', np.minimum.reduce(np.minimum.reduce(np.minimum.reduce(picture)))
    print 'max orig', np.maximum.reduce(np.maximum.reduce(np.maximum.reduce(picture)))

    #Change the picture from RGB to DKL
    thisDklPicture = colorFunctions.rgb2dklCart(picture, conversionMatrix=conversionMatrix)
    thisDklPicture = np.array(thisDklPicture)
    
    #Create copies of the info for each staircase
    thisInfo = copy.copy(info)
    #Specific info for this staircase
#    thisInfo['thisPicture'] = thisPicture

#The Staircase
    #Set Up
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
    shuffle(stairs)
    for thisStair in stairs:
        thisContrast = thisStair.next()

    #Loop to run through the trials 
        trialClock.reset()
        
        print thisContrast
        
        order = random.randint(1.0, 2.0)
        
        # extract the picture array from the dictionary
        for p, d in thisStair.extraInfo.iteritems():
            dklPicture = d
            
        print 'min dkl', np.minimum.reduce(np.minimum.reduce(np.minimum.reduce(d)))
        print 'max dkl', np.maximum.reduce(np.maximum.reduce(np.maximum.reduce(d)))

        lum = copy.copy(dklPicture[:,:,0])*info['Achromatic']
        lm = copy.copy(dklPicture[:,:,1])*info['Isoluminant']
        s = copy.copy(dklPicture[:,:,2])*info['Isoluminant']
        
        #change back to RGB
        rgbPicture = colorFunctions.dklCartToRGB_2d(lum, lm, s, conversionMatrix)
        
        if info['Isoluminant']==1:
#            rgbmin = np.minimum.reduce(np.minimum.reduce(np.minimum.reduce(rgbPicture)))
#            rgbmax = np.maximum.reduce(np.maximum.reduce(np.maximum.reduce(rgbPicture)))
            range = (np.maximum.reduce(np.maximum.reduce(np.maximum.reduce(rgbPicture))))-(np.minimum.reduce(np.minimum.reduce(np.minimum.reduce(rgbPicture))))
            rgbPicture = (((rgbPicture-(np.minimum.reduce(np.minimum.reduce(np.minimum.reduce(rgbPicture)))))/range)*2)+-1
        
        print 'min rgb', np.minimum.reduce(np.minimum.reduce(np.minimum.reduce(rgbPicture)))
        print 'max rgb', np.maximum.reduce(np.maximum.reduce(np.maximum.reduce(rgbPicture)))
        
        
        
        #Draw the picture
        if order==1:
            if DEBUG==False: #Play a sound to indicate response is required
                tick.play()
            img = visual.PatchStim(myWin, tex=rgbPicture, units='deg', sf=(1/10.0), size=10.0)
            drawPicture(info['baseContrast']+thisContrast, img)
            myWin.flip()
            core.wait(info['displayT'])
            fixation.draw()
            myWin.flip()
            core.wait(info['ISI'])
            myWin.flip()
            if DEBUG==False: #Play a sound to indicate response is required
                tick.play()
            core.wait(info['displayT'])
        
        if order==2:
            if DEBUG==False: #Play a sound to indicate response is required
                tick.play()
            img = visual.PatchStim(myWin, tex=rgbPicture, units='deg', sf=(1/10.0), size=10.0)
            myWin.flip()
            core.wait(info['displayT'])
            fixation.draw()
            myWin.flip()
            core.wait(info['ISI'])
            drawPicture(info['baseContrast']+thisContrast, img)
            myWin.flip()
            if DEBUG==False: #Play a sound to indicate response is required
                tick.play()
            core.wait(info['displayT'])
            myWin.flip()
            
        
        fixation.draw()
        myWin.flip()
        
        #Take Participant Response
        thisResp = None
        while thisResp==None:
            keys = event.waitKeys()
            thisResp = checkCorrect(keys)
        
        thisStair.addData(thisResp)
    #Saving Files - Save to a different folder for each participant, then within the folder labelled by datestamp
    #Saving a different file for each picture condition and identify the display conditions
    #Saved to xlsx and psydat
    
    if info['Achromatic']==1:
        dispInfo='Achromatic'
    if info['Isoluminant']==1:
        dispInfo='Isoluminant'
        
    if not os.path.isdir('StimDetection_%s' %info['participant']):
        os.mkdir('StimDetection_%s' %info['participant'])
        
    for thisStair in stairs:
        for p, d in thisStair.extraInfo.iteritems():
            Picture = p
            fName = 'StimDetection_%s//StimDetection_%s_%s_%s_%s' %(info['participant'], info['participant'], Picture, dispInfo, info['dateStr'])
        thisStair.saveAsPickle(fName)
        thisStair.saveAsExcel(fileName=fName, sheetName='RawData', matrixOnly = False, appendFile=True)
    
    if DEBUG == False:
        win = visual.Window(bitsMode='fast')
        win.bits.setContrast(1)
        win.flip()
   
core.quit()
