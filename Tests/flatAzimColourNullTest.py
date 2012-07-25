#Testing changing the elevation while keeping the azimuth flat using PatchStim/GratingStim - July 2012

from psychopy import visual, core, misc, monitors, event, filters
import copy
import numpy as np

myWin = visual.Window(size=(1024, 768), monitor = 'dklTest', units = 'degs', 
    fullscr=False, allowGUI=True)
myMon= monitors.Monitor('dklTest')
conversionMatrix = myMon.getDKL_RGB(RECOMPUTE=False)

def flatAzim(res, cone, ori=0.0, cycles=1.0, phase=0.0, elevation = 0.0):
    """Creates a grating defined either by S or LM in DKL space. The elevation
    can be changed whilst keeping the azimuth flat - in effect changing the position
    of the azimuth
    
    Warning: May generate values >1 or <-1
    
    :Parameters:
        res: integer
            the size of the resulting matrix on both dimensions (e.g 256)
        cone: 'LM' or 'S'
            which axis in DKL space the grating should be created in
        ori: float or int (default=0.0)
            the orientation of the grating in degrees
        cycles:float or int (default=1.0)
            the number of grating cycles within the array
        phase: float or int (default=0.0)
            the phase of the grating in degrees (NB this differs to most
            PsychoPy phase arguments which use units of fraction of a cycle)
        elevation: float or int (default=0.0)
            the angle that the azimuth will be changed to

    :Returns:
        a square numpy array of size resXres
        """

    gabor = filters.makeGrating(res, ori=ori, cycles = cycles, phase=phase)

    colorGabor = np.zeros((len(gabor), len(gabor), 3))
    colorGabor[:,:,0] = copy.copy(gabor)
    colorGabor[:,:,1] = copy.copy(gabor)
    colorGabor[:,:,2] = copy.copy(gabor)

    dklGabor = misc.rgb2dklCart(colorGabor)
    if cone=='LM':
        dklGabor = misc.cart2sph(dklGabor[:,:,0]*0.0, dklGabor[:,:,0]*0.0, dklGabor[:,:,0])
    if cone=='S':
        dklGabor = misc.cart2sph(dklGabor[:,:,0]*0.0, dklGabor[:,:,0], dklGabor[:,:,0]*0.0)

    temp = copy.copy(dklGabor[:,:,1])+1
    temp = (temp/np.abs(temp))*+elevation
    dklGabor[:,:,0] += temp

    rgbGabor = misc. dkl2rgb(dklGabor)
    return rgbGabor

tex = flatAzim(512, 'S', cycles=10.0, elevation=-45.0)/2.0

rgbGabor = visual.PatchStim(myWin, tex = tex, mask = 'gauss', units = 'deg', size = 10.0, sf = 0.05)
rgbGabor.draw()

#dklGabor = visual.PatchStim(myWin, tex='sin', mask='gauss', units='deg', size=10.0, sf = 0.5, colorSpace='dkl', contrast=0.2)
#dklGabor.setColor([0,45,1.0])
#dklGabor.draw()
myWin.flip()

event.waitKeys()
