# 2D Fast Fourier Transform on the lum, lm and s components of natural scenes - March 2011

from psychopy import colorFunctions, core, visual, event
from scipy import fftpack
import scipy, Image, copy, pylab
import numpy as np
import radialProfile, radial_data

OrigImage = "WhiteDot.jpg"
picture = np.array(Image.open(OrigImage).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1


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

F2Lum = fftpack.fftshift(fftLum)
F2Lm = fftpack.fftshift(fftLm)
F2S = fftpack.fftshift(fftS)

#Not sure why this is squared www.astrobetter.com/fourier-transforms-of-images-in-python/
#Or why a log is take before plotting, from the same source
F3Lum = abs(F2Lum)**2
F3Lm = abs(F2Lm)**2
F3S = abs(F2S)**2

#Plotting kspace
#pylab.figure(1)
#pylab.clf()
#pylab.imshow(np.log10(F3Lum))

#Calculating the azimuthally average 1D power spectrum using radialProfile
A1Lum = radialProfile.azimuthalAverage(F3Lum)
A1Lm = radialProfile.azimuthalAverage(F3Lm)
A1S = radialProfile.azimuthalAverage(F3S)

pylab.figure(2)
pylab.clf()
pylab.semilogy(A1Lum, label = 'Lum')
pylab.semilogy(A1Lm, label = 'Lm')
pylab.semilogy(A1S, label = 'S')
pylab.title(OrigImage)
pylab.legend()
pylab.xlim(0, 256)
pylab.xlabel('Spatial Frequency')
pylab.ylabel('Power Spectrum')

pylab.show()

LumMean = np.mean(A1Lum[127:])
LmMean = np.mean(A1Lm[127:])
SMean = np.mean(A1S[127:])
print LumMean
print LmMean
print SMean


