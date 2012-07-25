#Testing boots data

import cPickle
from psychopy import data, gui, core, misc
import numpy as np
import pylab
from scipy import stats


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
            markerPos = dat.data['Marker'][n][m]
            finalPos = np.abs(markerPos - dat.data['LumEdge'][n][m])
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

LumSTD = np.std(LumPositions)
LMSTD = np.std(LMPositions)
SSTD = np.std(SPositions)
LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

lumCounter = 0
lmCounter = 0
sCounter = 0
lmlumCounter = 0
slumCounter = 0
lmsCounter = 0

#Remove outliers
for n in LumPositions:
    if (((n-LumMean)/LumSTD)>3.0) or (((n-LumMean)/LumSTD)<-3.0):
        LumPositions.remove(n)
        lumCounter +=1
        
for n in LMPositions:
    if (((n-LMMean)/LMSTD)>3.0) or (((n-LMMean)/LMSTD)<-3.0):
        LMPositions.remove(n)
        lmCounter +=1
        
for n in SPositions:
    if (((n-SMean)/SSTD)>3.0) or (((n-SMean)/SSTD)<-3.0):
        SPositions.remove(n)
        sCounter +=1
        
for n in LMLumPositions:
    if (((n-LMLumMean)/LMLumSTD)>3.0) or (((n-LMLumMean)/LMLumSTD)<-3.0):
        LMLumPositions.remove(n)
        lmlumCounter +=1

for n in SLumPositions:
    if (((n-SLumMean)/SLumSTD)>3.0) or (((n-SLumMean)/SLumSTD)<-3.0):
        SLumPositions.remove(n)
        slumCounter +=1
        
for n in LMSPositions:
    if (((n-LMSMean)/LMSSTD)>3.0) or (((n-LMSMean)/LMSSTD)<-3.0):
        LMSPositions.remove(n)
        lmsCounter +=1

LumMean = np.mean(LumPositions)
LMMean = np.mean(LMPositions)
SMean = np.mean(SPositions)
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)
#
#print LumMean, LMMean, SMean, LMLumMean, SLumMean, LMSMean

LumSTD = np.std(LumPositions)
LMSTD = np.std(LMPositions)
SSTD = np.std(SPositions)
LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

#calculate linear summation predicted values
lum = LumSTD
lm = LMSTD
s = SSTD

lm = (lm/(np.sqrt(2)))**2
s = (s/(np.sqrt(2)))**2
lum = (lum/(np.sqrt(2)))**2

lmlum = (lm*lum)/(lm+lum)
slum = (s*lum)/(s+lum)
lms = (lm*s)/(lm+s)

lmlumLin = (np.sqrt(lmlum))*(np.sqrt(2))
slumLin = (np.sqrt(slum))*(np.sqrt(2))
lmsLin = (np.sqrt(lms))*(np.sqrt(2))

fileName = ('MOABootsNoOutliers_RJSAll.pickle')
pkl_file = open(fileName, 'rb')
everything = cPickle.load(pkl_file)
#print len(data1['bootLumPositions'])

#std 95% confidence interval
LumCI = everything['StdHiLowCI']['LumHi']-everything['StdHiLowCI']['LumLow']
LMCI = everything['StdHiLowCI']['LMHi']-everything['StdHiLowCI']['LMLow']
SCI = everything['StdHiLowCI']['SHi']-everything['StdHiLowCI']['SLow']
LMLumCI = everything['StdHiLowCI']['LMLumHi']-everything['StdHiLowCI']['LMLumLow']
SLumCI = everything['StdHiLowCI']['SLumHi']-everything['StdHiLowCI']['SLumLow']
LMSCI = everything['StdHiLowCI']['LMSHi']-everything['StdHiLowCI']['LMSLow']

#lin 95% confidence interval
LMLumLinCI = everything['bootLin']['bootLMLumLinHi']-everything['bootLin']['bootLMLumLinLow']
SLumLinCI = everything['bootLin']['bootSLumLinHi']-everything['bootLin']['bootSLumLinLow']
LMSLinCI = everything['bootLin']['bootLMSLumLinHi']-everything['bootLin']['bootLMSLumLinLow']

