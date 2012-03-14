#Create edge stimuli with staircased gap, noise and blur - March 2012

#The details below are based on the stimulus being displayed at a size of 10 degrees.
# Channel can be: Lum, LM, S, LMCombo, SCombo
#Gap is fraction of the overall stimulus i.e. a gap of 0.1 would be 10% of the stimulus or 1 degree
#Blur width is also a fraction of the overall stimulus i.e. a blur of 0.1 would be 10% of the stimulus or 1 degree
#Marker position - the output from the staircase - is between 0 and 10 and is in degrees
#lumEdgePos - is a randomly generated number which positions the luminance edge, this is a fraction of the stim
#i.e. lumEdgePos = 0.2 the luminance edge will be 2 degrees from the left
#the LM edge is positioned relative to the luminance edge - i.e. lm edge position = lumEdgePos+Gap

from psychopy import visual, event, filters, monitors, data, sound, gui, misc, core
import numpy as np
import random, time, os, cPickle
from numpy.random import shuffle

DEBUG=True

#Create a dialog box for settings and participant information
try:
    info=misc.fromFile('lastParams.pickle')
except:
    info = {'participant' : 'RJS',
                'Gap' : 0,
                'Edge Contrast LM' : 0.1,
                'Edge Contrast S' : 0.1,
                'Edge Contrast Lum' : 0.1}
info['dateStr']=time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Synthetic Edge Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', info)
else:
    core.quit()

#Clocks and Sounds
trialClock = core.Clock()
tick = sound.Sound('A', octave=6, secs=0.01); tick.setVolume(0.3)

if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
        fullscr=False, allowGUI=True, bitsMode=None)
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = None
    edgeSize = 4.5#10.0
    edgeSF = 1/4.5#1.0/10.0
    import colorFunctions
    
if DEBUG==False:
    myWin = visual.Window(size=(1024, 768), monitor = 'heron', units = 'deg', screen=1,
        fullscr=True, allowGUI=False, bitsMode = 'fast')
    myMon=monitors.Monitor('heron')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
    edgeSize = 4.5
    edgeSF = 1.0/4.5
    import colorFunctions

#Basic Settings
info['Blur'] = 0.03
info['ISI'] = 0.3
myMouse = event.Mouse(win = myWin)
finalPositions={}
markerPositions={}

#Setting for Trial Handler
stimList = data.importConditions('MOAConds.xlsx')
trials = data.TrialHandler(stimList, 2)
trials.data.addDataType('LumEdge')
trials.data.addDataType('Marker')

#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['left', 'right']:
            if (key in ['left']):
                return 1 #subject perceives the line to be to the right
            if (key in ['right']):
                return 0 #subject perceives the line to be to the left
            else:
                print "hit left or right (or q) (you hit %s)" %key
                return None

Conds = ['Lum', 'LMLum', 'SLum']
# ['LM', 'S', 'Lum', 'LMLum', 'SLum', 'LMS']
shuffle(Conds)

print Conds

#for thisCond in Conds:
for thisTrial in trials:
    info['Channel']=thisTrial['condList']
    #Start Message
    startMessage = visual.TextStim(myWin, pos=(0.0,-0.6), height =0.3, colorSpace = 'rgb', color=-1, wrapWidth=4.0,
                                                                                            text="Please press click and hold the left mouse button the align the marker and edge, when you are happy right click to move onto the next trial. Press any key when you are ready to continue.", )
                                                                                            
    startMessage.draw()
    myWin.flip()
    junk = event.waitKeys()

    #Jitter position of edges
    info['markerPos'] = float(random.randrange(-10, 10, 1))/10
    print 'marker', info['markerPos']
    info['lumEdgePos'] = 0.5

