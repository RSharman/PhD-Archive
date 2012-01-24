#Practice set for reversed colour and luminance blur detection - Oct 2011

from psychopy import visual, event, misc, filters, core, sound, data, gui, monitors
import numpy as np
import copy, time, os, random
from numpy.random import shuffle
from scipy import ndimage
import Image

info={}
info['pictures'] = ["Pansy512.jpg", "Leaf512.jpg", "Pelican512.jpg", "Pumpkin512.jpg"]
info['ISI'] = 0.5
info['displayT'] = 0.3
info['baseBlur'] = 0

info['blurs'] = [18, 18, 17, 17, 16, 16, 15, 15, 14, 14, 13, 13]

stimList=[]
for n in info['blurs']:
    stimList.append({'blur' : n})

DEBUG=True
#Create window and fixation
if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', 
        fullscr=False, allowGUI=True)
    conversionMatrix = None
    myMon= monitors.Monitor('testMonitor')
if DEBUG==False:
    myWin = visual.Window(size=(1024, 768), monitor = 'Raven', units = 'degs',
        fullscr=True, allowGUI=False, bitsMode=None)
    myMon=monitors.Monitor('Raven')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
fixation = visual.PatchStim(myWin, size=0.1, tex=None, mask='circle', rgb=-1)
order = random.randint(1.0,2.0)

#Checking Responses
def checkCorrect (keys):
    for key in keys:
        if key in ['q', 'escape']:
            core.quit()
        elif key in ['1', '2']:
            if (key in ['1']) and order==1:
                return 1 #subject perceives the first image as more blurred
            if (key in ['2']) and order==1:
                return 0 #subject perceives the second image as more blurred
            if (key in ['1']) and order==2:
                return 0
            if (key in ['2']) and order==2:
                return 1
            else:
                print "hit 1 or 2 (or q) (you hit %s)" %key
                return None

startMessage = visual.TextStim(myWin, pos=(0.0,-4), height =1, rgb=-1,
                                                                    text="Please press 1 or 2 to indicate whether the first or second image appears more blurred. Press any key when you are ready to continue.", )
startMessage.draw()
myWin.flip()
junk = event.waitKeys()

extraInfo = []
for thisPicture in info['pictures']:
    picture=np.array(Image.open(thisPicture).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

    #Change the picture from RGB to DKL
    thisDklPicture = misc.rgb2dklCart(picture, conversionMatrix=conversionMatrix)
    thisDklPicture = np.array(thisDklPicture)
    extraInfo.append(thisDklPicture)

trials = data.TrialHandler(stimList, nReps=1, method='random')
trials.data.addDataType('choice')
trials.data.addDataType('picture')

nDone=0
counter=0
condition = [0,1,2,3,0,1,2,3,0,1,2,3]
shuffle(condition)
#condition = condition[0]

for thisTrial in trials:

    pic = random.randrange(0,4,1)
    dklPicture = extraInfo[pic]
    
    print 'counter', counter

    thisCondition = condition[counter]
    counter+=1
    print thisCondition
    if thisCondition ==0:
        #luminance only
        chromaticity=0
        luminance=1
        chromaticityBlur='n'
        luminanceBlur='y'
    if thisCondition ==1:
        #colour only
        chromaticity=1
        luminance=0
        chromaticityBlur='y'
        luminanceBlur='n'
    if thisCondition ==2:
        #luminance blur with colour
        chromaticity=1
        luminance=1
        chromaticityBlur='n'
        luminanceBlur='y'
    if thisCondition ==3:
        #colour blur with luminance
        chromaticity=1
        luminance=1
        chromaticityBlur='y'
        luminanceBlur='n'

    lum = copy.copy(dklPicture[:,:,0])*chromaticity
    lm = copy.copy(dklPicture[:,:,1])*luminance
    s = copy.copy(dklPicture[:,:,2])*luminance

    sigmaLumFirst=0
    sigmaLumSecond=0
    sigmaFirst=0
    sigmaSecond=0
    
    if luminanceBlur=='y':
        if order==1:
            sigmaFirst += thisTrial['blur']
        if order==2:
            sigmaSecond += thisTrial['blur']
    
    if chromaticityBlur=='y':
        if order==1:
            sigmaLumFirst += thisTrial['blur']
        if order==2:
            sigmaLumSecond += thisTrial['blur']

    #blur for first image
    lmFirst = ndimage.gaussian_filter(lm, sigma=sigmaFirst, order=0, output=None, mode='reflect', cval=0.0)
    sFirst = ndimage.gaussian_filter(s, sigma=sigmaFirst, order=0, output=None, mode='reflect', cval=0.0)
    lumFirst = ndimage.gaussian_filter(lum, sigma=sigmaLumFirst)
    #blur for second image
    lmSecond = ndimage.gaussian_filter(lm, sigma=sigmaSecond, order=0, output=None, mode='reflect', cval=0.0)
    sSecond = ndimage.gaussian_filter(s, sigma=sigmaSecond, order=0, output=None, mode='reflect', cval=0.0)
    lumSecond = ndimage.gaussian_filter(lum, sigma=sigmaLumSecond)
    
    #change back to RGB
    rgbPictureFirst = misc.dklCart2rgb((lmFirst+sFirst)/2, lumFirst, lumFirst, conversionMatrix)
    rgbPictureSecond = misc.dklCart2rgb((lmSecond+sSecond)/2, lumSecond, lumSecond, conversionMatrix)

    #Divide all the values by 2 so that there is room for the increases caused by the Gaussian filter
    rgbPictureFirst=rgbPictureFirst/2
    rgbPictureSecond=rgbPictureSecond/2

    #Draw the picture
    imgFirst = visual.PatchStim(myWin, tex=rgbPictureFirst, units='deg', sf=(1/10.0), size=10.0)
    imgFirst.draw()
    myWin.flip()
    core.wait(info['displayT'])
#        junk = event.waitKeys()
    
    fixation.draw()
    myWin.flip()
    core.wait(info['ISI'])
    
    imgSecond = visual.PatchStim(myWin, tex=rgbPictureSecond, units='deg', sf=(1/10.0), size=10.0)
    imgSecond.draw()
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

    print 'thisResp', thisResp

    if thisResp==0:
        myWin.flip()
        answer = visual.TextStim(myWin, pos = (0.0,0.0), height =4, units='deg', color='red', text='incorrect')
        answer.draw()
        myWin.flip()
        core.wait(1.0)
    
    if thisResp==1:
        myWin.flip()
        answer = visual.TextStim(myWin, pos = (0.0,0.0), height = 4, units='deg', color='green', text='correct')
        answer.draw()
        myWin.flip()
        core.wait(1.0)



