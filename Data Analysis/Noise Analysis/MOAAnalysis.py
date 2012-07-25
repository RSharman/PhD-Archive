#MOA Analysis - March 2012

from psychopy import data, gui, core, misc
import numpy as np
import pylab, copy

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
#            finalPos = np.abs(markerPos - dat.data['LumEdge'][n][m])
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

print 'Lum mean', LumMean
print 'LM Mean', LMMean
print 'S Mean', SMean
print 'LMLum Mean', LMLumMean
print 'SLum Mean', SLumMean
print 'LMS Mean', LMSMean

print 'Lum STD', LumSTD
print 'LM STD', LMSTD
print 'S STD', SSTD
print 'LMLum STD', LMLumSTD
print 'SLum STD', SLumSTD
print 'LMS STD', LMSSTD

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

#calculate winner takes all values
if LumSTD<LMSTD:
    lmlumWin = LumSTD
if LumSTD>LMSTD:
    lmlumWin = LMSTD
if LumSTD<SSTD:
    slumWin = LumSTD
if LumSTD>SSTD:
    slumWin = SSTD
if LMSTD<SSTD:
    lmsWin = LMSTD
if LMSTD>SSTD:
    lmsWin = SSTD
    
#print 'lmlumlin', lmlumLin
#print 'slumlin', slumLin
#print 'lmslin', lmsLin
#
#print 'lmlumwin', lmlumWin
#print 'slumwin', slumWin
#print 'lmswin', lmsWin

print 'lum Outliers', lumCounter
print 'lm Outliers', lmCounter
print 's Outliers', sCounter
print 'lmlum Outliers', lmlumCounter
print 'slum Outliers', slumCounter
print 'lms Outliers', lmsCounter

pylab.figure(1)
#plot means
#LumBar = pylab.bar(0, LumMean, facecolor = 'gray', yerr = LumSE, label = 'Lum', ecolor = 'black')
#LMBar = pylab.bar(1, LMMean, facecolor = 'red', yerr = LMSE, label = 'LM', ecolor = 'black')
#SBar = pylab.bar(2, SMean, facecolor = 'blue', yerr = SSE, label = 'S', ecolor = 'black')
#LMLumBar = pylab.bar(3, LMLumMean, facecolor = 'pink', yerr = LMLumSE, label = 'LMLum', ecolor = 'black')
#LMLumPredBar = pylab.bar(4, 0.01654, facecolor = 'pink', label = 'LMLumLin', hatch = '/')
#SLumBar = pylab.bar(5, SLumMean, facecolor = 'dodgerblue', yerr = SLumSE, label = 'SLum', ecolor = 'black')
#SLumPredBar = pylab.bar(6, 0.01958, facecolor = 'dodgerblue', label = 'SLumLin', hatch ='/')
#LMSBar = pylab.bar(7, LMSMean, facecolor = 'orange', yerr = LMSSE, label = 'LMS', ecolor = 'black')
#LMSPredBar = pylab.bar(8, 0.03122, facecolor = 'orange', label = 'LMSLin', hatch = '/')

#Plot stds
#LumBar = pylab.bar(0, LumSTD, facecolor = 'gray', label = 'Lum', ecolor = 'black')
#LMBar = pylab.bar(1, LMSTD, facecolor = 'red', label = 'LM', ecolor = 'black')
#SBar = pylab.bar(2, SSTD, facecolor = 'blue', label = 'S', ecolor = 'black')
#LMLumBar = pylab.bar(3, LMLumSTD, facecolor = 'pink', label = 'LMLum', ecolor = 'black')
#LMLumLinBar = pylab.bar(4, lmlumLin, facecolor = 'pink', label = 'LMLumLin', hatch = '/')
#LMLumWinBar = pylab.bar(5, lmlumWin, facecolor = 'pink', label = 'LMLumWin', hatch = 'x')
#SLumBar = pylab.bar(6, SLumSTD, facecolor = 'dodgerblue', label = 'SLum', ecolor = 'black')
#SLumLinBar = pylab.bar(7, slumLin, facecolor = 'dodgerblue', label = 'SLumLin', hatch = '/')
#SLumWinBar = pylab.bar(8, slumWin, facecolor = 'dodgerblue', label = 'SLumWin', hatch = 'x')
#LMSBar = pylab.bar(9, LMSSTD, facecolor = 'orange', label = 'LMS', ecolor = 'black')
#LMSLinBar = pylab.bar(10, lmsLin, facecolor = 'orange', label = 'LMSLin', hatch = '/')
#LMSWinBar = pylab.bar(11, lmsWin, facecolor = 'orange', label = 'LMSWin', hatch = 'x')

#Plot histograms for each condition
#LMLum
LMLumOrder = copy.copy(LMLumPositions)
LMLumOrder.sort()

#LumOrder = copy.copy(LumPositions)
#LumOrder.sort()
#
#gauss = (1/(LumSTD*(np.sqrt(2*np.pi))))*np.exp(-(LumOrder-LumMean)**2 / (2*LumSTD**2))
#LumHist = pylab.hist(LumOrder, bins=10)
#LumGauss = pylab.plot(LumOrder, gauss)

LMLumOrder = copy.copy(LMLumPositions)
LMLumOrder.sort()

LMLumPredStd = 0.01789

LMLumgauss = (1/(LMLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*LMLumSTD**2))
LMLumPredGauss = (1/(LMLumPredStd*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*LMLumPredStd**2))

LMLumHist = pylab.hist(LMLumOrder, bins=10)
LMLumGaussPlot = pylab.plot(LMLumOrder, LMLumgauss)
LMLumPredPlot = pylab.plot(LMLumOrder, LMLumPredGauss)

#pylab.legend(loc = 'upper right')
#pylab.ylim(0, 8)
pylab.show()





