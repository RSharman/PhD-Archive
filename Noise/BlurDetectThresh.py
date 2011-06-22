#Find the blur detection thresholds for synthetic edges - May 2011

from psychopy import visual, event, monitors, data, sound, gui, core, misc, filters
import numpy as np
import time, os, random

DEBUG=True

try:
    info=misc.fromFile('lastParams.pickle')
except:
    info = {'Participant' : 'RJS',
                'Channel' : 'Lum', #Will accept 'Lum', 'LM', or 'S'
                'Noise Size' : 0.1,
                'Noise Contrast' : 0.2}
info['dateStr']=time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Synthetic Edge Blur Detection Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', info)
else:
    core.quit()
   
#Staircase Information
info['nTrials'] = 1
info['nReversals'] = 1
info['stepSizes'] = [0.125, 0.125, 0.06, 0.06, 0.03, 0.03, 0.015, 0.015, 0.005, 0.005]
info['minVal'] = 0
info['maxVal'] = 0.5
info['startVal'] = 0.3
info['nUp'] = 1
info['nDown'] = 3

#Clocks and Sounds
trialClock = core.Clock()
tick = sound.Sound('A', octave=6, secs=0.01); tick.setVolume(0.3)

if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
        fullscr=False, allowGUI=True, bitsMode=None)
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = None
    from psychopy import colorFunctions
    
if DEBUG==False:
    myWin = visual.Window(size=(1024, 768), monitor = 'heron', units = 'deg',
        fullscr=True, allowGUI=False, bitsMode = 'Fast')
    myMon=monitors.Monitor('heron')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
    import colorFunctions
   
#Basic Settings
info['displayT'] = 1
info['ISI'] = 0.3
fixation = visual.PatchStim(myWin, size=0.1, tex=None, mask='circle', rgb=-1)

#Function to Create Filtered White Noise
def makeFilteredNoise(res, radius, shape='gauss'):
    noise = np.random.random([res, res])
    kernel = filters.makeMask(res, shape='gauss', radius=radius)
    filteredNoise = filters.conv2d(kernel, noise)
    filteredNoise = ((filteredNoise-filteredNoise.min())/(filteredNoise.max()-filteredNoise.min())*2-1)
    return filteredNoise
    
#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['1', '2']:
            if (key in ['1']) and order==1:
                return 1 #subject perceives the first stim as more blurred
            if (key in ['2']) and order==1:
                return 0 #subject perceives the second stim as more blurred
            if (key in ['1']) and order==2:
                return 0
            if (key in ['2']) and order==2:
                return 1
            else:
                print "hit 1 or 2 (or q) (you hit %s)" %key
                return None

#The Staircase
#Set Up 
stairs = data.StairHandler(startVal=info['startVal'], 
                                                    nReversals=1,
                                                    stepSizes=info['stepSizes'],
                                                    stepType='lin', 
                                                    nTrials=info['nTrials'],
                                                    nUp=info['nUp'],
                                                    nDown=info['nDown'],
                                                    extraInfo=info,
                                                    minVal=info['minVal'],
                                                    maxVal=info['maxVal']
                                                    )

#Start Message
startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="Please press 1 or 2 to indicate whether the first or second image is blurred. Press any key when you are ready to continue.", )
                                                                                        
startMessage.draw()
myWin.flip()
junk = event.waitKeys()

