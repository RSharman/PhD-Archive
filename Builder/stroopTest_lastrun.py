#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.64.00), June 21, 2011, at 18:59
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from numpy import * #many different maths functions
from numpy.random import * #maths randomisation functions
import os #handy system and path functions
from psychopy import core, data, event, visual, gui
import psychopy.log #import like this so it doesn't interfere with numpy.log

#User-defined variables = ['FeedBack', u'Instruct', 'Instructions', u'feedBack', u'feedBackText', 'key_resp', u'key_resp_2', u'stroop', 'trial', u'trials']
known_name_collisions = None  #(collisions are bad)

#store info about the experiment
expName='stroopTest'#from the Builder filename that created this script
expInfo={'participant':'', 'session':'001'}
dlg=gui.DlgFromDict(dictionary=expInfo,title=expName)
if dlg.OK==False: core.quit() #user pressed cancel
expInfo['date']=data.getDateStr()#add a simple timestamp
expInfo['expName']=expName
#setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data') #if this fails (e.g. permissions) we will get error
filename='data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
psychopy.log.console.setLevel(psychopy.log.warning)#this outputs to the screen, not a file
logFile=psychopy.log.LogFile(filename+'.log', level=psychopy.log.EXP)

#setup the Window
win = visual.Window(size=[1024, 768], fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

#Initialise components for routine:Instructions
InstructionsClock=core.Clock()
Instruct=visual.TextStim(win=win, ori=0,
    text=u'Press the key that corresponds to the colour of the text\nred = left\ngreen = down\nblue = right\nPress any key to continue',
    font=u'Arial',
    pos=[0, 0], height=0.1,
    color=u'white', colorSpace=u'rgb')

#set up handler to look after randomisation of trials etc
trials=data.TrialHandler(nReps=1, method=u'random', 
    extraInfo=expInfo, originPath=u'C:\\Documents and Settings\\lpxrs\\My Documents\\Code\\Experiments\\Builder\\stroopTest.psyexp',
    trialList=data.importTrialList(u'trialTypes.xlsx'))
thisTrial=trials.trialList[0]#so we can initialise stimuli with some values
#abbrieviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial!=None:
    for paramName in thisTrial.keys():
        exec(paramName+'=thisTrial.'+paramName)

#Initialise components for routine:trial
trialClock=core.Clock()
stroop=visual.TextStim(win=win, ori=0,
    text=text,
    font=u'Arial',
    pos=[0, 0], height=0.1,
    color=letterColor, colorSpace=u'rgb')

#Initialise components for routine:FeedBack
FeedBackClock=core.Clock()
msg="x"
feedBackText=visual.TextStim(win=win, ori=0,
    text=msg,
    font=u'Arial',
    pos=[0, 0], height=0.1,
    color=u'white', colorSpace=u'rgb')

#update component parameters for each repeat
key_resp_2 = event._BuilderKeyResponse() #create an object of type KeyResponse

#run the trial
continueInstructions=True
t=0; InstructionsClock.reset()
while continueInstructions and (t<1000000.0000):
    #get current time
    t=InstructionsClock.getTime()
    
    #update/draw components on each frame
    if (0.0 <= t):
        Instruct.draw()
    if (0.0 <= t):
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            key_resp_2.keys=theseKeys[-1]#just the last key pressed
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
    stroop.setColor(letterColor, colorSpace=u'rgb')
    stroop.setText(text)
    key_resp = event._BuilderKeyResponse() #create an object of type KeyResponse
    
    #run the trial
    continueTrial=True
    t=0; trialClock.reset()
    while continueTrial and (t<1000000.0000):
        #get current time
        t=trialClock.getTime()
        
        #update/draw components on each frame
        if (0.0 <= t):
            stroop.draw()
        if (0.0 <= t):
            if key_resp.clockNeedsReset:
                key_resp.clock.reset() # now t=0
                key_resp.clockNeedsReset = False
            theseKeys = event.getKeys(keyList=u'["left","down","right"]')
            if len(theseKeys)>0:#at least one key was pressed
                key_resp.keys=theseKeys[-1]#just the last key pressed
                key_resp.rt = key_resp.clock.getTime()
                #was this 'correct'?
                if (key_resp.keys==str(corrAns)): key_resp.corr=1
                else: key_resp.corr=0
                #abort routine on response
                continueTrial=False
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        win.flip()
    
    #end of this routine (e.g. trial)
    if len(key_resp.keys)>0:#we had a response
        trials.addData('key_resp.keys',key_resp.keys)
        trials.addData('key_resp.corr',key_resp.corr)
        trials.addData('key_resp.rt',key_resp.rt)
    
    #update component parameters for each repeat
    if key_resp.corr:#stored on last run routine
      msg="Correct! RT=%.3f" %(key_resp.rt)
    else:
      msg="Oops! That was wrong"
    feedBackText.setText(msg)
    
    #run the trial
    continueFeedback=True
    t=0; FeedBackClock.reset()
    while continueFeedback and (t<0.5000):
        #get current time
        t=FeedBackClock.getTime()
        
        #update/draw components on each frame
        
        if (0.0 <= t < (0.0+0.5)):
            feedBackText.draw()
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        win.flip()
    
    #end of this routine (e.g. trial)
    

#completed 1 repeats of 'trials'

trials.saveAsPickle(filename+'trials')
trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
    stimOut=['text', 'congruent', 'corrAns', 'letterColor', ],
    dataOut=['n','all_mean','all_std', 'all_raw'])


#Shutting down:
win.close()
core.quit()
