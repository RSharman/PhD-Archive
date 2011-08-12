#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.64.00), July 19, 2011, at 14:52
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from numpy import * #many different maths functions
from numpy.random import * #maths randomisation functions
import os #handy system and path functions
from psychopy import core, data, event, visual, gui
import psychopy.log #import like this so it doesn't interfere with numpy.log
from psychopy.constants import *

#User-defined variables = ['Afixation', 'Instr', u'LAdapt', u'LGabor', u'RAdapt', u'RGabor', 'adaptation', 'fixation', 'key_resp', 'key_resp_2', 'stairs', 'text', 'trial']
known_name_collisions = None  #(collisions are bad)

#store info about the experiment
expName='None'#from the Builder filename that created this script
expInfo={'participant':'', 'session':'001', 'ori':''}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
psychopy.log.console.setLevel(psychopy.log.WARNING)#this outputs to the screen, not a file
logFile=psychopy.log.LogFile(filename+'.log', level=psychopy.log.EXP)

#setup the Window
win = visual.Window(size=[1920, 1080], fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=[0,0,0], colorSpace=u'rgb')

#Initialise components for routine:Instr
InstrClock=core.Clock()
text=visual.TextStim(win=win, ori=0,
    text='Press left or right to indicate the highest frequency patch',
    font='Arial',
    pos=[0, 0], height=0.1,
    color='white', colorSpace='rgb')

#Initialise components for routine:adaptation
adaptationClock=core.Clock()
LAdapt=visual.PatchStim(win=win, tex=u'sin', mask=u'gauss',
    ori=0, pos=[-3, 0], size=[3.0,3.0], sf=0.8, phase=random(),
    color=[1,1,1], colorSpace=u'rgb',
    texRes=128, units=u'deg', interpolate=False)
RAdapt=visual.PatchStim(win=win, tex=u'sin', mask=u'gauss',
    ori=0, pos=[3, 0], size=[3, 3], sf=1.0, phase=random(),
    color=[1,1,1], colorSpace=u'rgb',
    texRes=128, units=u'deg', interpolate=False)
Afixation=visual.PatchStim(win=win, tex='none', mask='circle',
    ori=0, pos=[0, 0], size=[0.1, 0.1], sf=None, phase=0.0,
    color=[-1,-1,-1], colorSpace='rgb',
    texRes=128, units='deg', interpolate=False)

#set up handler to look after randomisation of trials etc
stairs=data.StairHandler(startVal=0.5, extraInfo=expInfo,
    stepSizes=asarray([0.8,0.8,0.4,0.4,0.2]), stepType='log',
    nReversals=0, nTrials=1, 
    nUp=1, nDown=3,
    originPath=u'C:\\Documents and Settings\\lpxrs\\My Documents\\Code\\Experiments\\Builder Demos\\SfTest2.psyexp')
level=thisStair=0.5#initialise some vals

#Initialise components for routine:trial
trialClock=core.Clock()
LGabor=visual.PatchStim(win=win, tex=u'sin', mask=u'gauss',
    ori=expInfo['ori'], pos=[-3, 0], size=[3, 3], sf=level, phase=0.0,
    color=[1,1,1], colorSpace=u'rgb',
    texRes=128, units=u'deg', interpolate=False)
RGabor=visual.PatchStim(win=win, tex=u'sin', mask=u'gauss',
    ori=expInfo['ori'], pos=[3, 0], size=[3, 3], sf=None, phase=0.0,
    color=[1,1,1], colorSpace=u'rgb',
    texRes=128, units=u'deg', interpolate=False)
fixation=visual.PatchStim(win=win, tex='none', mask='circle',
    ori=0, pos=[0, 0], size=[0.1, 0.1], sf=None, phase=0.0,
    color=[-1,-1,-1], colorSpace='rgb',
    texRes=128, units='deg', interpolate=False)

#update component parameters for each repeat
key_resp_2Status=NOT_STARTED
key_resp_2 = event._BuilderKeyResponse() #create an object of type KeyResponse

#run Instr
continueRoutine=True
t=0; InstrClock.reset()
while continueRoutine and (t<1000000.0000):
    #get current time
    t=InstrClock.getTime()
    
    #update/draw components on each frame
    if (0.0 <= t):
        text.draw()
    if (0.0 <= t):
        if key_resp_2Status==NOT_STARTED:
            #keyboard checking is just starting
            event.clearEvents()
            key_resp_2Status=STARTED
        if key_resp_2.clockNeedsReset:
            key_resp_2.clock.reset() # now t=0
            key_resp_2.clockNeedsReset = False
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            key_resp_2.keys=theseKeys[-1]#just the last key pressed
            key_resp_2.rt = key_resp_2.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    win.flip()

#end of this routine (e.g. trial)

#update component parameters for each repeat

#run adaptation
continueRoutine=True
t=0; adaptationClock.reset()
while continueRoutine and (t<5.0000):
    #get current time
    t=adaptationClock.getTime()
    
    #update/draw components on each frame
    if (0.0 <= t < (0.0+5.0)):
        LAdapt.setPhase(random())
        LAdapt.draw()
    if (0.0 <= t < (0.0+5.0)):
        RAdapt.setPhase(random())
        RAdapt.draw()
    if (0.0 <= t < (0.0+5.0)):
        Afixation.draw()
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    win.flip()

#end of this routine (e.g. trial)

for thisStair in stairs:
    currentLoop = stairs
    level=thisStair
    
    #update component parameters for each repeat
    LGabor.setSF(level)
    key_respStatus=NOT_STARTED
    key_resp = event._BuilderKeyResponse() #create an object of type KeyResponse
    
    #run trial
    continueRoutine=True
    t=0; trialClock.reset()
    while continueRoutine and (t<1000000.0000):
        #get current time
        t=trialClock.getTime()
        
        #update/draw components on each frame
        if (0.0 <= t < (0.0+1)):
            LGabor.draw()
        if (0.0 <= t < (0.0+1.0)):
            RGabor.draw()
        if (0.0 <= t < (0.0+1.0)):
            fixation.draw()
        if (0.0 <= t):
            if key_respStatus==NOT_STARTED:
                #keyboard checking is just starting
                event.clearEvents()
                key_respStatus=STARTED
            theseKeys = event.getKeys(keyList='["left","right"]')
            if len(theseKeys)>0:#at least one key was pressed
                key_resp.keys=theseKeys[-1]#just the last key pressed
                #was this 'correct'?
                if (key_resp.keys==str('left')): key_resp.corr=1
                else: key_resp.corr=0
                #abort routine on response
                continueRoutine=False
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        win.flip()
    
    #end of this routine (e.g. trial)
    #check responses
    if len(key_resp.keys)==0: #No response was made
       key_resp.keys=None
       #was no response the correct answer?!
       if str('left').lower()=='none':key_resp.corr=1 #correct non-response
       else: key_resp.corr=0 #failed to respond (incorrectly)
    #store data for stairs (StairHandler)
    stairs.addData(key_resp.corr)

#staircase completed

stairs.saveAsPickle(filename+'stairs')
stairs.saveAsExcel(filename+'.xlsx', sheetName='stairs')

#Shutting down:
win.close()
core.quit()
