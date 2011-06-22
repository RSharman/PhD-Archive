#Function to create a sharp edge

from psychopy import visual, event, colorFunctions
import numpy as np

def makeSharpEdge(center, size=512):
    """Create a matrix of a given size that switches from -1 to 1 at a given point.
    
    params:
                center: (float) the location of the center of the ramp as a fraction of the total matrix
                size: (int) width and height of the matrix
                """
    edge = np.ones(size*3, float)
    centerLocation = int(size+center*size)
    edge[:centerLocation]=0

    shpEdge = (edge[size:size*2]-edge.min())/(edge.max()-edge.min())
    shpEdge.shape = (1,size)

    return np.tile(shpEdge, (size,1))*2-1



myWin = visual.Window(size=(1024, 768), monitor = 'testMonitor', units = 'degs', 
        fullscr=False, allowGUI=True)

tex = makeSharpEdge(0.25, 512)


stim = visual.PatchStim(myWin, tex = tex, size = 10.0, units = 'deg', sf =(1/10.0))

stim.draw()
myWin.flip()

junk = event.waitKeys()