#A library of various different functions related to colour

from psychopy import visual, event, log, misc, colors, filters
import numpy as np
import pylab, scipy, copy

def dkl2rgb2D(dkl_NxNx3, conversionMatrix):
    """convert a 2D (image) of Spherical DKL colours to RGB space"""
    origShape = dkl_NxNx3.shape#remember for later
    NxN = origShape[0]*origShape[1]#find nPixels
    dkl = np.reshape(dkl_NxNx3,[NxN,3])#make Nx3
    rgb = colors.dkl2rgb(dkl,conversionMatrix)#convert
    return np.reshape(rgb,origShape)#reshape and return
   
def dklCartToRGB_2d(LUM, LM, S, conversionMatrix=None):
    """Like dkl2rgb2D except that it uses cartesian coords (LM,S,LUM) rather than
    spherical coords for DKL (elev, azim, contr)
    NB: Due to the matrix multiplication, this may return rgb values >1 or <-1
    """
    NxNx3=list(LUM.shape)
    NxNx3.append(3)
    dkl_cartesian = np.asarray([LUM.reshape([-1]), LM.reshape([-1]), S.reshape([-1])])

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
         31/5/11: Added to option to create an edge with no blur for staircase procedures, etc. RJS

    :params:
            width: (float) the sd of the gauss used to smooth as a fraction of the matrix size
            center: (float) the location of the center of the ramp as a fraction of the total matrix
            size: (int=256) width and height of the matrix
            """
    if width==0:
        edge = np.ones(size*3, float)
        centerLocation = int(size+center*size)
        edge[:centerLocation]=0
        shpEdge = (edge[size:size*2]-edge.min())/(edge.max()-edge.min())
        shpEdge.shape = (1,size)
        return np.tile(shpEdge, (size,1))*2-1
    else:
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
   
def rgb2dklCart(picture, conversionMatrix=None):
    """convert an RGB image into Cartesian DKL space"""
    #Turn the picture into an array so we can do maths
    picture=scipy.array(picture)
    #Find the original dimensions of the picture
    origShape = picture.shape

    #this is the inversion of the dkl2rgb conversion matrix
    if conversionMatrix==None:
        conversionMatrix = np.asarray([\
            #LUMIN->%L-M->L+M-S
            [ 0.25145542,  0.64933633,  0.09920825],
            [ 0.78737943, -0.55586618, -0.23151325],
            [ 0.26562825,  0.63933074, -0.90495899]])
    else:
        conversionMatrix = np.linalg.inv(conversionMatrix)

    #Reshape the picture so that it can multiplied by the conversion matrix
    red = picture[:,:,0]
    green = picture[:,:,1]
    blue = picture[:,:,2]

    dkl = np.asarray([red.reshape([-1]), green.reshape([-1]), blue.reshape([-1])])
    
    #Multiply the picture by the conversion matrix
    dkl=np.dot(conversionMatrix, dkl)

    #Reshape the picture so that it's back to it's original shape
    dklPicture = np.reshape(np.transpose(dkl), origShape)
    return dklPicture