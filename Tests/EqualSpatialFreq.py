#Creation of equal spacial frequency stimuli - April 2011

from psychopy import visual, core, event
import colorFunctions, Image, copy
from scipy import ndimage
import numpy as np

myWin = visual.Window(monitor = 'testMonitor')

pictures = ["horzlines.png", "vertlines.png"]

picture = np.array(Image.open("horzlines.jpg"))/127.5-1

dklPicture = colorFunctions.rgb2dklCart(picture, conversionMatrix=None)
dklPicture = np.array(dklPicture)

dklPicture2 = copy.copy(dklPicture)
dklPicture2 = np.rot90(dklPicture2)


#picture2 = np.array(Image.open("vertlines.jpg"))/127.5-1
#dklPicture2 = colorFunctions.rgb2dklCart(picture2, conversionMatrix=None)
#dklPicture2 = np.array(dklPicture2)

#lum = copy.copy(dklPicture[:,:,0])*(0.029*10)
lum = copy.copy(dklPicture[:,:,0])
lm = copy.copy(dklPicture[:,:,1])*0
s = copy.copy(dklPicture[:,:,2])*0

lum2 = copy.copy(dklPicture2[:,:,0])*0
#put the information in lm instead of lum
#lm2 = copy.copy(dklPicture2[:,:,0])*(0.074*10)
lm2 = copy.copy(dklPicture2[:,:,0])
s2 = copy.copy(dklPicture2[:,:,2])*0

lum = lum+lum2
lm = lm+lm2
s = s+s2

rgbPictureFirst = colorFunctions.dklCartToRGB_2d(lum, lm, s)
rgbPictureFirst /=2

grating = visual.PatchStim(myWin, tex = rgbPictureFirst, units='deg', sf=(1/20.0), size=20.0)

grating.draw()


SpatialFrequency = 1.0
alignment = 90

#colourGrating1 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0,10.0), pos = (0, 0), sf = SpatialFrequency, units = 'deg', 
#                            color = (0,45,1.0), colorSpace = 'dkl', opacity = 0.5)
#colourGrating2 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0,5.0), pos= (0, -2.5), sf = SpatialFrequency, units = 'deg', 
#                            color = (0,45,1.0), colorSpace = 'dkl', opacity = 0.25)
#lumGrating1 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0,10.0), pos=(0,0), sf = SpatialFrequency, units = 'deg', 
#                            color = (-90, 0, 1), opacity = 0.5, colorSpace = 'dkl', ori = alignment)
#lumGrating2 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0, 5.0), pos=(-2.5,0), sf = SpatialFrequency, units = 'deg', 
#                            color = (-90, 0, 1), opacity = 0.25, colorSpace = 'dkl', ori = alignment)
#
#
#redPatch = visual.PatchStim(myWin, tex = None, size = (10.0, 5.0), pos = (0.5, 2.5), units = 'deg', color = (0, 0, 1.0), colorSpace='dkl')
#greenPatch = visual.PatchStim(myWin, tex=None, size = (10.0, 5.0), pos = (0.5, -2.0), units = 'deg', color = (0,0,-1.0), colorSpace = 'dkl')
#
#darkPatch = visual.PatchStim(myWin, tex=None, size = (5.0, 10.0), pos = (-2.0, 0.0), units = 'deg', color = (1.0,0,0), colorSpace = 'dkl', opacity = 0.5)
#
#redPatch.draw()
#greenPatch.draw()
#darkPatch.draw()
#myWin.flip()
#
#lumGrating1.draw()
#colourGrating1.draw()

#colourGrating2.draw()
#lumGrating2.draw()
myWin.flip()

myWin.getMovieFrame()
myWin.saveMovieFrames('EqualOrthLum100.tif') 

junk =event.waitKeys()