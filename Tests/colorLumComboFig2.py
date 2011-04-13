from psychopy import visual, event, log, misc, colors, filters
import numpy as np
#win = visual.Window([512,100], monitor='testMonitor')
import pylab, random, copy
import matplotlib.image as mpimg


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
lum = makeEdgeGauss(width=0.05,center=0.5)*0.1
lm= makeEdgeGauss(width=0.1,center=0.55)*0.3
#lum = makeEdgeMatrix(width=0.04,center=0.56)*0.1
#lm= makeEdgeMatrix(width=0.04,center=0.50)*0.3
s=makeEdgeGauss(width=0.2,center=0.5)*0.0
tex=dklCartToRGB_2d(LUM=lum, LM=lm, S=s)

noise=[]
for n in range(256):
    temp = random.random()
    noise.append(temp)

noise = np.array(noise)
noise = noise.reshape(16,16)

noise1 = copy.copy(noise)
noise2 = np.resize(noise, (512, 512))

#
#noise2 = noise1.resize((512,512), interpolation = 'bicubic')
#noise2 = np.array(noise2)


lumEdge=dklCartToRGB_2d(LUM=lum, LM=lm*0, S=s*0)
rgEdge = dklCartToRGB_2d(LUM=lum*0, LM=lm, S=s*0)
combEdge = dklCartToRGB_2d(LUM=lum, LM=lm, S=s*0)



subplots=True
if subplots: 
    fig = pylab.figure(figsize=[6,9])
    pylab.subplot(311)
    pylab.imshow(rgEdge/2.0+0.5)
    pylab.axis('off')
    pylab.subplot(312)
    pylab.imshow(combEdge/2.0+0.5)
    pylab.axis('off')
    pylab.subplot(313)
    pylab.imshow(lumEdge/2.0+0.5, alpha = 1.0)
    pylab.imshow(noise2, alpha = 0.5, cmap='gray')
    pylab.axis('off')
    pylab.show()
else:
    pylab.figure(figsize=[2,1])
    pylab.imshow(rgEdge[0:200,:]/2.0+0.5)
    pylab.text(5,55, '(A) Chromatic', color='w')#('Chromatic boundary only')
    pylab.axis('off')
    pylab.savefig('pics/edgeRG.png', dpi=400)
    pylab.figure(figsize=[2,1])
    pylab.imshow(combEdge[0:200,:]/2.0+0.5)
    pylab.text(5,55, '(B) Combined', color='w')
    pylab.axis('off')
    pylab.savefig('pics/edgeComb.png', dpi=400)
    pylab.figure(figsize=[2,1])
    pylab.imshow(lumEdge[0:200,:]/2.0+0.5)
    pylab.text(5,55, '(C) Luminance', color='w')#('Chromatic boundary only')
    pylab.axis('off')
    pylab.savefig('pics/edgeLum.png', dpi=400)