#    Reset mouse and clock
    myMouse.clickReset()
    trialClock.reset()
    
    while True:
        for key in event.getKeys():
            if key in ['escape', 'q']:
                core.quit()

    #get mouse events
        mouse_dX, mouse_dY = myMouse.getRel()
        mouse1, mouse2, mouse3 = myMouse.getPressed()
        #if right click then quit
        if (mouse3):
            trials.data.add('Condition', info['Channel'])
            trials.data.add('LumEdge', finalPosition)
            trials.data.add('Marker', info['markerPos'])

            print 'tada', finalPosition
            break

        #Changing lumEdgePos with mousePos
        if (mouse1):
            info['lumEdgePos'] += mouse_dX/25
        
        #Create stimuli
        lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=info['lumEdgePos'])*info['Edge Contrast Lum']
        lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(info['lumEdgePos']+info['Gap']))*info['Edge Contrast LM']
        s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(info['lumEdgePos']+info['Gap']))*info['Edge Contrast S']
        tex= colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm, S=s)
        
        #Draw stimuli
        if info['Channel']== 'Lum':
            lumEdge= colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s*0, conversionMatrix = conversionMatrix)
            if (np.max(lumEdge)>1.0) or (np.min(lumEdge)<-1.0):
                print 'contrast outside range'
                core.quit()
            lum1 = visual.PatchStim(myWin, tex = lumEdge, size = edgeSize, units = 'deg', sf=(edgeSF))
            lum1.draw()
        if info['Channel']=='LM':
            rgEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s*0, conversionMatrix = conversionMatrix)
            print np.max(rgEdge), np.min(rgEdge)
            if (np.max(rgEdge)>1.0) or (np.min(rgEdge)<-1.0):
                print 'contrast outside range'
                core.quit()
            rg1 = visual.PatchStim(myWin, tex = rgEdge, size = edgeSize, units = 'deg', sf=(edgeSF))
            rg1.draw()
        if info['Channel']=='S':
            sEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm*0, S=s, conversionMatrix = conversionMatrix)
            if (np.max(sEdge)>1.0) or (np.min(sEdge)<-1.0):
                print 'contrast outside range'
                core.quit()
            s1 = visual.PatchStim(myWin, tex=sEdge, size=edgeSize, units='deg', sf=(edgeSF))
            s1.draw()
        if info['Channel']=='LMLum':
            combEdge = colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm, S=s*0, conversionMatrix = conversionMatrix)
            if (np.max(combEdge)>1.0) or (np.min(combEdge)<-1.0):
                print 'contrast outside range'
                core.quit()
            combo = visual.PatchStim(myWin, tex = combEdge, size = edgeSize, units = 'deg', sf=(edgeSF))
            combo.draw()
        if info['Channel']=='SLum':
            sCombEdge = colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s, conversionMatrix = conversionMatrix)
            if (np.max(sCombEdge)>1.0) or (np.min(sCombEdge)<-1.0):
                print 'contrast outside range'
                core.quit()
            scombo = visual.PatchStim(myWin, tex=sCombEdge, size = edgeSize, units = 'deg', sf=(edgeSF))
            scombo.draw()
        if info['Channel']=='LMS':
            LMSEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s, conversionMatrix = conversionMatrix)
            if (np.max(LMSEdge)>1.0) or (np.min(LMSEdge)<-1.0):
                print 'contrast outside range'
                core.quit()
            LMSCombo = visual.PatchStim(myWin, tex=LMSEdge, size=edgeSize, units='deg', sf=(edgeSF))
            LMSCombo.draw()
        #Draw mask
        upperMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                                vertices=((-5,5), (5,5), (5,0.5), (-5,0.5)))
        lowerMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                                vertices=((-5,-5), (5,-5), (5,-0.5), (-5,-0.5)))
        upperMask.draw()
        lowerMask.draw()
        
        #Draw the marker
        marker = visual.ShapeStim(myWin, units = 'deg', lineWidth = 1.0, lineColor = 'black', fillColor = None,
                            pos=(info['markerPos'],-0.5), vertices = ((0, 0), (0, -0.5)), closeShape = False)
        marker.draw()

        myWin.flip()
        #myWin.getMovieFrame()
        #myWin.saveMovieFrames('LMS.jpg')
        
         #Take Participant Response
        if (mouse1):
            finalPosition = info['lumEdgePos']
#            print 'lumEdge', finalPosition
#            print 'line up', ((info['markerPos']+1)/2)-finalPosition
#            print 'marker', info['markerPos']

#Save Data
if not os.path.isdir('MOA_%s' %info['participant']):
    os.mkdir('MOA_%s' %info['participant'])
fileName = 'MOA_%s//MOALong_Gap%.2f_EContrLM%.2f_EContrS%.2f_EContrS%.2f_%s_%s.pickle' %(info['participant'], info['Gap'],\
                    info['Edge Contrast LM'], info['Edge Contrast S'], info['Edge Contrast Lum'], info['dateStr'], info['participant']) 

trials.saveAsExcel(fileName=fileName, sheetName='rawData', stimOut = ['condList'], dataOut = ('n', 'all_mean', 'all_std', 'all_raw'))
trials.saveAsPickle(fileName=fileName)

core.quit()








