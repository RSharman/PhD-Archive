#Practice Dyslexia Vernier Acuity/Judgement of Absolute Phase - January 2011

import copy, string, scipy, os, time
import numpy as num
from psychopy import visual, core, event, data, gui, sound, monitors, misc, filters

DEBUG=True

if DEBUG:
    myMon = 'testMonitor'
    allowGUI = True
    fullscr=False
    bitsMode=None
else:
    allowGUI = False
    fullscr=True
    myMon = 'sparrow'
    allowGUI = False
    bitsMode = 'fast'

    #Create a dialog box for participant information
try:
    info = misc.fromFile('lastParams.pickle')
except:
    info = {'participant' : 'RJS'}
info['dateStr']=time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Dyslexia Vernier Acuity Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', info)
else:
    core.quit()

#Basic Information
info['baseSF']=1.0
info['patchSize']=3.0
info['monitorDist']=52.0
info['nComponents']=30
info['displayT']=1
info['ISI']=1.0
info['cycles']=1 #number of times the trial handler will cycle through the conditions
reactionClock = core.Clock()
tick = sound.Sound('A', octave=6, secs=0.01); tick.setVolume(0.3)
error = sound.Sound('C', octave=4, secs=0.75); tick.setVolume(0.6)

#Create window and fixation
myWin = visual.Window(size=(1024,768), monitor=myMon, units = 'degs', 
    fullscr=fullscr, allowGUI=allowGUI, bitsMode=bitsMode)
fixation = visual.PatchStim(myWin, size=0.1, tex=None, mask='circle', rgb=-1)

#Start Message
startMessage = visual.TextStim(myWin, pos=(0, -4), height=1, rgb=-1, 
                                        text="This is a short practice trial. Please press up or down to indicate whether the right patch is lower or higher than the left patch. Press any key to continue")
startMessage.draw()
fixation.draw()
myWin.flip()
junk = event.waitKeys()

#Create stimuli
leftField=scipy.array([2,0])
rightField=scipy.array([-2,0])

leftPatch=visual.PatchStim(myWin,
                                          mask='gauss',
                                          sf=info['baseSF'],
                                          size=info['patchSize'],
                                          pos=leftField,
                                          ori=90)
                                          
rightPatch=visual.PatchStim(myWin,
                                          mask='gauss',
                                          sf=info['baseSF'],
                                          size=info['patchSize'],
                                          pos=rightField,
                                          ori=90)

def setGratingPhase(phaseForm, patch) :
    texture=num.zeros((256,256),'d')
    maxPeak = 0
    for thisSF in num.arange(1,2*info['nComponents']+1,2):
        texture+=filters.makeGrating(256,cycles=thisSF,phase=phaseForm)/thisSF
        maxPeak = maxPeak+1.0/thisSF
    texture/=maxPeak
    patch.setTex(texture)

#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit() #quit
        elif key in ['up', 'down']:#valid response
            if thisTrial['absPhase'] <0:
                if (key in ['up']):
                    error.play()
                    return 0 #test patch is higher than reference patch
                elif (key in ['down']): 
                    return 1 #test patch is lower than reference patch
            if thisTrial['absPhase'] >0:
                if (key in ['up']):
                    return 1 #test patch is higher than reference patch
                elif (key in ['down']): 
                    error.play()
                    return 0 #test patch is lower than reference patch
        else:
            print "hit up or down (or q) (you hit %s)" %key
            return None
            
#Setting the phase of the reference patch
setGratingPhase(90, leftPatch)

#Trial Handler
stimList = data.importTrialList('PracticeVernierList.xlsx')
trials = data.TrialHandler(stimList, info['cycles'])
trials.data.addDataType('response') #1 for higher, 0 for lower

nDone=0
for thisTrial in trials:
    setGratingPhase(90, rightPatch)
    rightPatch.setPhase(thisTrial['absPhase'])
    
#    print thisTrial
    reactionClock.reset()#start RT timer
    fixation.draw()
    leftPatch.draw()
    rightPatch.draw()
    myWin.flip()
    core.wait(info['displayT'])
    
    myWin.getMovieFrame()
    myWin.saveMovieFrames('Acuity.jpg')
    
    if DEBUG==False:
        tick.play()
    fixation.draw()
    myWin.flip()
    
    #Collect Participant Response
    thisResp = None

    while thisResp == None:
        keys = event.waitKeys()
        thisResp = checkCorrect(keys)
    thisRT=reactionClock.getTime()
    trials.data.add('response', thisResp)
    trials.data.add('RT', thisRT)
    nDone += 1  
    
    fixation.draw()
    myWin.update()
    core.wait(info['ISI'])
    
for key in event.getKeys():
    if key in['q']:
        core.quit()

core.quit()