#SEM
bootLumSem = stats.sem(everything['bootStd']['bootLumStd'])
bootLmSem = stats.sem(everything['bootStd']['bootLMStd'])
bootSSem = stats.sem(everything['bootStd']['bootSStd'])
bootLMLumSem = stats.sem(everything['bootStd']['bootLMLumStd'])
bootSLumSem = stats.sem(everything['bootStd']['bootSLumStd'])
bootLMSSem = stats.sem(everything['bootStd']['bootLMSStd'])
#
#lin SEM
bootLMLumLinSem = stats.sem(everything['LMLumLin'])
bootSLumLinSem = stats.sem(everything['SLumLin'])
bootLMSLinSem = stats.sem(everything['LMSLin'])

#SEM
bootLumSem = np.std(everything['bootStd']['bootLumStd'])
bootLmSem = np.std(everything['bootStd']['bootLMStd'])
bootSSem = np.std(everything['bootStd']['bootSStd'])
bootLMLumSem = np.std(everything['bootStd']['bootLMLumStd'])
bootSLumSem = np.std(everything['bootStd']['bootSLumStd'])
bootLMSSem = np.std(everything['bootStd']['bootLMSStd'])

#lin SEM
bootLMLumLinSem = np.std(everything['LMLumLin'])
bootSLumLinSem = np.std(everything['SLumLin'])
bootLMSLinSem = np.std(everything['LMSLin'])

#calculate winner takes all values
if LumSTD<LMSTD:
    lmlumWin = LumSTD
    lmlumWinSem = bootLumSem
if LumSTD>LMSTD:
    lmlumWin = LMSTD
    lmlumWinSem = bootLmSem
if LumSTD<SSTD:
    slumWin = LumSTD
    slumWinSem = bootLumSem
if LumSTD>SSTD:
    slumWin = SSTD
    slumWinSem = bootSSem
if LMSTD<SSTD:
    lmsWin = LMSTD
    lmsWinSem = bootLmSem
if LMSTD>SSTD:
    lmsWin = SSTD
    lmsWinSem = bootSSem

#Plot stds
LumBar = pylab.bar(0, LumSTD, facecolor = 'gray', label = 'Lum', yerr = bootLumSem, ecolor = 'black')
LMBar = pylab.bar(1, LMSTD, facecolor = 'red', label = 'LM', yerr = bootLmSem, ecolor = 'black')
SBar = pylab.bar(2, SSTD, facecolor = 'blue', label = 'S', yerr = bootSSem, ecolor = 'black')
LMLumBar = pylab.bar(3, LMLumSTD, facecolor = 'pink', label = 'LMLum', yerr = bootLMLumSem, ecolor = 'black')
LMLumLinBar = pylab.bar(4, lmlumLin, facecolor = 'pink', label = 'LMLumLin', yerr = bootLMLumLinSem, ecolor = 'black', hatch = '/')
LMLumWinBar = pylab.bar(5, lmlumWin, facecolor = 'pink', label = 'LMLumWin', yerr = lmlumWinSem, ecolor = 'black', hatch = 'x')
SLumBar = pylab.bar(6, SLumSTD, facecolor = 'dodgerblue', label = 'SLum', yerr = bootSLumSem, ecolor = 'black')
SLumLinBar = pylab.bar(7, slumLin, facecolor = 'dodgerblue', label = 'SLumLin', yerr = bootSLumLinSem, ecolor = 'black',  hatch = '/')
SLumWinBar = pylab.bar(8, slumWin, facecolor = 'dodgerblue', label = 'SLumWin', yerr = slumWinSem, ecolor = 'black', hatch = 'x')
LMSBar = pylab.bar(9, LMSSTD, facecolor = 'orange', label = 'LMS', yerr = bootLMSSem, ecolor = 'black')
LMSLinBar = pylab.bar(10, lmsLin, facecolor = 'orange', label = 'LMSLin', yerr = bootLMSLinSem, ecolor = 'black', hatch = '/')
LMSWinBar = pylab.bar(11, lmsWin, facecolor = 'orange', label = 'LMSWin', yerr = lmsWinSem, ecolor = 'black', hatch = 'x')

print 'Lm: sem', bootLmSem
print 'S: sem', bootSSem
print 'LMS sem', bootLMSSem, 'lin', lmsLin, 'linerr',  bootLMSLinSem, 'win', lmsWin, 'winerr', lmsWinSem

pylab.legend()
pylab.show()
pkl_file.close()
