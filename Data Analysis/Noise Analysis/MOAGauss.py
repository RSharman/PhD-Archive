#MOA Analysis, Plotting Gaussians - April 2012

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

LumZ = []
LMZ = []
SZ = []
LMLumZ = []
SLumZ = []
LMSZ = []
   
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

for n in LumPositions:
    temp = (n-LumMean)/LumSTD
    LumZ.append(temp)
    if (temp>3.0) or (temp<-3.0):
        LumZ.remove(temp)
    
for n in LMPositions:
    temp = (n-LMMean)/LMSTD
    LMZ.append(temp)
    if (temp>3.0) or (temp<-3.0):
        LMZ.remove(temp)
    
for n in SPositions:
    temp = (n-SMean)/SSTD
    SZ.append(temp)
    if (temp>3.0) or (temp<-3.0):
        SZ.remove(temp)
    
for n in LMLumPositions:
    temp = (n-LMLumMean)/LMLumSTD
    LMLumZ.append(temp)
    if (temp>3.0) or (temp<-3.0):
        LMLumZ.remove(temp)

for n in SLumPositions:
    temp = (n-SLumMean)/SLumSTD
    SLumZ.append(temp)
    if (temp>3.0) or (temp<-3.0):
        SLumZ.remove(temp)

for n in LMSPositions:
    temp = (n-LMSMean)/LMSSTD
    LMSZ.append(temp)
    if (temp>3.0) or (temp<-3.0):
        LMSZ.remove(temp)

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

LumSTD = np.std(LumPositions)
LMSTD = np.std(LMPositions)
SSTD = np.std(SPositions)
LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

LumSE = (LumSTD/np.sqrt(dat.nReps))
LMSE = (LMSTD/np.sqrt(dat.nReps))
SSE = (SSTD/np.sqrt(dat.nReps))
LMLumSE = (LMLumSTD/np.sqrt(dat.nReps))
SLumSE = (SLumSTD/np.sqrt(dat.nReps))
LMSSE = (LMSSTD/np.sqrt(dat.nReps))

#calculate linear summation predicted std values
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

#Plot histograms for each condition
#Lum
pylab.subplot(321)
LumOrder = copy.copy(LumPositions)
LumOrder.sort()

LumZ.sort()

LumGauss = (1/(LumSTD*(np.sqrt(2*np.pi))))*np.exp(-(LumOrder-LumMean)**2 / (2*LumSTD**2))

LumHist = pylab.hist(LumOrder, bins=10, facecolor='cornflowerblue')
LumGaussPlot = pylab.plot(LumOrder, LumGauss, 'r-', label = 'Lum Actual')

pylab.legend()

#LM
pylab.subplot(322)
LMOrder = copy.copy(LMPositions)
LMOrder.sort()
LmGauss = (1/(LMSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMOrder-LMMean)**2 / (2*LMSTD**2))

LmHist = pylab.hist(LMOrder, bins=10, facecolor='cornflowerblue')
LmGaussPlot = pylab.plot(LMOrder, LmGauss, 'r-', label = 'LM Actual')

pylab.legend()

#S
pylab.subplot(323)
SOrder = copy.copy(SPositions)
SOrder.sort()
SGauss = (1/(SSTD*(np.sqrt(2*np.pi))))*np.exp(-(SOrder-SMean)**2 / (2*SSTD**2))

SHist = pylab.hist(SOrder, bins=10, facecolor='cornflowerblue')
SGaussPlot = pylab.plot(SOrder, SGauss, 'r-', label = 'S Actual')

pylab.legend()

#LMLum
pylab.subplot(324)
LMLumOrder = copy.copy(LMLumPositions)
LMLumOrder.sort()

LMLumgauss = (1/(LMLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*LMLumSTD**2))
LMLumLinGauss = (1/(lmlumLin*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*lmlumLin**2))
LMLumWinGauss = (1/(lmlumWin*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*lmlumWin**2))

LMLumHist = pylab.hist(LMLumOrder, bins=10, facecolor='cornflowerblue')
LMLumGaussPlot = pylab.plot(LMLumOrder, LMLumgauss, 'r-', label = 'LMLum Actual')
LMLumLinPlot = pylab.plot(LMLumOrder, LMLumLinGauss, 'g--', label = 'LMLum Lin')
LMLumWinPlot = pylab.plot(LMLumOrder, LMLumWinGauss, 'k:', label = 'LMLum Win')

pylab.legend()

#SLum
pylab.subplot(325)
SLumOrder = copy.copy(SLumPositions)
SLumOrder.sort()

SLumgauss = (1/(SLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(SLumOrder-SLumMean)**2 / (2*SLumSTD**2))
SLumLinGauss = (1/(slumLin*(np.sqrt(2*np.pi))))*np.exp(-(SLumOrder-SLumMean)**2 / (2*slumLin**2))
SLumWinGauss = (1/(slumWin*(np.sqrt(2*np.pi))))*np.exp(-(SLumOrder-SLumMean)**2 / (2*slumWin**2))

SLumHist = pylab.hist(SLumOrder, bins=10, facecolor='cornflowerblue')
SLumGaussPlot = pylab.plot(SLumOrder, SLumgauss, 'r-', label = 'SLum Actual')
SLumLinPlot = pylab.plot(SLumOrder, SLumLinGauss, 'g--', label = 'SLum Lin')
SLumWinPlot = pylab.plot(SLumOrder, SLumWinGauss, 'k:', label = 'SLum Win')

pylab.legend()

#LMS
pylab.subplot(326)
LMSOrder = copy.copy(LMSPositions)
LMSOrder.sort()

LMSgauss = (1/(LMSSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMSOrder-LMSMean)**2 / (2*LMSSTD**2))
LMSLinGauss = (1/(lmsLin*(np.sqrt(2*np.pi))))*np.exp(-(LMSOrder-LMSMean)**2 / (2*lmsLin**2))
LMSWinGauss = (1/(lmsWin*(np.sqrt(2*np.pi))))*np.exp(-(LMSOrder-LMSMean)**2 / (2*lmsWin**2))

LMSHist = pylab.hist(LMSOrder, bins=10, facecolor='cornflowerblue')
LMSGaussPlot = pylab.plot(LMSOrder, LMSgauss, 'r-', label = 'LMS Actual')
LMSLinPlot = pylab.plot(LMSOrder, LMSLinGauss, 'g--', label = 'LMS Lin')
LMSWinPlot = pylab.plot(LMSOrder, LMSWinGauss, 'k:', label = 'LMS Win')

pylab.legend()
pylab.show()