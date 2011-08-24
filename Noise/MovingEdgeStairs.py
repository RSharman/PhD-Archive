#Create edge stimuli with staircased gap, noise and blur - April 2011

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

DEBUG=False

#Create a dialog box for settings and participant information
try:
    info=misc.fromFile('lastParams.pickle')
except:
    info = {'participant' : 'RJS',
                'Channel' : 'LM',
                'Blur' : 0.1,
                'Gap' : 0,
                'Noise Size' : 0.1,
                'Noise Contrast' : 0.2,
                'Edge Contrast' : 0.3}
info['dateStr']=time.strftime("%b%d_%H%M", time.localtime())
dlg = gui.DlgFromDict(info, title='Synthetic Edge Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', info)
else:
    core.quit()

#Staircase Information
info['nTrials'] = 50
info['nReversals'] = 1
info['stepSizes'] = [0.09888, 0.09888, 0.02472, 0.00618, 0.001545]#[0.25,0.125,0.125,0.06,0.06,0.03,0.03,0.015,0.015, 0.0075] 
#[0.25,0.25,0.125,0.125,0.06,0.06,0.03,0.03,0.015,0.015]
info['minVal'] = 0.2
info['maxVal'] = 0.8
info['startVal'] = 0.5
info['nUp'] = 1
info['nDown'] = 1

#Clocks and Sounds
trialClock = core.Clock()
tick = sound.Sound('A', octave=6, secs=0.01); tick.setVolume(0.3)

if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
        fullscr=False, allowGUI=True, bitsMode=None)
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = None
    import colorFunctions
    
if DEBUG==False:
    myWin = visual.Window(size=(1024, 768), monitor = 'hawk', units = 'deg',
        fullscr=True, allowGUI=False, bitsMode = None)
    myMon=monitors.Monitor('hawk')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
    import colorFunctions

#Basic Settings
info['displayT'] = 0.3

#Function to Create Filtered White Noise
#def makeFilteredNoise(res, radius, shape='gauss'):
#    noise = np.random.random([res, res])
#    kernel = filters.makeMask(res, shape='gauss', radius=radius)
#    filteredNoise = filters.conv2d(kernel, noise)
#    filteredNoise = ((filteredNoise-filteredNoise.min())/(filteredNoise.max()-filteredNoise.min())*2-1)
#    return filteredNoise

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

if info['Edge Contrast'] + info['Noise Contrast'] >1.0:
    print 'Edge Contrast + Noise Contrast > 1.0, please reduce one of these values'
    core.quit()

#noise=[]
#for n in range(100):
#    temp = makeFilteredNoise(512, radius=info['Noise Size'])
#    noise.append(temp)

pkl_file = open('noise02.pickle', 'rb')
noise = cPickle.load(pkl_file)

#Start Message
startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                                        text="Please press left or right to indicate whether the line appears to the left or the right of the edge. Press any key when you are ready to continue.", )
                                                                                        
startMessage.draw()
myWin.flip()
junk = event.waitKeys()

#Jitter position of edges
info['markerPos'] = float(random.randrange(-30, 30, 1))/10
print 'marker', info['markerPos']

