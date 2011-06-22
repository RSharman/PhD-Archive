#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.50.04), June 21, 2011, at 17:58
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""
from numpy import * #many different maths functions
from numpy.random import * #maths randomisation functions
import os #handy system and path functions
from psychopy import core, data, event, visual, gui
import psychopy.log #import like this so it doesn't interfere with numpy.log

#User-defined variables = ['instrText', 'instruct', 'ready', 'resp', 'thanks', 'thanksText', 'trial', 'trials', 'word']
known_name_collisions = None  #(collisions are bad)

#store info about the experiment
expName='None'#from the Builder filename that created this script
expInfo={'participant':'', 'session':'01'}
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
    monitor='testMonitor', color='black', colorSpace='rgb', units='norm')

#Initialise components for routine:instruct
instructClock=core.Clock()
instrText=visual.TextStim(win=win, ori=0,
    text='OK. Ready for the real thing?\n\nRemember, ignore the word itself; press:\nLeft for red LETTERS\nDown for green LETTERS\nRight for blue LETTERS\n(Esc will quit)\n\nPress any key to continue',
    font='Arial',
    pos=[0, 0], height=0.1,
    color=[1, 1, 1], colorSpace='rgb')

#set up handler to look after randomisation of trials etc
trials=data.TrialHandler(nReps=5.0, method='random', 
    extraInfo=expInfo, originPath='C:\\Documents and Settings\\lpxrs\\My Documents\\Code\\Experiments\\Builder Demos\\stroop\\stroop.psyexp',
    trialList=data.importTrialList('trialTypes.xlsx'))
thisTrial=trials.trialList[0]#so we can initialise stimuli with some values
#abbrieviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial!=None:
    for paramName in thisTrial.keys():
        exec(paramName+'=thisTrial.'+paramName)

#Initialise components for routine:trial
trialClock=core.Clock()
word=visual.TextStim(win=win, ori=0,
    text=text,
    font='Arial',
    pos=[0, 0], height=0.2,
    color=letterColor, colorSpace='rgb')

#Initialise components for routine:thanks
thanksClock=core.Clock()
thanksText=visual.TextStim(win=win, ori=0,
    text='This is the end of the experiment.\n\nThanks!',
    font='arial',
    pos=[0, 0], height=0.2,
    color=[1, 1, 1], colorSpace='rgb')

#update component parameters for each repeat

#run the trial
continueInstruct=True
t=0; instructClock.reset()
while continueInstruct and (t<1000000.0000):
    #get current time
    t=instructClock.getTime()
    
    #update/draw components on each frame
    if (0 <= t):
        instrText.draw()
    if (0 <= t):
        theseKeys = event.getKeys()
        if len(theseKeys)>0:#at least one key was pressed
            #abort routine on response
            continueInstruct=False
    
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
    word.setColor(letterColor, colorSpace='rgb')
    word.setText(text)
    resp = event._BuilderKeyResponse() #create an object of type KeyResponse
    
    #run the trial
    continueTrial=True
    t=0; trialClock.reset()
    while continueTrial and (t<1000000.0000):
        #get current time
        t=trialClock.getTime()
        
        #update/draw components on each frame
        if (0.5 <= t):
            word.draw()
        if (0.5 <= t):
            if resp.clockNeedsReset:
                resp.clock.reset() # now t=0
                resp.clockNeedsReset = False
            theseKeys = event.getKeys(keyList='["left","down","right"]')
            if len(theseKeys)>0:#at least one key was pressed
                resp.keys=theseKeys[-1]#just the last key pressed
                resp.rt = resp.clock.getTime()
                #was this 'correct'?
                if (resp.keys==str(corrAns)): resp.corr=1
                else: resp.corr=0
                #abort routine on response
                continueTrial=False
        
        #check for quit (the [Esc] key)
        if event.getKeys(["escape"]): core.quit()
        #refresh the screen
        win.flip()
    
    #end of this routine (e.g. trial)
    if len(resp.keys)>0:#we had a response
        trials.addData('resp.keys',resp.keys)
        trials.addData('resp.corr',resp.corr)
        trials.addData('resp.rt',resp.rt)

#completed 5.0 repeats of 'trials'

trials.saveAsPickle(filename+'trials')
trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
    stimOut=['text', 'congruent', 'corrAns', 'letterColor', ],
    dataOut=['n','all_mean','all_std', 'all_raw'])

#update component parameters for each repeat

#run the trial
continueThanks=True
t=0; thanksClock.reset()
while continueThanks and (t<2.0000):
    #get current time
    t=thanksClock.getTime()
    
    #update/draw components on each frame
    if (0.0 <= t < (0.0+2.0)):
        thanksText.draw()
    
    #check for quit (the [Esc] key)
    if event.getKeys(["escape"]): core.quit()
    #refresh the screen
    win.flip()

#end of this routine (e.g. trial)

#Shutting down:
win.close()
core.quit()
