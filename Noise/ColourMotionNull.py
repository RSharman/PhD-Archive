#Determining isoluminance psychophysically - June 2012
#Test construction of stimuli

from psychopy import visual, core, data, misc, event, gui, monitors
import time, copy, os
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
    myWin = visual.Window(size=(1280, 1024), monitor = 'heron', units = 'degs', screen=1,
        fullscr=True, allowGUI=False, bitsMode='fast')
    myMon=monitors.Monitor('heron')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)

#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['left', 'right']:
            if (key in ['left']):
                return 0 #subject thinks the grating is drifting to the left
            if (key in ['right']):
                return 1 #subject thinks the grating is drifting to the right
            else:
                print "hit left or right (or q) (you hit %s)" %key
                return None

#Staircase Information
info['nTrials'] = 50
info['nReversals'] = 1
info['stepSizes'] = [5.0, 2.0, 2.0, 1.0, 1.0, 0.5, 0.5, 0.25, 0.25]
info['minVal'] = -45.0
info['maxVal'] = 45.0
#info['startVal'] = 0.0
info['nUp'] = 1
info['nDown'] = 3

#Create multiple staircases in order interleave them
stairs = []
conds = ['posStart']#, 'negStart']
info['ISI'] = 0.3

#Create stimuli
if DEBUG==True:
    bwGabor1 = visual.PatchStim(myWin, tex='sin', mask='gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.0)
    colorGabor1 = visual.PatchStim(myWin, tex='sin', mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.25, colorSpace = 'dkl')
    bwGabor2 = visual.PatchStim(myWin, tex='sin', mask='gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.5)
    colorGabor2 = visual.PatchStim(myWin, tex='sin', mask = 'gauss', units = 'deg', size = 10.0, sf = 0.2, phase = 0.25, colorSpace = 'dkl')
if DEBUG==False:
    bwGabor1 = visual.PatchStim(myWin, tex='sin', mask='gauss', units = 'deg', size = 2.0, sf = 2.0, phase = 0.0)
    colorGabor1 = visual.PatchStim(myWin, tex='sin', mask = 'gauss', units = 'deg', size = 2.0, sf = 2.0, phase = 0.25, colorSpace = 'dkl')
    bwGabor2 = visual.PatchStim(myWin, tex='sin', mask='gauss', units = 'deg', size = 2.0, sf = 2.0, phase = 0.5)
    colorGabor2 = visual.PatchStim(myWin, tex='sin', mask = 'gauss', units = 'deg', size = 2.0, sf = 2.0, phase = 0.25, colorSpace = 'dkl')
    
for thisCond in conds:
    #Create copies of the info for each staircase
    thisInfo = copy.copy(info)
    if thisCond=='posStart':
        thisInfo['condition'] = 'posStart'
        thisInfo['startVal'] = 25.0

    if thisCond=='negStart':
        thisInfo['condition'] = 'negStart'
        thisInfo['startVal'] = -25.0

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
    
for trialN in range(info['nTrials']):
    shuffle(stairs) #randomise the order
    
    #Loop through the randomised staircases
    for thisStair in stairs:
        thisElev = thisStair.next()
        bwGabor1.draw()
        myWin.flip()
        core.wait(0.1)
                
        colorGabor1.setColor(color = [thisElev,0,0.5])
        colorGabor1.draw()
        myWin.flip()
        core.wait(0.1)
        event.waitKeys()

        bwGabor2.draw()
        myWin.flip()
        core.wait(0.1)

        colorGabor2.setColor(color = [thisElev,0,0.5])
        colorGabor2.draw()
        myWin.flip()
        core.wait(0.1)
        myWin.flip()
            
        thisResp=None
        while thisResp==None:
            keys=event.waitKeys()
            thisResp = checkCorrect(keys)
        print thisElev
        thisStair.addData(thisResp)
        core.wait(info['ISI'])

if not os.path.isdir('ColorNulling_%s' %info['participant']):
    os.mkdir('ColorNulling_%s' %info['participant'])

for thisStair in stairs:
    fName = 'ColorNulling_%s//ColorNulling_%s_%s_%s' %(info['participant'], thisStair.extraInfo['participant'], thisStair.extraInfo['condition'], info['dateStr'])
    thisStair.saveAsExcel(fileName=fName, sheetName='RawData', matrixOnly = False, appendFile=True)
    thisStair.saveAsPickle(fName)