#For Loop to Run Through the Trials
for thisDistance in stairs:
    trialClock.reset()
    
    print thisDistance
    info['lumEdgePos'] = (thisDistance)

    #Create stimuli
    lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=info['lumEdgePos'])*info['Edge Contrast']
    lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(info['lumEdgePos']+info['Gap']))*info['Edge Contrast']
    s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(info['lumEdgePos']+info['Gap']))*info['Edge Contrast']
    tex= colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm, S=s)
    
    noise1 = (noise[random.randrange(0,99,1)])*info['Noise Contrast']
    lum += noise1
    noise2 = noise[random.randrange(0,99,1)]*info['Noise Contrast']
    lm += noise2
    noise3 = noise[random.randrange(0,99,1)]*info['Noise Contrast']
    s += noise3

    #Draw stimuli
    if info['Channel']== 'Lum':
        lumEdge= colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s*0, conversionMatrix = conversionMatrix)
        if (np.max(lumEdge)>1.0) or (np.min(lumEdge)<-1.0):
            print 'contrast outside range'
            core.quit()
        lum1 = visual.PatchStim(myWin, tex = lumEdge, size = 10.0, units = 'deg', sf=(1/10.0))
        lum1.draw()
    if info['Channel']=='LM':
        rgEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s*0, conversionMatrix = conversionMatrix)
        print np.max(rgEdge), np.min(rgEdge)
        if (np.max(rgEdge)>1.0) or (np.min(rgEdge)<-1.0):
            print 'contrast outside range'
            core.quit()
        rg1 = visual.PatchStim(myWin, tex = rgEdge, size = 10.0, units = 'deg', sf=(1/10.0))
        rg1.draw()
    if info['Channel']=='S':
        sEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm*0, S=s, conversionMatrix = conversionMatrix)
        if (np.max(sEdge)>1.0) or (np.min(sEdge)<-1.0):
            print 'contrast outside range'
            core.quit()
        s1 = visual.PatchStim(myWin, tex=sEdge, size=10.0, units='deg', sf=(1/10.0))
        s1.draw()
    if info['Channel']=='LMLum':
        combEdge = colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm, S=s*0, conversionMatrix = conversionMatrix)
        if (np.max(combEdge)>1.0) or (np.min(combEdge)<-1.0):
            print 'contrast outside range'
            core.quit()
        combo = visual.PatchStim(myWin, tex = combEdge, size = 10.0, units = 'deg', sf=(1/10.0))
        combo.draw()
    if info['Channel']=='SLum':
        sCombEdge = colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s, conversionMatrix = conversionMatrix)
        if (np.max(sCombEdge)>1.0) or (np.min(sCombEdge)<-1.0):
            print 'contrast outside range'
            core.quit()
        scombo = visual.PatchStim(myWin, tex=sCombEdge, size = 10.0, units = 'deg', sf=(1/10.0))
        scombo.draw()
    if info['Channel']=='LMS':
        LMSEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s, conversionMatrix = conversionMatrix)
        if (np.max(LMSEdge)>1.0) or (np.min(LMSEdge)<-1.0):
            print 'contrast outside range'
            core.quit()
        LMSCombo = visual.PatchStim(MyWin, tex=LMSEdge, size = 10.0, units = 'deg', sf=(1/10))
        LMSCombo.draw()
    #Draw mask
    upperMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                            vertices=((-5,5), (5,5), (5,1), (-5,1)))
    lowerMask = visual.ShapeStim(myWin, units='deg', lineColor=(0,0,0), fillColor=(0,0,0), 
                            vertices=((-5,-5), (5,-5), (5,-1), (-5,-1)))
    upperMask.draw()
    lowerMask.draw()
    
    #Draw the marker
    marker = visual.ShapeStim(myWin, units = 'deg', lineWidth = 1.0, lineColor = 'black', fillColor = None,
                        pos=(info['markerPos'],-1), vertices = ((0, 0), (0, -1.0)), closeShape = False)
    marker.draw()

    myWin.flip()
    core.wait(info['displayT'])
    tick.play()
    
    myWin.flip()
    
     #Take Participant Response
    thisResp = None
    while thisResp == None:
        keys = event.waitKeys()
        thisResp = checkCorrect(keys)
    stairs.addData(thisResp)

    #myWin.getMovieFrame()
    #myWin.saveMovieFrames('test.jpg')

print 'position', info['markerPos']

#Save stairs
if not os.path.isdir('SynthMov_%s' %info['participant']):
    os.mkdir('SynthMov_%s' %info['participant'])
fName = 'SynthMov_%s//SynthMov_Gap%.2f_NoiseContrast%.2f_NoiseSize%.2f_EdgeContrast%.2f_Blur%.2f_%s_%s_%s' %(info['participant'], info['Gap'], info['Noise Contrast'], info['Noise Size'], info['Edge Contrast'], info['Blur'], info['dateStr'], info['Channel'], info['participant'])
stairs.saveAsPickle(fName)
stairs.saveAsExcel(fileName=fName, sheetName='Raw Data', matrixOnly=False, appendFile=True)
