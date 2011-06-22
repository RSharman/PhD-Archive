#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.62.00), May 24, 2011, at 16:05
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from numpy import * #many different maths functions
from numpy.random import * #maths randomisation functions
import os #handy system and path functions
from psychopy import core, data, event, visual, gui
import psychopy.log #import like this so it doesn't interfere with numpy.log

#User-defined variables = ['balloonBody', 'balloonValMsg', 'bankButton', 'bankedMsg', 'checkKeys', 'checkPopped', 'doneKey', 'feedback', 'feedbackMsg', 'finalScore', 'finalScore_2', 'instrMessage', 'instructions', 'reminderMsg', 'resp', 'setBalloonSize', 'trial', 'trials', 'updateEarnings']
known_name_collisions = None  #(collisions are bad)

#store info about the experiment
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
psychopy.log.console.setLevel(psychopy.log.warning)#this outputs to the screen, not a file
logFile=psychopy.log.LogFile(filename+'.log', level=psychopy.log.WARNING)

#setup the Window
win = visual.Window(size=[2560, 1440], fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#Initialise components for routine:instructions
instructionsClock=core.Clock()
instrMessage=visual.TextStim(win=win, ori=0,
    text="This is a game where you have to optimise your earnings in a balloon pumping competition.\n\nYou get prize money for each balloon you pump up, according to its size. But if you pump it too far it will pop and you'll get nothing for that balloon.\n\nBalloons differ in their maximum size - they can occasionally reach to almost the size of the screen but most will pop well before that.\n\nPress;\n    SPACE to pump the balloon\n    RETURN to bank the cash for this balloon and move onto the next\n",
    font='Arial',
    pos=[0, 0], height=0.05,
    color='white', colorSpace='rgb')

#set up handler to look after randomisation of trials etc
trials=data.TrialHandler(nReps=1.0, method='random', extraInfo=expInfo, 
    trialList=data.importTrialList('trialTypes.xlsx'))
thisTrial=trials.trialList[0]#so we can initialise stimuli with some values
#abbrieviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial!=None:
    for paramName in thisTrial.keys():
        exec(paramName+'=thisTrial.'+paramName)

#Initialise components for routine:trial
trialClock=core.Clock()
bankedEarnings=0.0
lastBalloonEarnings=0.0
thisBalloonEarnings=0.0
balloonSize=0.08
balloonMsgHeight=0.01
balloonBody=visual.PatchStim(win=win, tex='redBalloon.png', mask='None',
    ori=0, pos=[-1+balloonSize/2, 0], size=balloonSize, sf=1, phase=0.0,
    color='white', colorSpace='rgb',
    texRes=512, units='norm', interpolate=False)
reminderMsg=visual.TextStim(win=win, ori=0,
    text='Press SPACE to pump the balloon\nPress RETURN to bank this sum',
    font='Arial',
    pos=[0, -0.8], height=0.05,
    color='white', colorSpace='rgb')
balloonValMsg=visual.TextStim(win=win, ori=0,
    text=u"This balloon value:\n£%.2f" %thisBalloonEarnings,
    font='Arial',
    pos=[0,0.05], height=0.1,
    color='white', colorSpace='rgb')
bankedMsg=visual.TextStim(win=win, ori=0,
    text=u"You have banked:\n£%.2f" %bankedEarnings,
    font='Arial',
    pos=[0, 0.8], height=0.1,
    color='white', colorSpace='rgb')


#Initialise components for routine:feedback
feedbackClock=core.Clock()
feedbackText=""
from psychopy import sound
bang = sound.Sound("bang.wav")

feedbackMsg=visual.TextStim(win=win, ori=0,
    text=feedbackText,
    font='Arial',
    pos=[0, 0], height=0.1,
    color='white', colorSpace='rgb')

#Initialise components for routine:finalScore
finalScoreClock=core.Clock()
finalScore_2=visual.TextStim(win=win, ori=0,
    text=u"Well done! You banked a total of\n£%2.f" %bankedEarnings,
    font='Arial',
    pos=[0, 0], height=0.1,
    color='white', colorSpace='rgb')

#update component parameters for each repeat
resp = event._BuilderKeyResponse() #create an object of type KeyResponse

#run the trial
continueInstructions=True
t=0; instructionsClock.reset()
while continueInstructions and (t<1000000.0000):
    #get current time
    t=instructionsClock.getTime()
    
    #update/draw components on each frame
    if (0.0 <= t):
        instrMessage.draw()
    if (0.0 <= t):
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            resp.keys=theseKeys[-1]#just the last key pressed
            #abort routine on response
            continueInstructions=False
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    win.flip()

#end of this routine (e.g. trial)

for thisTrial in trials:
    #abbrieviate parameter names if possible (e.g. rgb=thisTrial.rgb)
    if thisTrial!=None:
        for paramName in thisTrial.keys():
            exec(paramName+'=thisTrial.'+paramName)
    
    #update component parameters for each repeat
    
    balloonSize=0.08
    popped=False
    nPumps=0
    
    bankButton = event._BuilderKeyResponse() #create an object of type KeyResponse
    
    #run the trial
    continueTrial=True
    t=0; trialClock.reset()
    while continueTrial and (t<1000000.0000):
        #get current time
        t=trialClock.getTime()
        
        #update/draw components on each frame
        thisBalloonEarnings=nPumps*0.05
        balloonSize=0.1+nPumps*0.015
        if (0.0 <= t):
            balloonBody.setPos([-1+balloonSize/2, 0])
            balloonBody.setSize(balloonSize)
            balloonBody.draw()
        if (0.0 <= t):
            reminderMsg.draw()
        if (0.0 <= t):
            balloonValMsg.setText(u"This balloon value:\n£%.2f" %thisBalloonEarnings)
            balloonValMsg.draw()
        if (0.0 <= t):
            bankedMsg.setText(u"You have banked:\n£%.2f" %bankedEarnings)
            bankedMsg.draw()
        if event.getKeys(['space']):
          nPumps=nPumps+1
          if nPumps>maxPumps:
            popped=True
            continueTrial=False
        if (0.0 <= t):
            if bankButton.clockNeedsReset:
                bankButton.clock.reset() # now t=0
                bankButton.clockNeedsReset = False
            theseKeys = event.getKeys(keyList='["return"]')
            if len(theseKeys)>0:#at least one key was pressed
                bankButton.rt = bankButton.clock.getTime()
                #abort routine on response
                continueTrial=False
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        win.flip()
    
    #end of this routine (e.g. trial)
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
    
    
    
    
    #update component parameters for each repeat
    if popped==True:
      feedbackText="Oops! Lost that one!"
      bang.play()
    else:
      feedbackText=u"You banked £%.2f" %lastBalloonEarnings
    
    feedbackMsg.setText(feedbackText)
    
    #run the trial
    continueFeedback=True
    t=0; feedbackClock.reset()
    while continueFeedback and (t<1.5000):
        #get current time
        t=feedbackClock.getTime()
        
        #update/draw components on each frame
        
        if (0.0 <= t < (0.0+1.5)):
            feedbackMsg.draw()
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        win.flip()
    
    #end of this routine (e.g. trial)
    

#completed 1.0 repeats of 'trials'

trials.saveAsPickle(filename+'trials')
trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
    stimOut=['imageFile', 'maxPumps', ],
    dataOut=['n','all_mean','all_std', 'all_raw'])

#update component parameters for each repeat
finalScore_2.setText(u"Well done! You banked a total of\n£%2.f" %bankedEarnings)
doneKey = event._BuilderKeyResponse() #create an object of type KeyResponse

#run the trial
continueFinalscore=True
t=0; finalScoreClock.reset()
while continueFinalscore and (t<1000000.0000):
    #get current time
    t=finalScoreClock.getTime()
    
    #update/draw components on each frame
    if (0.0 <= t):
        finalScore_2.draw()
    if (0.0 <= t):
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            doneKey.keys=theseKeys[-1]#just the last key pressed
            #abort routine on response
            continueFinalscore=False
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    win.flip()

#end of this routine (e.g. trial)





#Shutting down:
win.close()
core.quit()
