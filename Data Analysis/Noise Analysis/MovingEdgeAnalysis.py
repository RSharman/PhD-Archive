#!/usr/bin/env python

#This analysis script takes one or more staircase datafiles as input from a GUI
#It then plots the staircases on top of each other on the left 
#and a combined psychometric function from the same data
#on the right
#

from psychopy import data, gui, misc, core, logging
import pylab, scipy
import numpy as np
import cPickle
import pickle

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses, extraInfo, positions, reversalIntensities = [],[],[],[],[]
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
    assert isinstance(thisDat, data.StairHandler)
    allIntensities.append( thisDat.intensities)
    allResponses.append( thisDat.data)
    extraInfo.append(thisDat.extraInfo)
    reversalIntensities.append(thisDat.reversalIntensities)
#    print 'extra', extraInfo
#    temp = extraInfo[0]
#    print 'edge', temp['lumEdgePos']*10
    print 'last 6 reversals mean = %.3f' %(scipy.average(thisDat.reversalIntensities[-6:]))#-(temp['lumEdgePos']*10))

channels = []

for n in range(len(extraInfo)):
    temp = extraInfo[n]
    positions.append(temp['lumEdgePos'])
    print 'edge', temp['lumEdgePos']
    channels.append(temp['Channel'])
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
    label = files[fileN]
    pylab.plot(thisStair, label=label[-21:])
#pylab.legend()
#pylab.ylim(0.5,-0.5)


#get combined data
combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(allIntensities, allResponses, bins = 'unique')
             
print combinedN
#print 'len', len(np.array(allIntensities[0]))#, 'Inten', allIntensities
#print 'len', len(np.array(allResponses[0])), 'Resp', allResponses
#
#print 'len', len(combinedInten), 'Inten', combinedInten
#print 'len', len(combinedResp), 'Resp', combinedResp

sem = np.array(combinedN)

combinedInten = pylab.array(combinedInten)+100
#fit curve
fit = data.FitWeibull(combinedInten, combinedResp, sems=1.0, guess=(100,100), expectedMin=0.0)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)

fit2 = data.FitWeibull(combinedInten, combinedResp, sems=1.0/sem, guess=(100,100), expectedMin=0.0)
smoothResp2 = fit2.eval(smoothInt)

smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.5)-100
lower = fit.inverse(0.25)-100
upper = fit.inverse(0.75)-100
jnd = upper-lower
#print 'pse', thresh, 'jnd', jnd
#print 'alpha, beta', fit.params[0]-100, fit.params[1]

threshComb = fit2.inverse(0.5)-100
lower2 = fit2.inverse(0.25)-100
upper2 = fit2.inverse(0.75)-100
jnd2 = upper2-lower2
print '1/combN pse', threshComb, 'jnd', jnd2
print '1/combN alpha, beta', fit2.params[0]-100, fit2.params[1]

#plot curve
pylab.subplot(122)
pylab.plot(smoothInt-100, smoothResp, 'k-')
pylab.plot(smoothInt-100, smoothResp2, 'k--')
pylab.plot([thresh, thresh],[0,0.5],'k--'); pylab.plot([0, thresh],[0.5,0.5],'k--')
pylab.title('pse = %0.3f' %(threshComb))



combinedInten-=100
#plot points
maxN=max(combinedN); minN=min(combinedN)
#print len(combinedN)
maxMarker=8.0; minMarker=4.0
for pointN in range(len(combinedInten)):
    thisN = combinedN[pointN]
    thisMarkerSize = minMarker+(thisN-minN)*(maxMarker-minMarker)/(maxN-minN)
    pylab.plot([combinedInten[pointN]], [combinedResp[pointN]], 'ok', markerfacecolor='k', label = '_nolegend_',markeredgewidth=1.0, markersize=thisMarkerSize)
#plot points
pylab.plot(combinedInten, combinedResp, 'ko')
pylab.ylim([0,1])
#plot points
maxN=max(combinedN); minN=min(combinedN)
maxMarker=8.0; minMarker=4.0
for pointN in range(len(combinedInten)):
    thisN = combinedN[pointN]
    thisMarkerSize = minMarker+(thisN-minN)*(maxMarker-minMarker)/(maxN-minN)
    pylab.plot([combinedInten[pointN]], [combinedResp[pointN]], 'ok', markerfacecolor='w', label = '_nolegend_',markeredgewidth=1.0, markersize=thisMarkerSize)      
#print 'last 6 reversals mean for %s = %.3f' %(thisDat.extraInfo.Participant, (scipy.average(thisDat.reversalIntensities[-6:])))
#pylab.xlim(-0.5,0.5)
#extraInfo=extraInfo[0]
#print 'last 6 reversals mean = %.3f' %(scipy.average(thisDat.reversalIntensities[-6:]))#-extraInfo['lumEdgePos'])


pylab.show()
    

    