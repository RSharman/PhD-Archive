#dkl spherical - dkl cart - rgb test: July 2012

from psychopy import visual, misc, core, event, monitors
import colorFunctions
import numpy as np

DEBUG=True

if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
        fullscr=False, allowGUI=True, bitsMode=None)
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = None
    
info = {}
info['Blur'] = 0.01
edgeSize = 10.0
edgeSF = 1/10.0
edgePos = 0.5
   
lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5, size=512)
lmlms= colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5, size=512)
slms= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(0.5), size=512)
lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(0.5), size=512)
s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(0.5), size=512)

Edge= misc.dklCart2rgb(LUM=lum, LM=lm, S=s, conversionMatrix = conversionMatrix)/2.0
if (np.max(Edge)>1.0) or (np.min(Edge)<-1.0):
    print 'contrast outside range'
    core.quit()
lum1 = visual.PatchStim(myWin, tex = Edge, size=edgeSize, units = 'deg', sf=edgeSF, pos=(edgePos, 0.0))
lum1.draw()

myWin.flip()
event.waitKeys()

