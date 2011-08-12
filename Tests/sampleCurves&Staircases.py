#sampleCurves&Staircases.py (13/9/2010)
from psychopy import data, gui, misc, core
from matplotlib import rcParams, use
use ('WxAgg') 
import pylab, numpy, scipy, copy, os
fileTag = '_5000boots'

#---Set some general parameters for your psychometric function plots 
lineWidth = 1
fSize =10
labelFont = {'fontname': 'Helvetica', 'fontsize': 10}

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#---First figure: staircases
#get the data from all the files
allIntensitiesL,allIntensitiesR, allResponsesL,allResponsesR, = [],[],[],[]
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
    thisOb = thisDat.extraInfo["observer"]
    thisSide = thisDat.extraInfo["contourField"]
    thisAngle = thisDat.extraInfo['angleRef']
    thisLocation = thisDat.extraInfo['location']
    thisSize = thisDat.extraInfo['size']
    thisStimOri = thisDat.extraInfo['stimOri']
    assert isinstance(thisDat, data.StairHandler)
    if thisSide == 'l':
        allIntensitiesL.append( thisDat.intensities )
        allResponsesL.append( thisDat.data )
    if thisSide == 'r':
        allIntensitiesR.append( thisDat.intensities )
        allResponsesR.append( thisDat.data )

pylab.figure(1, figsize = (5,5)) 
#plot all staircase on a single figure with a legend showing the timestring and title showing the condition
pylab.subplot(211)
for fileN, thisStair in enumerate(allIntensitiesL):
    pylab.plot(thisStair, '-')
pylab.title('%s_left_loc=%0.0f' %(thisOb,thisLocation))
pylab.ylabel("Angle of test probe (compound side) (Deg)")
pylab.xlabel("Trial")
xlimits=pylab.xlim([0,50])
ylimits=pylab.ylim([140,165])

pylab.subplot(212)
for fileN, thisStair in enumerate(allIntensitiesR):
    pylab.plot(thisStair, '-')
pylab.title('%s_right_loc=%0.0f' %(thisOb,thisLocation))
xlimits=pylab.xlim([0,50])
ylimits=pylab.ylim([140,165])

pylab.savefig ('Analysis%s//FIGURES//SampleStaircases.png' %(fileTag), dpi = 600) 
pylab.savefig ('Analysis%s//FIGURES//SampleStaircases.eps' %(fileTag), dpi = 600) 

pylab.figure(2, figsize = (5,5)) 
#left side trials
combinedInten, combinedResp, combinedN = data.functionFromStaircase(allIntensitiesL, allResponsesL, 'unique')#fit curve
guess= [pylab.mean(combinedInten), 4.0]
fit = data.FitWeibull(combinedInten, combinedResp, expectedMin=0.0, guess=guess, display=0)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.5)
lower = fit.inverse(0.25)
upper = fit.inverse(0.75)
jnd =  upper - lower
#plot curve
pylab.plot(smoothInt, smoothResp, '-k')
pylab.plot([thresh, thresh],[0,0.5],'--r'); pylab.plot([0, thresh],[0.5,0.5],'--r')
#plot points
maxN=max(combinedN); minN=min(combinedN)
maxMarker=8.0; minMarker=4.0
for pointN in range(len(combinedInten)):
    thisN = combinedN[pointN]
    thisMarkerSize = minMarker+(thisN-minN)*(maxMarker-minMarker)/(maxN-minN)
    pylab.plot([combinedInten[pointN]], [combinedResp[pointN]], 'ok', markerfacecolor='k', label = '_nolegend_',markeredgewidth=1.0, markersize=thisMarkerSize)
                            
#right side trials
combinedInten, combinedResp, combinedN = data.functionFromStaircase(allIntensitiesR, allResponsesR, 'unique')#fit curve
guess= [pylab.mean(combinedInten), 4.0]
fit = data.FitWeibull(combinedInten, combinedResp, expectedMin=0.0, guess=guess, display=0)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.5)
lower = fit.inverse(0.25)
upper = fit.inverse(0.75)
jnd =  upper - lower
#plot curve
pylab.plot(smoothInt, smoothResp, '-k')
pylab.plot([thresh, thresh],[0,0.5],'--r'); pylab.plot([0, thresh],[0.5,0.5],'--r')
#plot points
maxN=max(combinedN); minN=min(combinedN)
maxMarker=8.0; minMarker=4.0
for pointN in range(len(combinedInten)):
    thisN = combinedN[pointN]
    thisMarkerSize = minMarker+(thisN-minN)*(maxMarker-minMarker)/(maxN-minN)
    pylab.plot([combinedInten[pointN]], [combinedResp[pointN]], 'ok', markerfacecolor='w', label = '_nolegend_',markeredgewidth=1.0, markersize=thisMarkerSize)      


xlimits=pylab.xlim([130,165])
ylimits=pylab.ylim([-0.01,1.01])
pylab.ylabel('Proportion responses to the compound side')
pylab.xlabel("Angle of test probe (compound side) (Deg)")

pylab.savefig ('Analysis%s//FIGURES//SampleCurves.png' %(fileTag), dpi = 600) 
pylab.savefig ('Analysis%s//FIGURES//SampleCurves.eps' %(fileTag), dpi = 600) 

pylab.show()