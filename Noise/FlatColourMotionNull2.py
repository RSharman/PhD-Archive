#Determining isoluminance psychophysically - July 2012
#Modified to keep the azimuth flat

from psychopy import visual, core, data, misc, event, gui, monitors, filters
import time, copy, os, random
import numpy as np
from numpy.random import shuffle

DEBUG=True

try:
    #try to load previous info
    info = misc.fromFile('color_nulling.pickle')
    print info
except:
    #if no file use some defaults
    info={}
    info['participant']=''
info['dateStr'] = time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, fixed=['dateStr'])
#save to a file for future use (ie storing as defaults)
if dlg.OK: 
    misc.toFile('color_nulling.pickle',info)
else:
    core.quit() #user cancelled. quit
   
if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', 
        fullscr=False, allowGUI=True)
    conversionMatrix = None
    myMon= monitors.Monitor('testMonitor')
if DEBUG==False:
    myWin = visual.Window(size=(1280, 1024), monitor = 'heron', units = 'degs', 
        fullscr=True, allowGUI=False, bitsMode='fast')
    myMon=monitors.Monitor('heron')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
   
#Checking Responses
def checkCorrect (keys, direction):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['left', 'right']:
            if (key in ['left']) and direction=='left':
                return 0 #subject thinks the grating is drifting to the left
            if (key in ['right']) and direction=='left':
                return 1 #subject thinks the grating is drifting to the right
            if (key in ['left']) and direction=='right':
                return 1 #subject thinks the grating is drifting to the left
            if (key in ['right']) and direction=='right':
                return 0 #subject thinks the grating is drifting to the right
            else:
                print "hit left or right (or q) (you hit %s)" %key
                return None

#Ensuring that the azimuth remains flat when the elevation is changed
def flatAzim(res, cone, ori=0.0, cycles=1.0, phase=0.0, elevation = 0.0):
    """Creates a grating defined either by S or LM in DKL space. The elevation
    can be changed whilst keeping the azimuth flat - in effect changing the position
    of the azimuth
    
    Warning: May generate values >1 or <-1
    
    :Parameters:
        res: integer
            the size of the resulting matrix on both dimensions (e.g 256)
        cone: 'LM' or 'S'
            which axis in DKL space the grating should be created in
        ori: float or int (default=0.0)
            the orientation of the grating in degrees
        cycles:float or int (default=1.0)
            the number of grating cycles within the array
        phase: float or int (default=0.0)
            the phase of the grating in degrees (NB this differs to most
            PsychoPy phase arguments which use units of fraction of a cycle)
        elevation: float or int (default=0.0)
            the angle that the azimuth will be changed to

    :Returns:
        a square numpy array of size resXres
        """

    gabor = filters.makeGrating(res, ori=ori, cycles = cycles, phase=phase)

    colorGabor = np.zeros((len(gabor), len(gabor), 3))
    colorGabor[:,:,0] = copy.copy(gabor)
    colorGabor[:,:,1] = copy.copy(gabor)
    colorGabor[:,:,2] = copy.copy(gabor)

    dklGabor = misc.rgb2dklCart(colorGabor)
    if cone=='LM':
        dklGabor = misc.cart2sph(dklGabor[:,:,0]*0.0, dklGabor[:,:,0]*0.0, dklGabor[:,:,0])
    if cone=='S':
        dklGabor = misc.cart2sph(dklGabor[:,:,0]*0.0, dklGabor[:,:,0], dklGabor[:,:,0]*0.0)
    if cone=='Lum':
        dklGabor = misc.cart2sph(dklGabor[:,:,0], dklGabor[:,:,0]*0.0, dklGabor[:,:,0]*0.0)

    temp = copy.copy(dklGabor[:,:,1])+1
    temp = (temp/np.abs(temp))*+elevation
    dklGabor[:,:,0] += temp

    rgbGabor = misc. dkl2rgb(dklGabor)
    return rgbGabor

