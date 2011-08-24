#Testing Gauss Smooth - July 2011

#def GaussSmooth(matrix, width, center, size):
#    """put an image/matrix through a Gaussian smoothing filter
#   
#    params:
#        matrix: array to be smoothed
#        width: (float) the sd of the gauss used to smooth as a fraction of the matrix size
#        center: (float) the location of the center of the ramp as a fraction of the total matrix
#        size: (int=256) width and height of the matrix
#            """
#        centerLocation = int(size+center*size)
#        matrix
       
from psychopy import visual, filters, event
import Image, scipy
import numpy as np
from scipy.signal import convolve2d

width = 0.5
picture = np.array(Image.open('Leaf512.jpg').transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

gauss = filters.makeGauss(picture, mean=0, sd=width)/np.sqrt(2*np.pi*width**2)
smth = scipy.signal.convolve2d(picture, gauss, 'same')


myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', 
        fullscr=False, allowGUI=True)

img = visual.PatchStim(myWin, tex=smth, units='deg', sf=(1/10.0), size=10.0)
img.draw()
myWin.flip()
event.waitKeys()