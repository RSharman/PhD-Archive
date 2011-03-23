# 2D Fast Fourier Transform on the lum, lm and s components of natural scenes - March 2011

from psychopy import colorFunctions, core, visual, event
from scipy import fftpack
import scipy, Image, copy, pylab
import numpy as np

picture = np.array(Image.open("WhiteDot.jpg").transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

dklPicture = colorFunctions.rgb2dklCart(picture, conversionMatrix=None)
dklPicture = np.array(dklPicture)

lum = copy.copy(dklPicture[:,:,0])
lm = copy.copy(dklPicture[:,:,1])
s = copy.copy(dklPicture[:,:,2])

fftLum = fftpack.fft2(lum)
fftLm = fftpack.fft2(lm)
fftS = fftpack.fft2(s)

n = lum.size
timestep = 0.1
fftLum = fftpack.fftfreq(n, d=timestep)
fftLum = np.array(fftLum)

#fftLum = np.reshape(fftLum(512,512))

#print fftLum
print fftLum.shape

#fftLum = np.reshape(fftLum, -1)

#magnitudeLum = []
#counter = 0
#for n in fftLum:
#    mag1 = np.sqrt((fftLum[counter])*(fftLum[counter]))
#    counter += 1
#    if counter>262143:
#        counter -=1
#    mag2 = np.sqrt((fftLum[counter])*(fftLum[counter]))
#    mag = mag1+mag2
#    magnitudeLum.append(mag)

#print counter
#magnitudeLum = np.array(magnitudeLum)
#print magnitudeLum.shape
#
#magnitudeLum = np.reshape(fftLum, (512,512))

#print magnitudeLum
    


myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs',
                fullscr=False, allowGUI=True)

img = visual.PatchStim(myWin, tex=fftLum, sf=(1/10.0), size=20.0)
img.draw()
myWin.flip()

junk = event.waitKeys()