#For Loop to Run Through the Trials
for thisBlur in stairs:
    trialClock.reset()
   
    print thisBlur
    
    #Jitter position of edges
    info['targetEdgePos'] = float(random.randrange(20, 80, 1))/float(100)
    info['foilEdgePos'] = float(random.randrange(20, 80, 1))/float(100)
    
    order = random.randint(1.0, 2.0)
    print 'order', order
    #Create stimuli
   
    blurLum = colorFunctions.makeEdgeGauss(width=thisBlur, center=info['targetEdgePos'])*0.3
    blurLm = colorFunctions.makeEdgeGauss(width=thisBlur, center=info['targetEdgePos'])*0.3
    blurS = colorFunctions.makeEdgeGauss(width=thisBlur, center=info['targetEdgePos'])*0.3

    sharpLum = colorFunctions.makeEdgeGauss(width=0, center=info['foilEdgePos'])*0.3
    sharpLm =colorFunctions.makeEdgeGauss(width=0, center=info['foilEdgePos'])*0.3
    sharpS =colorFunctions.makeEdgeGauss(width=0, center=info['foilEdgePos'])*0.3
    
    #Add channel specific noise
    noise1 = makeFilteredNoise(res=512, radius=info['Noise Size'])*info['Noise Contrast']
    blurLum += noise1
    blurLm += noise1
    blurS += noise1
    noise2 = makeFilteredNoise(res=512, radius=info['Noise Size'])*info['Noise Contrast']
    sharpLum += noise2
    sharpLm += noise2
    sharpS += noise2
    
    #Convert back to RGB
    blurLumEdge = colorFunctions.dklCartToRGB_2d(LUM=blurLum, LM=blurLm*0, S=blurS*0, conversionMatrix = conversionMatrix)
    blurLmEdge = colorFunctions.dklCartToRGB_2d(LUM=blurLum*0, LM=blurLm, S=blurS*0, conversionMatrix = conversionMatrix)
    blurSEdge = colorFunctions.dklCartToRGB_2d(LUM=blurLum*0, LM=blurLm*0, S=blurS, conversionMatrix = conversionMatrix)

    sharpLumEdge = colorFunctions.dklCartToRGB_2d(LUM=sharpLum, LM=sharpLm*0, S=sharpS*0, conversionMatrix = conversionMatrix)
    sharpLmEdge = colorFunctions.dklCartToRGB_2d(LUM=sharpLum*0, LM=sharpLm, S=sharpS*0, conversionMatrix = conversionMatrix)
    sharpSEdge = colorFunctions.dklCartToRGB_2d(LUM=sharpLum*0, LM=sharpLm*0, S=sharpS, conversionMatrix = conversionMatrix)


    

    #Draw Stimuli
    if info['Channel']=='Lum':
        imgFirst = visual.PatchStim(myWin, tex=blurLumEdge, units='deg', sf=(1/10.0), size=10.0, interpolate=True)
        imgSecond = visual.PatchStim(myWin, tex=sharpLumEdge, units='deg', sf=(1/10.0), size=10.0, interpolate=True)
    
    if info['Channel']=='LM':
        imgFirst = visual.PatchStim(myWin, tex=blurLmEdge, units='deg', sf=(1/10.0), size=10.0, interpolate=True)
        imgSecond = visual.PatchStim(myWin, tex=sharpLmEdge, units='deg', sf=(1/10.0), size=10.0, interpolate=True)
    
    if info['Channel']=='S':
        imgFirst = visual.PatchStim(myWin, tex=blurSEdge, units='deg', sf=(1/10.0), size=10.0, interpolate=True)
        imgSecond = visual.PatchStim(myWin, tex=sharpSEdge, units='deg', sf=(1/10.0), size=10.0, interpolate=True)
       
    if order==1:
        imgFirst.draw()
    if order==2:
        imgSecond.draw()
    myWin.flip()
    core.wait(info['displayT'])
    
    fixation.draw()
    myWin.flip()
    core.wait(info['ISI'])
   
    if order==1:
        imgSecond.draw()
    if order==2:
        imgFirst.draw()
    myWin.flip()
    core.wait(info['displayT'])
    
    if DEBUG==False: #Play a sound to indicate response is required
        tick.play()
       
    fixation.draw()
    myWin.flip()
   
    #Take Participant Response
    thisResp = None
    while thisResp==None:
        keys = event.waitKeys()
        thisResp = checkCorrect(keys)
         
    stairs.addData(thisResp)

#Save stairs
if info['Noise Contrast'] !=0:
    noiseInfo = ('NContrast%.2f_NSize%.2f_' %(info['Noise Contrast'], info['Noise Size']))
else:
    noiseInfo = ''
   
if not os.path.isdir('SynthBlurDetect_%s' %info['Participant']):
    os.mkdir('SynthBlurDetect_%s' %info['Participant'])
fName = 'SynthBlurDetect_%s//SynthBlurDetect_%s%s_%s_%s' %(info['Participant'], noiseInfo, info['Channel'], info['dateStr'], info['Participant'])
stairs.saveAsPickle(fName)
stairs.saveAsExcel(fileName=fName, sheetName='Raw Data', matrixOnly=False, appendFile=True)
