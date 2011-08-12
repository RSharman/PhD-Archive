#Creation of equal spacial frequency stimuli - April 2011

from psychopy import visual, core, event

myWin = visual.Window(size = (800,600), monitor = 'testMonitor')

SpatialFrequency = 1.0
alignment = 90

colourGrating1 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0,10.0), pos = (0, 0), sf = SpatialFrequency, units = 'deg', 
                            color = (0,45,1.0), colorSpace = 'dkl', opacity = 0.5)
colourGrating2 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0,5.0), pos= (0, -2.5), sf = SpatialFrequency, units = 'deg', 
                            color = (0,45,1.0), colorSpace = 'dkl', opacity = 0.25)
lumGrating1 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0,10.0), pos=(0,0), sf = SpatialFrequency, units = 'deg', 
                            color = (-90, 0, 1), opacity = 0.5, colorSpace = 'dkl', ori = alignment)
lumGrating2 = visual.PatchStim(myWin, tex = 'sqr', size = (10.0, 5.0), pos=(-2.5,0), sf = SpatialFrequency, units = 'deg', 
                            color = (-90, 0, 1), opacity = 0.25, colorSpace = 'dkl', ori = alignment)


#redPatch = visual.PatchStim(myWin, tex = None, size = (10.0, 5.0), pos = (0.5, 2.5), units = 'deg', color = (0, 0, 1.0), colorSpace='dkl')
#greenPatch = visual.PatchStim(myWin, tex=None, size = (10.0, 5.0), pos = (0.5, -2.0), units = 'deg', color = (0,0,-1.0), colorSpace = 'dkl')
#
#darkPatch = visual.PatchStim(myWin, tex=None, size = (5.0, 10.0), pos = (-2.0, 0.0), units = 'deg', color = (1.0,0,0), colorSpace = 'dkl', opacity = 0.5)
#
#redPatch.draw()
#greenPatch.draw()
#darkPatch.draw()
#myWin.flip()

lumGrating1.draw()
colourGrating1.draw()

#colourGrating2.draw()
#lumGrating2.draw()
myWin.flip()

#myWin.getMovieFrame()
#myWin.saveMovieFrames('bwEqual3.tif') 

junk =event.waitKeys()