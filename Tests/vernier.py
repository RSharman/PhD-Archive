#Vernier acuity - July 2011

from psychopy import visual, event, core, monitors
import numpy as np

DEBUG = True

if DEBUG==True:
    myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'deg',
        fullscr=False, allowGUI=True, bitsMode=None)
    myMon = monitors.Monitor('testMonitor')
    conversionMatrix = None
    from psychopy import colorFunctions
    
if DEBUG==False:
    myWin = visual.Window(size=(1024, 768), monitor = 'hawk', units = 'deg',
        fullscr=True, allowGUI=False, bitsMode = None)
    myMon=monitors.Monitor('hawk')
    conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)
    import colorFunctions
   
stationaryMarker = visual.ShapeStim(myWin, units='deg', lineWidth=1.0, lineColor='black', fillColor = None,
                                    pos = (0,0), vertices = ((0,0), (0, -1.0)), closeShape = False)

positions = -0.04635, -0.0309, -0.01545, 0, 0.01545, 0.0309, 0.04635

for n in positions:
    variableMarker = visual.ShapeStim(myWin, units = 'deg', lineWidth=1.0, lineColor='blue', fillColor = None,
                                        pos = (n, 0), vertices = ((0,0), (0,1.0)), closeShape = False)
    variableMarker.draw()
    stationaryMarker.draw()
    myWin.flip()
    event.waitKeys()




