#MOA Analysis - March 2012

from psychopy import data, gui, core, misc
import numpy as np
import pylab

#Import file to analyse
files = gui.fileOpenDlg('.')
if not files:
    core.quit()
    
LumPositions = []
LMPositions = []
SPositions = []
LMLumPositions = []
SLumPositions = []
LMSPositions = []
   
for thisFileName in files:
    dat = misc.fromFile(thisFileName)
    conditions = dat.trialList
    for n in range(len(dat.data['Condition'])):
        for m in range(dat.nReps):
            markerPos = (dat.data['Marker'][n][m]+1.0)/2.0
            finalPos = markerPos - dat.data['LumEdge'][n][m]
            if dat.data['Condition'][n][m]=='Lum':
                LumPositions.append(finalPos)
            if dat.data['Condition'][n][m]=='LM':
                LMPositions.append(finalPos)
            if dat.data['Condition'][n][m]=='S':
                SPositions.append(finalPos)
            if dat.data['Condition'][n][m]=='LMLum':
                LMLumPositions.append(finalPos)
            if dat.data['Condition'][n][m]=='SLum':
                SLumPositions.append(finalPos)
            if dat.data['Condition'][n][m]=='LMS':
                LMSPositions.append(finalPos)

LumMean = np.mean(LumPositions)
LMMean = np.mean(LMPositions)
SMean = np.mean(SPositions)
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)

#print LumMean, LMMean, SMean, LMLumMean, SLumMean, LMSMean

LumSTD = np.std(LumPositions)
LMSTD = np.std(LMPositions)
SSTD = np.std(SPositions)
LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

#print 'Lum STD', LumSTD
#print 'LM STD', LMSTD
#print 'S STD', SSTD
#print 'LMLum STD', LMLumSTD
#print 'SLum STD', SLumSTD
#print 'LMS STD', LMSSTD

LumSE = (LumSTD/np.sqrt(dat.nReps))
LMSE = (LMSTD/np.sqrt(dat.nReps))
SSE = (SSTD/np.sqrt(dat.nReps))
LMLumSE = (LMLumSTD/np.sqrt(dat.nReps))
SLumSE = (SLumSTD/np.sqrt(dat.nReps))
LMSSE = (LMSSTD/np.sqrt(dat.nReps))

print 'Lum SE', LumSE
print 'LM SE', LMSE
print 'S SE', SSE
print 'LMLum SE', LMLumSE
print 'SLum SE', SLumSE
print 'LMS SE', LMSSE
#xBars = [0,1,2]
#
#MOABar = pylab.bar(xBars, [LumMean, LMLumMean, SLumMean], yerr=[LumSE, LMLumSE, SLumSE])
#pylab.show()

pylab.figure(1)
LumBar = pylab.bar(0, LumMean, facecolor = 'gray', yerr = LumSE, label = 'Lum', ecolor = 'black')
LMBar = pylab.bar(1, LMMean, facecolor = 'red', yerr = LMSE, label = 'LM', ecolor = 'black')
SBar = pylab.bar(2, SMean, facecolor = 'purple', yerr = SSE, label = 'S', ecolor = 'black')
LMLumBar = pylab.bar(3, LMLumMean, facecolor = 'yellow', yerr = LMLumSE, label = 'LMLum', ecolor = 'black')
SLumBar = pylab.bar(4, SLumMean, facecolor = 'green', yerr = SLumSE, label = 'SLum', ecolor = 'black')
LMSBar = pylab.bar(5, LMSMean, facecolor = 'orange', yerr = LMSSE, label = 'LMS', ecolor = 'black')
pylab.legend(loc = 'lower right')
pylab.ylim(-0.15, 0.08)
pylab.show()





