#!/usr/bin/env python

#Blur Detection Analysis Script - Jan 2011
#This analysis script takes one or more staircase datafiles as input from a GUI
#It then plots the staircases on top of each other on the left 
#and a combined psychometric function from the same data
#on the right
#It also plots the individual curves for each image.

from psychopy import data, gui, misc, core
import matplotlib
matplotlib.use('WXAgg')
import pylab, scipy, numpy

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#Get the individual data from the files
indIntensities={}
indResponses={}

for thisFileName in files:
    thisIndDat = misc.fromFile(thisFileName)
    for imageName, array in thisIndDat.extraInfo.iteritems():
        thisImageName = imageName
        indIntensities[thisImageName]=[]
        indResponses[thisImageName]=[]

        thisIntensity = thisIndDat.intensities
        thisResponse = thisIndDat.data
        indIntensities[thisImageName].extend(thisIntensity)
        indResponses[thisImageName].extend(thisResponse)
        
        #get individual data
        thisNewIntensity = indIntensities[thisImageName]
        thisNewResponse = indResponses[thisImageName]
        
        combinedIndInten, combinedIndResp, CombinedN = data.functionFromStaircase(thisIntensity, thisResponse, 'unique')

    #fit curve
        combinedIndInten = numpy.array(combinedIndInten)+100
        fit = data.FitWeibull(combinedIndInten, combinedIndResp, guess =[105, 10], expectedMin = 0.5)
        smoothIndInt = pylab.arange(min(combinedIndInten), max(combinedIndInten), 0.001)
        smoothIndResp = fit.eval(smoothIndInt)
        Threshold = fit.inverse(0.8)-100
        
        print 'Threshold', Threshold
        
        label = thisImageName + (" - %.2f" %Threshold)
        
        pylab.subplot(122)
        pylab.plot(smoothIndInt-100, smoothIndResp, '--', label = label)
        pylab.legend(loc = 'lower right')
#        pylab.plot(combinedIndInten-100, combinedIndResp, 'ro')

#        pylab.ylim([0,1])
#        pylab.xlim([-1, 0.5])
#pylab.show()


#get the combined data from all the files
allIntensities, allResponses, allNames = [],[],[]
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
    assert isinstance(thisDat, data.StairHandler)
    allIntensities.append( thisDat.intensities )
    allResponses.append( thisDat.data )
    for imageName, array in thisDat.extraInfo.iteritems():
        allNames.append(imageName)

#plot each staircase
pylab.subplot(121)
colors = 'brgkcmbrgkcm'
lines, names = [],[]
for fileN, thisStair in enumerate(allIntensities):
    #lines.extend(pylab.plot(thisStair))
    pylab.plot(thisStair)

#get combined data
combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(allIntensities, allResponses, 'unique')
             
combinedInten = numpy.array(combinedInten)+100
#fit curve
fit = data.FitWeibull(combinedInten, combinedResp, guess=[105,10], expectedMin=0.5)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.80)-100
lower = fit.inverse(0.625)
upper = fit.inverse(0.875)
jnd = upper-lower

#plot curve
pylab.subplot(122)
#pylab.plot(smoothInt-100, smoothResp, 'k-')
#pylab.plot([thresh, thresh],[0,0.80],'k.-.'); pylab.plot([0, thresh],[0.8,0.8],'k.-.')
pylab.title('threshold = %0.3f' %(thresh))
pylab.title('threshold = %0.3f (%0.3f)' %(thresh, jnd))
#plot points
#pylab.plot(combinedInten-100, combinedResp, 'ko')
pylab.ylim([0.5,1])
pylab.xlim([0, 0.25])

pylab.show()
    

    