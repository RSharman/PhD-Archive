#Create edge stimuli with controlled gap, noise and blur - April 2011

from psychopy import visual, event, filters, monitors
import numpy as np
import random
import colorFunctions

DEBUG=True

#Settings
blur = 0.075
gap = 0.06
noiseSize = 0.5
noiseContrast = 0


if DEBUG==True:
    monitor = 'testMonitor'
    bitsMode = None
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = None
    
if DEBUG==False:
    monitor = 'heron'
    bitsMode = 'Fast'
    myMon=monitors.Monitor('heron')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
   
def makeFilteredNoise(res, radius, shape='gauss'):
    noise = np.random.random([res, res])
    kernel = filters.makeMask(res, shape='gauss', radius=radius)
    filteredNoise = filters.conv2d(kernel, noise)
    filteredNoise = ((filteredNoise-filteredNoise.min())/(filteredNoise.max()-filteredNoise.min())*2-1)
    return filteredNoise
   
#Create stimuli
lum = colorFunctions.makeEdgeGauss(width=blur,center=0.5)*0.3
lm= colorFunctions.makeEdgeGauss(width=blur,center=(0.5+gap))*0.3
s=colorFunctions.makeEdgeGauss(width=0.2,center=0.5)*0.0
tex= colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm, S=s)

noiseContrast = 1.0

noise1 = makeFilteredNoise(512, radius=noiseSize)*noiseContrast
lum += noise1
noise2 = makeFilteredNoise(res=512, radius=noiseSize)*noiseContrast
lm += noise2

lumEdge= colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s*0, conversionMatrix = conversionMatrix)
rgEdge = colorFunctions.dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s*0, conversionMatrix = conversionMatrix)
combEdge = colorFunctions.dklCartToRGB_2d(LUM=lum, LM=lm, S=s*0, conversionMatrix = conversionMatrix)

#Create window and draw stimuli
myWin = visual.Window(size = (800,600), monitor = monitor, bitsMode = bitsMode)

combo = visual.PatchStim(myWin, tex = combEdge, size = 10.0, units = 'deg', sf=(1/10.0))
lum1 = visual.PatchStim(myWin, tex = lumEdge, size = 10.0, units = 'deg', sf=(1/10.0))
rg1 = visual.PatchStim(myWin, tex = rgEdge, size = 10.0, units = 'deg', sf=(1/10.0))

#lum1.draw()
#rg1.draw()
combo.draw()

myWin.flip()

#myWin.getMovieFrame()
#myWin.saveMovieFrames('test.jpg')

junk = event.waitKeys()