#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.65.01), December 09, 2011, at 13:26
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
import numpy as np  # whole numpy lib is available, pre-pend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os #handy system and path functions
from psychopy import core, data, event, visual, gui
import psychopy.log #import like this so it doesn't interfere with numpy.log
from psychopy.constants import *

#store info about the experiment session
expName='None'#from the Builder filename that created this script
expInfo={'participant':'', 'gender (m/f)':'', 'age':'', 'session':'004'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile=psychopy.log.LogFile(filename+'.log', level=psychopy.log.WARNING)
psychopy.log.console.setLevel(psychopy.log.WARNING)#this outputs to the screen, not a file

#setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#Initialise components for routine:instructions
instructionsClock=core.Clock()
instrMessage=visual.TextStim(win=win, ori=0, name='instrMessage',
    text="This is a game where you have to optimise your earnings in a balloon pumping competition.\n\nYou get prize money for each balloon you pump up, according to its size. But if you pump it too far it will pop and you'll get nothing for that balloon.\n\nBalloons differ in their maximum size - they can occasionally reach to almost the size of the screen but most will pop well before that.\n\nPress;\n    SPACE to pump the balloon\n    RETURN to bank the cash for this balloon and move onto the next\n",
    font='Arial',
    pos=[0, 0], height=0.05,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

#Initialise components for routine:trial
trialClock=core.Clock()
bankedEarnings=0.0
lastBalloonEarnings=0.0
thisBalloonEarnings=0.0
balloonSize=0.08
balloonMsgHeight=0.01
balloonBody=visual.PatchStim(win=win, name='balloonBody',units='norm', 
    tex='redBalloon.png', mask=None,
    ori=0, pos=[0,0], size=1.0, sf=1, phase=0.0,
    color='white', colorSpace='rgb', opacity=1,
    texRes=512, interpolate=False, depth=-2.0)
reminderMsg=visual.TextStim(win=win, ori=0, name='reminderMsg',
    text='Press SPACE to pump the balloon\nPress RETURN to bank this sum',
    font='Arial',
    pos=[0, -0.8], height=0.05,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-3.0)
balloonValMsg=visual.TextStim(win=win, ori=0, name='balloonValMsg',
    text='nonsense',
    font='Arial',
    pos=[0,0.05], height=0.1,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-4.0)
bankedMsg=visual.TextStim(win=win, ori=0, name='bankedMsg',
    text='nonsense',
    font='Arial',
    pos=[0, 0.8], height=0.1,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-5.0)


#Initialise components for routine:feedback
feedbackClock=core.Clock()
feedbackText=""
from psychopy import sound
bang = sound.Sound("bang.wav")

feedbackMsg=visual.TextStim(win=win, ori=0, name='feedbackMsg',
    text='nonsense',
    font='Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

#Initialise components for routine:finalScore
finalScoreClock=core.Clock()
finalScore_2=visual.TextStim(win=win, ori=0, name='finalScore_2',
    text='nonsense',
    font='Arial',
    pos=[0, 0], height=0.1,wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

#Start of routine instructions
t=0; instructionsClock.reset()
frameN=-1

#update component parameters for each repeat
resp = event.BuilderKeyResponse() #create an object of type KeyResponse
resp.status=NOT_STARTED
#keep track of which have finished
instructionsComponents=[]#to keep track of which have finished
instructionsComponents.append(instrMessage)
instructionsComponents.append(resp)
for thisComponent in instructionsComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=instructionsClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*instrMessage* updates
    if t>=0.0 and instrMessage.status==NOT_STARTED:
        #keep track of start time/frame for later
        instrMessage.tStart=t#underestimates by a little under one frame
        instrMessage.frameNStart=frameN#exact frame index
        instrMessage.setAutoDraw(True)
    
    #*resp* updates
    if t>=0.0 and resp.status==NOT_STARTED:
        #keep track of start time/frame for later
        resp.tStart=t#underestimates by a little under one frame
        resp.frameNStart=frameN#exact frame index
        resp.status=STARTED
        #keyboard checking is just starting
        resp.clock.reset() # now t=0
        event.clearEvents()
    if resp.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            resp.keys=theseKeys[-1]#just the last key pressed
            resp.rt = resp.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine instructions
for thisComponent in instructionsComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)

#set up handler to look after randomisation of conditions etc
trials=data.TrialHandler(nReps=1.0, method='random', 
    extraInfo=expInfo, originPath='C:\\Documents and Settings\\lpxrs\\My Documents\\Code\\Experiments\\Builder Demos\\PsychoPy2 Demos\\BART\\bart.psyexp',
    trialList=data.importConditions(u'trialTypes.xlsx'),
    seed=None)
thisTrial=trials.trialList[0]#so we can initialise stimuli with some values
#abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial!=None:
    for paramName in thisTrial.keys():
        exec(paramName+'=thisTrial.'+paramName)

for thisTrial in trials:
    currentLoop = trials
    #abbrieviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial!=None:
        for paramName in thisTrial.keys():
            exec(paramName+'=thisTrial.'+paramName)
    
    #Start of routine trial
    t=0; trialClock.reset()
    frameN=-1
    
    #update component parameters for each repeat
    
    balloonSize=0.08
    popped=False
    nPumps=0
    
    bankButton = event.BuilderKeyResponse() #create an object of type KeyResponse
    bankButton.status=NOT_STARTED
    #keep track of which have finished
    trialComponents=[]#to keep track of which have finished
    trialComponents.append(balloonBody)
    trialComponents.append(reminderMsg)
    trialComponents.append(balloonValMsg)
    trialComponents.append(bankedMsg)
    trialComponents.append(bankButton)
    for thisComponent in trialComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=trialClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        thisBalloonEarnings=nPumps*0.05
        balloonSize=0.1+nPumps*0.015
        
        #*balloonBody* updates
        if t>=0.0 and balloonBody.status==NOT_STARTED:
            #keep track of start time/frame for later
            balloonBody.tStart=t#underestimates by a little under one frame
            balloonBody.frameNStart=frameN#exact frame index
            balloonBody.setAutoDraw(True)
        if balloonBody.status==STARTED:#only update if being drawn
            balloonBody.setPos([-1+balloonSize/2, 0])
            balloonBody.setSize(balloonSize)
        
        #*reminderMsg* updates
        if t>=0.0 and reminderMsg.status==NOT_STARTED:
            #keep track of start time/frame for later
            reminderMsg.tStart=t#underestimates by a little under one frame
            reminderMsg.frameNStart=frameN#exact frame index
            reminderMsg.setAutoDraw(True)
        
        #*balloonValMsg* updates
        if t>=0.0 and balloonValMsg.status==NOT_STARTED:
            #keep track of start time/frame for later
            balloonValMsg.tStart=t#underestimates by a little under one frame
            balloonValMsg.frameNStart=frameN#exact frame index
            balloonValMsg.setAutoDraw(True)
        if balloonValMsg.status==STARTED:#only update if being drawn
            balloonValMsg.setText(u"This balloon value:\n£%.2f" %thisBalloonEarnings)
        
        #*bankedMsg* updates
        if t>=0.0 and bankedMsg.status==NOT_STARTED:
            #keep track of start time/frame for later
            bankedMsg.tStart=t#underestimates by a little under one frame
            bankedMsg.frameNStart=frameN#exact frame index
            bankedMsg.setAutoDraw(True)
        if bankedMsg.status==STARTED:#only update if being drawn
            bankedMsg.setText(u"You have banked:\n£%.2f" %bankedEarnings)
        if event.getKeys(['space']):
          nPumps=nPumps+1
          if nPumps>maxPumps:
            popped=True
            continueTrial=False
        
        #*bankButton* updates
        if t>=0.0 and bankButton.status==NOT_STARTED:
            #keep track of start time/frame for later
            bankButton.tStart=t#underestimates by a little under one frame
            bankButton.frameNStart=frameN#exact frame index
            bankButton.status=STARTED
            #keyboard checking is just starting
            event.clearEvents()
        if bankButton.status==STARTED:#only update if being drawn
            theseKeys = event.getKeys(keyList=['return'])
            if len(theseKeys)>0:#at least one key was pressed
                #abort routine on response
                continueRoutine=False
        
        #check if all components have finished
        if not continueRoutine:
            break # lets a component forceEndRoutine
        continueRoutine=False#will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                continueRoutine=True; break#at least one component has not yet finished
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #end of routine trial
    for thisComponent in trialComponents:
        if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
    #calculate cash 'earned'
    if popped:
      thisBalloonEarnings=0.0
      lastBalloonEarnings=0.0
    else:   lastBalloonEarnings=thisBalloonEarnings
    bankedEarnings = bankedEarnings+lastBalloonEarnings
    #save data
    trials.addData('nPumps', nPumps)
    trials.addData('size', balloonSize)
    trials.addData('earnings', thisBalloonEarnings)
    trials.addData('popped', popped)
    
    
    
    
    #Start of routine feedback
    t=0; feedbackClock.reset()
    frameN=-1
    
    #update component parameters for each repeat
    if popped==True:
      feedbackText="Oops! Lost that one!"
      bang.play()
    else:
      feedbackText=u"You banked £%.2f" %lastBalloonEarnings
    
    feedbackMsg.setText(feedbackText)
    #keep track of which have finished
    feedbackComponents=[]#to keep track of which have finished
    feedbackComponents.append(feedbackMsg)
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
    #start the Routine
    continueRoutine=True
    while continueRoutine:
        #get current time
        t=feedbackClock.getTime()
        frameN=frameN+1#number of completed frames (so 0 in first frame)
        #update/draw components on each frame
        
        
        #*feedbackMsg* updates
        if t>=0.0 and feedbackMsg.status==NOT_STARTED:
            #keep track of start time/frame for later
            feedbackMsg.tStart=t#underestimates by a little under one frame
            feedbackMsg.frameNStart=frameN#exact frame index
            feedbackMsg.setAutoDraw(True)
        elif feedbackMsg.status==STARTED and t>=(0.0+1.5):
            feedbackMsg.setAutoDraw(False)
        
        #check if all components have finished
        if not continueRoutine:
            break # lets a component forceEndRoutine
        continueRoutine=False#will revert to True if at least one component still running
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
                continueRoutine=True; break#at least one component has not yet finished
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #end of routine feedback
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)
    

#completed 1.0 repeats of 'trials'

trials.saveAsPickle(filename+'trials')
trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
    stimOut=trials.trialList[0].keys(),
    dataOut=['n','all_mean','all_std', 'all_raw'])

#Start of routine finalScore
t=0; finalScoreClock.reset()
frameN=-1

#update component parameters for each repeat
finalScore_2.setText(u"Well done! You banked a total of\n£%2.f" %bankedEarnings)
doneKey = event.BuilderKeyResponse() #create an object of type KeyResponse
doneKey.status=NOT_STARTED
#keep track of which have finished
finalScoreComponents=[]#to keep track of which have finished
finalScoreComponents.append(finalScore_2)
finalScoreComponents.append(doneKey)
for thisComponent in finalScoreComponents:
    if hasattr(thisComponent,'status'): thisComponent.status = NOT_STARTED
#start the Routine
continueRoutine=True
while continueRoutine:
    #get current time
    t=finalScoreClock.getTime()
    frameN=frameN+1#number of completed frames (so 0 in first frame)
    #update/draw components on each frame
    
    #*finalScore_2* updates
    if t>=0.0 and finalScore_2.status==NOT_STARTED:
        #keep track of start time/frame for later
        finalScore_2.tStart=t#underestimates by a little under one frame
        finalScore_2.frameNStart=frameN#exact frame index
        finalScore_2.setAutoDraw(True)
    
    #*doneKey* updates
    if t>=0.0 and doneKey.status==NOT_STARTED:
        #keep track of start time/frame for later
        doneKey.tStart=t#underestimates by a little under one frame
        doneKey.frameNStart=frameN#exact frame index
        doneKey.status=STARTED
        #keyboard checking is just starting
        doneKey.clock.reset() # now t=0
        event.clearEvents()
    if doneKey.status==STARTED:#only update if being drawn
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            doneKey.keys=theseKeys[-1]#just the last key pressed
            doneKey.rt = doneKey.clock.getTime()
            #abort routine on response
            continueRoutine=False
    
    #check if all components have finished
    if not continueRoutine:
        break # lets a component forceEndRoutine
    continueRoutine=False#will revert to True if at least one component still running
    for thisComponent in finalScoreComponents:
        if hasattr(thisComponent,"status") and thisComponent.status!=FINISHED:
            continueRoutine=True; break#at least one component has not yet finished
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    if continueRoutine:#don't flip if this routine is over or we'll get a blank screen
        win.flip()

#end of routine finalScore
for thisComponent in finalScoreComponents:
    if hasattr(thisComponent,"setAutoDraw"): thisComponent.setAutoDraw(False)





#Shutting down:
win.close()
core.quit()
