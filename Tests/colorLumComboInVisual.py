from psychopy import visual, event, log, misc, colors, filters, monitors
import numpy as np
#win = visual.Window([512,100], monitor='testMonitor')
import pylab, random, copy
import matplotlib.image as mpimg
from scipy import ndimage

DEBUG=True
nElements = 800
elementSize = 0.25
opacity = 0
gap = 0.01
blur = 0.01

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


def dkl2rgb2D(dkl_NxNx3, conversionMatrix):
    """convert a 2D (image) of DKL colours to RGB space"""
    origShape = dkl_NxNx3.shape#remember for later
    NxN = origShape[0]*origShape[1]#find nPixels
    dkl = np.reshape(dkl_NxNx3,[NxN,3])#make Nx3
    rgb = colors.dkl2rgb(dkl,conversionMatrix)#convert
#    print 'dkl',dkl
#    print 'rgb', rgb
#    print 'rgbReshape', np.reshape(rgb,origShape)[:,:,0]
    return np.reshape(rgb,origShape)#reshape and return
    
def dklCartToRGB_2d(LUM, LM, S, conversionMatrix=None):
    """Like dkl2rgb2D except that it uses cartesian coords (LM,S,LUM) rather than
    spherical coords for DKL (elev, azim, contr)
    """
    NxNx3=list(LUM.shape)
    NxNx3.append(3)
    dkl_cartesian = np.asarray([LUM.reshape([-1]), LM.reshape([-1]), S.reshape([-1])])
#    print 'rg,by,lum:', RG, BY, LUM
    if conversionMatrix==None:
        conversionMatrix = np.asarray([ \
            #LUMIN	%L-M	%L+M-S  (note that dkl has to be in cartesian coords first!)
            [1.0000, 1.0000, -0.1462],#R
            [1.0000, -0.3900, 0.2094],#G
            [1.0000, 0.0180, -1.0000]])#B
    rgb = np.dot(conversionMatrix, dkl_cartesian)
    return np.reshape(np.transpose(rgb), NxNx3)
    
def makeEdgeGauss(width, center, size=512):
    """Create a matrix of given size that switches from 0 to 1 using a gaussian profile
    
    :params:
            width: (float) the sd of the gauss used to smooth as a fraction of the matrix size
            center: (float) the location of the center of the ramp as a fraction of the total matrix
            size: (int=256) width and height of the matrix
            """
    edge = np.ones(size*3, float)#3x to achieve edge-padding
    centerLocation = int(size+center*size)
    edge[:centerLocation]=0
    gauss = filters.makeGauss(x=np.linspace(-1.0,1.0,size), mean=0, sd=width)/np.sqrt(2*np.pi*width**2)
    smthEdge = np.convolve(edge, gauss,'same')
    smthEdge = (smthEdge[size:size*2]-smthEdge.min())/(smthEdge.max()-smthEdge.min())#just take the middle section
    smthEdge.shape=(1,size)
    return np.tile(smthEdge,(size,1))*2-1

def makeEdgeMatrix(width, center, size=512):
    """Create a matrix of given size that switches from 0 to 1 using a linear ramp.
    
    :params:
            width: (float) the width of the linear ramp (blur) as fraction of the total matrix
            center: (float) the location of the center of the ramp as a fraction of the total matrix
            size: (int=256) width and height of the matrix
            """
    center=int(center*(size-1))
    width = int(width*size/2)*2
    mat = np.ones([size,size], 'f')
    mat[:,0:(center-width/2)]=0
    if (center-width/2)<0 or (center+width/2)>size:
        log.error('ramp extends beyond texture')
    mat[:,(center-width/2):(center+width/2)] = np.linspace(0,1.0,width)
    return mat*2.0-1

def gammaCorrect(texture, gamma=2.2):
    return (((texture+1)/2.0)**(1.0/gamma))*2-1
    


#these work OK
lum = makeEdgeGauss(width=blur,center=0.5)*0.1
lm= makeEdgeGauss(width=blur,center=(0.5+gap))*0.3
#lum = makeEdgeMatrix(width=0.04,center=0.56)*0.1
#lm= makeEdgeMatrix(width=0.04,center=0.50)*0.3
s=makeEdgeGauss(width=0.2,center=0.5)*0.0
tex=dklCartToRGB_2d(LUM=lum, LM=lm, S=s)

lumEdge=dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s*0, conversionMatrix = conversionMatrix)
rgEdge = dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s*0, conversionMatrix = conversionMatrix)
combEdge = dklCartToRGB_2d(LUM=lum, LM=lm, S=s*0, conversionMatrix = conversionMatrix)

ori = []
for n in range(nElements):
    temp = random.randint(0,360)
    ori.append(temp)



myWin = visual.Window(size = (800,600), monitor = monitor, bitsMode = bitsMode)
noise1 = visual.ElementArrayStim(myWin, units = 'deg', fieldSize = (10.0,10.0), fieldShape = 'sqr', opacities = opacity, nElements = nElements,
                elementTex=lumEdge, elementMask='None', sizes = elementSize)
noise1.setOris(ori)

noise2 = visual.ElementArrayStim(myWin, units = 'deg', fieldSize = (10.0,10.0), fieldShape = 'sqr', opacities = opacity, nElements = nElements,
                elementTex=rgEdge, elementMask='None', sizes = elementSize)
noise2.setOris(ori)

combo = visual.PatchStim(myWin, tex = combEdge, size = 10.0, units = 'deg', sf=(1/10.0))

#lum5 = visual.PatchStim(myWin, tex = lumEdge, size = 10.0, units = 'deg', sf=(1/10.0))
#rg4 = visual.PatchStim(myWin, tex = rgEdge, size = 10.0, units = 'deg', sf=(1/10.0))
#
#lum5.draw()
#rg4.draw()

combo.draw()
noise1.draw()
noise2.draw()
myWin.flip()

#myWin.getMovieFrame()
#myWin.saveMovieFrames('test.jpg')

junk = event.waitKeys()