#Staircase Information
info['nTrials'] = 50
info['nReversals'] = 1
info['stepSizes'] = [3.0, 3.0, 1.5, 1.5, 0.75, 0.75, 0.375, 0.375, 0.1825]#[5.0, 2.0, 2.0, 1.0, 1.0, 0.5, 0.5, 0.25, 0.25]
info['minVal'] = -45.0
info['maxVal'] = 45.0
#info['startVal'] = 0.0
info['nUp'] = 1
info['nDown'] = 1
info['framesPerImg']=5
info['trialDuration']=0.3

#Create multiple staircases in order interleave them
stairs = []
conds = ['posStart', 'negStart']
directions = ['left', 'right']
info['ISI'] = 0.3

trialClock = core.Clock()
fixation = visual.PatchStim(myWin, size=0.05, tex=None, mask='circle', color = 'black')

for thisCond in conds:
    #Create copies of the info for each staircase
    thisInfo = copy.copy(info)
    
    if thisCond=='posStart':
        thisInfo['condition'] = 'posStart'
        thisInfo['startVal'] = 6.0

    if thisCond=='negStart':
        thisInfo['condition'] = 'negStart'
        thisInfo['startVal'] = -6.0
        
    #Set up staircase
    thisStair = data.StairHandler(startVal=thisInfo['startVal'], 
                                                        nReversals=thisInfo['nReversals'],
                                                        stepSizes=thisInfo['stepSizes'],
                                                        stepType='lin', 
                                                        nTrials=thisInfo['nTrials'],
                                                        nUp=thisInfo['nUp'],
                                                        nDown=thisInfo['nDown'],
                                                        extraInfo=thisInfo,
                                                        minVal=thisInfo['minVal'],
                                                        maxVal=thisInfo['maxVal']
                                                        )
    stairs.append(thisStair)

#Start Message
startMessage = visual.TextStim(myWin, pos=(0.0,-1), height =0.2, color=-1, text="Press left or right to indicate which")
startMessage1 = visual.TextStim(myWin, pos=(0.0, -1.2), height = 0.2, color=-1, text="direction the grating is moving.")
startMessage2 = visual.TextStim(myWin, pos=(0.0, -1.4), height=0.2, color=-1, text = "Press any key when ready.")
startMessage.draw()
startMessage1.draw()
startMessage2.draw()
fixation.draw()
myWin.flip()
junk = event.waitKeys()

for trialN in range(info['nTrials']):
    shuffle(stairs)
    
    temp = random.randint(0.0, 1.0)
    
    #Loop through the randomised staircases
    for thisStair in stairs:
        thisElev = thisStair.next()
        direction = directions[temp]
        print direction
        
        bwTex = flatAzim(512, 'Lum', elevation = 0.0)/2.0
        colorTex = flatAzim(512, 'LM', elevation = thisElev)/2.0
        
        #Change the direction of apparent motion
        if direction=='left':
            bwGabor1 = visual.PatchStim(myWin, tex = bwTex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase=0.0,contrast=0.1)
            colorGabor1 = visual.PatchStim(myWin, tex=colorTex, mask='gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.25)
            bwGabor2 = visual.PatchStim(myWin, tex = bwTex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.5,contrast=0.1)
            colorGabor2 = visual.PatchStim(myWin, tex = colorTex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.75)
        if direction=='right':
            bwGabor1 = visual.PatchStim(myWin, tex = bwTex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase=0.0,contrast=0.1)
            colorGabor1 = visual.PatchStim(myWin, tex=colorTex, mask='gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.75)
            bwGabor2 = visual.PatchStim(myWin, tex = bwTex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.5,contrast=0.1)
            colorGabor2 = visual.PatchStim(myWin, tex = colorTex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.25)
        
        trialClock.reset()
        while trialClock.getTime()<info['trialDuration']:
            for stim in [bwGabor1, colorGabor1,bwGabor2, colorGabor2]:
                for frames in range(info['framesPerImg']):
                    stim.draw()
                    myWin.flip()
        fixation.draw()
        myWin.flip()

            #Collect responses
        thisResp=None
        while thisResp==None:
            keys=event.waitKeys()
            thisResp = checkCorrect(keys, direction)
        print thisElev
        thisStair.addData(thisResp)
        core.wait(info['ISI'])