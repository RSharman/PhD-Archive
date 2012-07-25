#!/usr/bin/env python

#This analysis script takes one or more staircase datafiles as input from a GUI
#It then plots the staircases on top of each other on the left 
#and a combined psychometric function from the same data
#on the right
#

from psychopy import data, gui, misc, core, compatibility
import pylab, scipy
import numpy as np

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses = [],[]
for thisFileName in files:
    thisDat = compatibility.fromFile(thisFileName)
    assert isinstance(thisDat, data.StairHandler)
    allIntensities.append( thisDat.intensities )
    allResponses.append( thisDat.data )
    
#plot each staircase
pylab.subplot(121)
colors = 'brgkcmbrgkcm'
lines, names = [],[]
for fileN, thisStair in enumerate(allIntensities):
    #lines.extend(pylab.plot(thisStair))
    #names = files[fileN]
    pylab.plot(thisStair, label=files[fileN])
#pylab.legend()

#get combined data
combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(allIntensities, allResponses, 'unique')

combinedInten = np.asarray(combinedInten) +100
#fit curve
fit = data.FitWeibull(combinedInten, combinedResp, guess=[100.2, 0.5], expectedMin=0.0)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.5)-100
#thresh = fit.inverse(0.8)-100

#lower = fit.inverse(0.675)
#upper = fit.inverse(0.925)
lower = fit.inverse(0.25)-100
upper = fit.inverse(0.75)-100
jnd = upper-lower

print 'thresh', thresh
print 'jnd', jnd

#plot curve
pylab.subplot(122)
pylab.plot(smoothInt-100, smoothResp, 'k-')
pylab.plot([thresh, thresh],[0,0.5],'k--'); pylab.plot([0, thresh],[0.5,0.5],'k--')
pylab.title('threshold = %0.3f' %(thresh))
#plot points
#pylab.plot(combinedInten-100, combinedResp, 'ko')
pylab.ylim([0,1])

#plot points
maxN=max(combinedN); minN=min(combinedN)
#print len(combinedN)
maxMarker=8.0; minMarker=4.0

combinedInten -=100

for pointN in range(len(combinedInten)):
    thisN = combinedN[pointN]
    thisMarkerSize = minMarker+(thisN-minN)*(maxMarker-minMarker)/(maxN-minN)
    pylab.plot([combinedInten[pointN]], [combinedResp[pointN]], 'ok', markerfacecolor='w', label = '_nolegend_',markeredgewidth=1.0, markersize=thisMarkerSize)

pylab.show()
    

    