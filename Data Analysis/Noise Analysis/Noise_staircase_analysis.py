#!/usr/bin/env python

#This analysis script takes one or more staircase datafiles as input from a GUI
#It then plots the staircases on top of each other on the left 
#and a combined psychometric function from the same data
#on the right
#

from psychopy import data, gui, misc, core
import pylab, scipy
import numpy as np

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses, extraInfo, positions, reversalIntensities = [],[],[],[],[]
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
    assert isinstance(thisDat, data.StairHandler)
    allIntensities.append( thisDat.intensities )
    allResponses.append( thisDat.data )
    extraInfo.append(thisDat.extraInfo)
    reversalIntensities.append(thisDat.reversalIntensities)
#    print 'extra', extraInfo
#    temp = extraInfo[0]
#    print 'edge', temp['lumEdgePos']*10
    print 'last 6 reversals mean = %.3f' %(scipy.average(thisDat.reversalIntensities[-6:]))#-(temp['lumEdgePos']*10))

for n in range(len(extraInfo)):
    temp = extraInfo[n]
    positions.append(temp['lumEdgePos']*10)
    print 'edge', temp['lumEdgePos']*10
#    print 'last 6 reversals mean = %.3f' %(scipy.average(thisDat.reversalIntensities[-6:]))
#    print 'last 6 reversals mean = %.3f' %(scipy.average(thisDat.reversalIntensities[-6:])-(temp['lumEdgePos']*10))

newIntensities=[]
for n in range(len(allIntensities)):
    allIntensities[n]=np.array(allIntensities[n])
    allIntensities[n]-=positions[n]
    reversalIntensities[n]=np.array(reversalIntensities[n])
    reversalIntensities[n]-=positions[n]

#allIntensities = (pylab.array(allIntensities))-position
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
             data.functionFromStaircase(allIntensities, allResponses, 5)
             
combinedInten = (pylab.array(combinedInten)*10)+100
#fit curve
fit = data.FitWeibull(combinedInten, combinedResp, guess=None)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.5)
print 'thresh', thresh
print 'pse, jnd', fit.params
#plot curve
pylab.subplot(122)
pylab.plot(smoothInt-100, smoothResp, 'k-')
pylab.plot([thresh, thresh],[0,0.5],'k--'); pylab.plot([0, thresh],[0.5,0.5],'k--')
pylab.title('threshold = %0.3f' %(thresh))
#plot points
pylab.plot(combinedInten-100, combinedResp, 'ko-')
pylab.ylim([0,1])

#print 'last 6 reversals mean for %s = %.3f' %(thisDat.extraInfo.Participant, (scipy.average(thisDat.reversalIntensities[-6:])))

#extraInfo=extraInfo[0]
#print 'last 6 reversals mean = %.3f' %(scipy.average(thisDat.reversalIntensities[-6:]))#-extraInfo['lumEdgePos'])


pylab.show()
    

    