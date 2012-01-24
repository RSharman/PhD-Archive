#Staircases to find the contrast detection threshold of LM, S and Lum based edges

from psychopy import visual, event, misc, core, data, gui, monitors, sound
import numpy as np
import copy, os, random, time
from numpy.random import shuffle
import colorFunctions

#Create a dialog box for participant information
try:
    info=misc.fromFile('detParams.pickle')
except:
    info = {'participant' : 'RJS'}
info['dateStr'] = time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Synth Edge Detection', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('detParams.pickle', info)
else:
    core.quit()
   
#Create the basic information
info['conditions'] = ['LM', 'S', 'Lum']
info['ISI'] = 0.5
info['displayT'] = 0.3
info['baseContrast'] = 0
info['Blur'] = 0.03

#Staircase Information
info['nTrials'] = 2
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
    myWin = visual.Window(size=(1280, 1024), monitor = 'heron', units = 'degs', screen=1,
        fullscr=True, allowGUI=False, bitsMode='fast')
    myMon=monitors.Monitor('heron')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
fixation = visual.PatchStim(myWin, size=0.05, tex=None, mask='circle', rgb=-1)

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
startMessage = visual.TextStim(myWin, pos=(0.0,-0.6), height =0.3, rgb=-1, wrapWidth=4.0,
                                                                                        text="Please press 1 or 2 to indicate whether the stimulus is present in the first or second interval. Press any key when you are ready to continue.", )
                                                                                        
startMessage.draw()
myWin.update()
junk = event.waitKeys()

#Create multiple staircases in order interleave them
stairs = []
edges=[]

for thisCond in info['conditions']:
    thisInfo = copy.copy(info)
#    if thisCond=='LM':
#        thisInfo['condition']='LM'
#    if thisCond=='S':
#        thisInfo['condition']='S'
#    if thisCond=='Lum':
#        thisInfo['condition']='Lum'
    
    #The Staircase
    #Set Up
    thisStair = data.StairHandler(startVal=info['startVal'], 
                                                        nReversals=info['nReversals'],
                                                        stepSizes=info['stepSizes'],
                                                        stepType='lin', 
                                                        nTrials=info['nTrials'],
                                                        nUp=info['nUp'],
                                                        nDown=info['nDown'],
                                                        extraInfo=thisInfo,
                                                        minVal=info['minVal'],
                                                        maxVal=info['maxVal']
                                                        )
    thisStair.extraInfo['condition']=thisCond
    stairs.append(thisStair)

for trialN in range(info['nTrials']):
    shuffle(stairs)
    for thisStair in stairs:
        thisContrast=thisStair.next()
       
            #Create stimuli
        if thisStair.extraInfo['condition']=='LM':
            lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)*0
            lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)
            s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)*0
        if thisStair.extraInfo['condition']=='S':
            lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)*0
            lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)*0
            s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)
        if thisStair.extraInfo['condition']=='Lum':
            lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)
            lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)*0
            s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5)*0
        order = random.randint(1.0, 2.0)
       
        rgbEdge = misc.dklCart2rgb(lum, lm, s, conversionMatrix)
        
        #Draw the picture
        if order==1:
            if DEBUG==False:
                tick.play()
            img = visual.PatchStim(myWin, tex=rgbEdge, units='deg', size = 4.5, sf=(1/4.5))
            drawPicture(info['baseContrast']+thisContrast, img)
                        #Draw mask
            upperMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                                    vertices=((-5,5), (5,5), (5,0.5), (-5,0.5)))
            lowerMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                                    vertices=((-5,-5), (5,-5), (5,-0.5), (-5,-0.5)))
            upperMask.draw()
            lowerMask.draw()
            myWin.flip()
            core.wait(info['displayT'])
            fixation.draw()
            myWin.flip()
            core.wait(info['ISI'])
            myWin.flip()
            if DEBUG==False:
                tick.play()
            core.wait(info['displayT'])
           
        if order==2:
            if DEBUG==False:
                tick.play()
            img = visual.PatchStim(myWin, tex=rgbEdge, units='deg', size=4.5, sf=(1/4.5))
            myWin.flip()
            core.wait(info['displayT'])
            fixation.draw()
            myWin.flip()
            core.wait(info['ISI'])
            drawPicture(info['baseContrast']+thisContrast, img)
                   #Draw mask
            upperMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                                    vertices=((-5,5), (5,5), (5,0.5), (-5,0.5)))
            lowerMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                                    vertices=((-5,-5), (5,-5), (5,-0.5), (-5,-0.5)))
            upperMask.draw()
            lowerMask.draw() 
            myWin.flip()
            if DEBUG==False:
                tick.play()
            core.wait(info['displayT'])
        fixation.draw()
        myWin.flip()
       
       #Take Participant Response
        thisResp = None
        while thisResp==None:
            keys = event.waitKeys()
            thisResp = checkCorrect(keys)
        
        thisStair.addData(thisResp)
           
if not os.path.isdir('EdgeDetection_%s' %info['participant']):
    os.mkdir('EdgeDetection_%s' %info['participant'])
   
for thisStair in stairs:
    fName = 'EdgeDetection_%s//EdgeDetection_%s_%s_%s' %(info['participant'], thisStair.extraInfo['condition'], info['participant'], info['dateStr'])
    thisStair.saveAsPickle(fName)
    thisStair.saveAsExcel(fileName=fName, sheetName='RawData', matrixOnly=False, appendFile=True)
   
if DEBUG==False:
    myWin.bits.setContrast(1.0, LUTrange=1.0)
    fixation.draw()
    myWin.flip()

core.quit()