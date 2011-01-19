#!/usr/bin/env python

#This analysis script takes one or more staircase datafiles as input from a GUI
#It then plots the staircases on top of each other on the left 
#and a combined psychometric function from the same data
#on the right
#

from psychopy import data, gui, misc, core
import matplotlib
matplotlib.use('WXAgg')
import pylab, scipy, numpy

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses = [],[]
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
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
             
combinedInten = numpy.array(combinedInten)+100
#fit curve
fit = data.FitWeibull(combinedInten, combinedResp, guess=[105,10], expectedMin=0.5)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.80)-100
#lower = fit.inverse(0.625)
#upper = fit.inverse(0.875)
#jnd = upper-lower

#plot curve
pylab.subplot(122)
pylab.plot(smoothInt-100, smoothResp, 'k-')
pylab.plot([thresh, thresh],[0,0.80],'k--'); pylab.plot([0, thresh],[0.8,0.8],'k--')
pylab.title('threshold = %0.3f' %(thresh))
#pylab.title('threshold = %0.3f (%0.3f)' %(thresh, jnd))
#plot points
pylab.plot(combinedInten-100, combinedResp, 'ko')
pylab.ylim([0.5,1])
pylab.xlim([0, 0.2])

pylab.show()
    

    