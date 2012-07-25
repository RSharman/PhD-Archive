#dkl spherical - dkl cart - rgb test: July 2012

from psychopy import visual, misc, core, event, monitors, logging
import colorFunctions, copy
import numpy

DEBUG=True

if DEBUG==True:
    
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
        fullscr=False, allowGUI=True, bitsMode=None)
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = numpy.asarray([ \
        #LUMIN    %L-M    %L+M-S  (note that dkl has to be in cartesian coords first!)
        [1.0000, 1.0000, -0.1462],#R
        [1.0000, -0.3900, 0.2094],#G
        [1.0000, 0.0180, -1.0000]])#B
    
info = {}
info['Blur'] = 0.1
edgeSize = 10.0
edgeSF = 1/10.0
edgePos = 0.5
   
lum = colorFunctions.makeEdgeGauss(width=info['Blur'],center=0.5, size=512)
lm= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(0.5), size=512)*0.0
s= colorFunctions.makeEdgeGauss(width=info['Blur'],center=(0.5), size=512)

sphEdge = misc.cart2sph(z = lum, y = s, x = lm)

print len(sphEdge.shape)


#print sphEdge[:,:,0][0]

temp = copy.copy(sphEdge[:,:,1])+1
temp = (temp/numpy.abs(temp))*-15.0
sphEdge[:,:,0] += temp

#print sphEdge[:,:,0][0]

cartEdge = misc.dklCart2rgb(lum, lm, s)/2.0

Edge= misc.dkl2rgb(sphEdge, conversionMatrix = None)/2.0

lum1 = visual.PatchStim(myWin, tex = Edge, size=edgeSize, units = 'deg', sf=edgeSF, pos=(0.0, 0.0))
lum1.draw()

myWin.flip()
event.waitKeys()

