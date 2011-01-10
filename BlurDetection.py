# Staircasing the chromatic blur of a natural scene to find the discrimination threshold - Oct 2010

from psychopy import visual, event, log, misc, colors, filters, misc, core, sound, data, gui, monitors
import numpy as np
import pylab, scipy, copy, time, os, random
from scipy import ndimage
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
info['baseContrast'] = 0.1

#Staircase Information
info['nTrials'] = 1
info['nReversals'] = 1
info['stepSizes'] = [0.5, 0.5, 0.25, 0.25, 0.125, 0.125]
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

def drawPicture(contr, picture):
    """Function to Set Contrast"""
    screenContr = float(max([contr]))
    if DEBUG == False:
        myWin.bits.setContrast(screenContr, LUTrange=0.9)
    picture.setContrast(0.9*contr/screenContr)
    picture.draw()

for thisPicture in info['pictures']:

    #Import a picture, turn into an array and change the range from 0-255 to (-1)-1
    picture=np.array(Image.open(thisPicture).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

    #Change the picture from RGB to DKL
    dklPicture = colorFunctions.rgb2dklCart(picture, conversionMatrix=conversionMatrix)
    
        #The Staircase
    #Set Up
    stairs = data.StairHandler(startVal=info['startVal'], 
                                                        nReversals=info['nReversals'],
                                                        stepSizes=info['stepSizes'],
                                                        stepType='lin', 
                                                        nTrials=info['nTrials'],
                                                        nUp=info['nUp'],
                                                        nDown=info['nDown'],
                                                        extraInfo=info,
                                                        minVal=info['minVal'],
                                                        maxVal=info['maxVal']
                                                        )

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

    for thisContrast in stairs:
        trialClock.reset()
        
        order = random.randint(1.0, 2.0)
        
        #Turn the dkl picture into an array so we can manipulate it
        dklPicture = np.array(dklPicture)

        lum = copy.copy(dklPicture[:,:,0])*info['Achromatic']
        lm = copy.copy(dklPicture[:,:,1])*info['Isoluminant']
        s = copy.copy(dklPicture[:,:,2])*info['Isoluminant']
        
        #change back to RGB
        rgbPicture = colorFunctions.dklCartToRGB_2d(lum, lm, s, conversionMatrix)
        
        #Draw the picture
        
        if order==1:
            img = visual.PatchStim(myWin, tex=rgbPicture, units='deg', sf=(1/10.0), size=10.0)
            drawPicture(info['baseContrast']-thisContrast, img)
            myWin.flip()
            core.wait(info['displayT'])
            fixation.draw()
            myWin.flip()
            core.wait(info['ISI'])
            myWin.flip()
            core.wait(info['displayT'])
        
        if order==2:
            img = visual.PatchStim(myWin, tex=rgbPicture, units='deg', sf=(1/10.0), size=10.0)
            myWin.flip()
            core.wait(info['displayT'])
            fixation.draw()
            myWin.flip()
            core.wait(info['ISI'])
            drawPicture(info['baseContrast']-thisContrast, img)
            myWin.flip()
            core.wait(info['displayT'])
            myWin.flip()
            
            
        
        if DEBUG==False: #Play a sound to indicate response is required
           tick.play()
        
        fixation.draw()
        myWin.flip()
        
                #Take Participant Response
        thisResp = None
        while thisResp==None:
            keys = event.waitKeys()
            thisResp = checkCorrect(keys)
        
        stairs.addData(thisResp)
    #Saving Files - Save to a different folder for each participant, then within the folder labelled by datestamp
    #Saving a different file for each picture condition and identify the display conditions
    #Saved to xlsx and psydat
    
    if info['Achromatic']==1:
        dispInfo='Achromatic'
    if info['Isoluminant']==1:
        dispInfo='Isoluminant'
        
    if not os.path.isdir('StimDetection_%s' %info['participant']):
        os.nkdir('StimDetection_%s' %info['participant'])
    fName = 'StimDetection_%s//StimDetection_%s_%s_%s_%s' %(info['participant'], info['participant'], thisPicture, dispInfo, info['dateStr'])
    stairs.saveAsPickle(fName)
    stairs.saveAsExcel(fileName=fName, sheetName='RawData', matrixOnly = False, appendFile=True)
    
core.quit()
