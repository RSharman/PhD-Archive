#Rotating either colour or luminance component so they are no longer aligned - Apr 2012

from psychopy import visual, misc, event
import numpy as np
from scipy import ndimage
import Image, copy

myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', fullscr=False, allowGUI=True)

file = "Pumpkin512.jpg"

picture = np.array(Image.open(file).transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

dklPicture = misc.rgb2dklCart(picture)
dklPicture = np.array(dklPicture)

lum = copy.copy(dklPicture[:,:,0])
lm = copy.copy(dklPicture[:,:,1])
s = copy.copy(dklPicture[:,:,2])

#lum = np.rot90(lum)

#Do blurring here
lum = ndimage.gaussian_filter(lum, sigma=5.0)
#lm = ndimage.gaussian_filter(lm, sigma=5.0)
#s = ndimage.gaussian_filter(s, sigma=5.0)

#Reversing the channels
rgbPicture = misc.dklCart2rgb((lm+s)/2, lum, lum)

#rgbPicture = misc.dklCart2rgb(lum, lm, s)
rgbPicture = rgbPicture/3

print np.min(rgbPicture), np.max(rgbPicture)

img = visual.PatchStim(myWin, tex=rgbPicture, units='deg', sf=(1/10.0), size=10.0)
img.draw()
myWin.flip()

myWin.getMovieFrame()
myWin.saveMovieFrames('RevPumpkin5degBlurChrom.jpg')

event.waitKeys()