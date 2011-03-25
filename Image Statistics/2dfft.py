# 2D Fast Fourier Transform on the lum, lm and s components of natural scenes - March 2011

from psychopy import colorFunctions, core, visual, event
from scipy import fftpack
import scipy, Image, copy, pylab
import numpy as np
import radialProfile

picture = np.array(Image.open("Pansy512.jpg").transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

dklPicture = colorFunctions.rgb2dklCart(picture, conversionMatrix=None)
dklPicture = np.array(dklPicture)

lum = copy.copy(dklPicture[:,:,0])
lm = copy.copy(dklPicture[:,:,1])
s = copy.copy(dklPicture[:,:,2])

fftLum = fftpack.fft2(lum)
fftLm = fftpack.fft2(lm)
fftS = fftpack.fft2(s)

#fftLumAmp = fftLum.real
#fftLumPhase = fftLum.imag

F2 = fftpack.fftshift(fftLum)

#Not sure why this is squared www.astrobetter.com/fourier-transforms-of-images-in-python/
#Or why a log is take before plotting, from the same source
pylab.figure(1)
pylab.clf()
F3 = abs(F2)**2
pylab.imshow(np.log10(F3))

#Calculating the azimuthally average 1D power spectrum
A1 = radialProfile.azimuthalAverage(F3)
pylab.figure(2)
pylab.clf()
pylab.semilogy(A1)
pylab.xlabel('Spatial Frequency')
pylab.ylabel('Power Spectrum')




#fftLumMag = abs(fftLum)**2
#
#fftLumMag = abs(fftpack.fftshift(fftLumMag))
#fftLumMagNew = abs(fftpack.fftshift(fftpack.fft2(fftLumMag)))
#
#pylab.imshow(fftLumMag)
#
#
#pylab.imshow(fftLumMagNew)
#pylab.imshow(picture)
#pylab.xlim(120,130)
#pylab.ylim(120,130)
#pylab.pink()
pylab.show()

#print fftLumMag[:,0]

#centre=[]
#centre2=[]
#xrange = np.arange(75, 437)
#for n in xrange:
#
#    centre.append(fftLumMag[:,n])
#    centre2.append(centre[n,:])
#
#print centre2.shape


#print np.min(fftLum)
#print np.max(fftLum)

#fftLum = (((fftLum +0.000850091991337)/259005.5678)*2)-1

#fftLum = np.reshape(fftLum(512,512))

#print fftLumMag

#pylab.plot(fftLumMag)
#pylab.ylim(0, 1000)
#pylab.show()
#
#myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs',
#                fullscr=False, allowGUI=True)
#
#img = visual.PatchStim(myWin, tex=fftLumMag, sf=(1/20.0), size=20.0)
#img.draw()
#myWin.flip()
#
#junk = event.waitKeys()

