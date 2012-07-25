#MOA Analysis, Plotting Gaussians - April 2012

from psychopy import data, gui, core, misc, compatibility
import numpy as np
import pylab, copy

#Import file to analyse
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

nBoots = 5000
    
#Create dictionaries/lists
LMLumPositions = []
SLumPositions = []
LMSPositions = []

LMLumZ = []
SLumZ = []
LMSZ = []

bootLMLumPositions = []
bootSLumPositions = []
bootLMSPositions = []

everything = {}
   
for thisFileName in files:
    dat = compatibility.fromFile(thisFileName)
    conditions = dat.trialList
    for n in range(len(dat.data['Condition'])):
        for m in range(dat.nReps):
            markerPos = dat.data['Marker'][n][m]
            finalPos = markerPos - dat.data['LumEdge'][n][m]
            if dat.extraInfo['Flip']=='n':
                if dat.data['Condition'][n][m]=='LMLum':
                    LMLumPositions.append(finalPos)
                if dat.data['Condition'][n][m]=='SLum':
                    SLumPositions.append(finalPos)
                if dat.data['Condition'][n][m]=='LMS':
                    LMSPositions.append(finalPos)
            if dat.extraInfo['Flip']=='y':
                if dat.data['Condition'][n][m]=='LMLum':
                    LMLumPositions.append(finalPos*-1)
                if dat.data['Condition'][n][m]=='SLum':
                    SLumPositions.append(finalPos*-1)
                if dat.data['Condition'][n][m]=='LMS':
                    LMSPositions.append(finalPos*-1)
                
#Remove outliers
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)

LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

lmlumCounter = 0
slumCounter = 0
lmsCounter = 0

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
for n in LMLumPositions:
    print ((n-LMLumMean)/LMLumSTD)
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
        
        
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)

LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

print 'lmlum Outliers', lmlumCounter
print 'slum Outliers', slumCounter
print 'lms Outliers', lmsCounter

#Bootstrapping
positions = [LMLumPositions, SLumPositions, LMSPositions]

for n in positions:
    rawDat = [n]
    bootSamples = data.bootStraps(rawDat, n=nBoots)
    for bootN in range(nBoots):
        thisBoot = bootSamples[:,:,bootN]
        if n==LMLumPositions:
            bootLMLumPositions.append(thisBoot)
        if n==SLumPositions:
            bootSLumPositions.append(thisBoot)
        if n==LMSPositions:
            bootLMSPositions.append(thisBoot)
            
LMLumSE = np.std(bootLMLumPositions)
SLumSE = np.std(bootSLumPositions)
LMSSE = np.std(bootLMSPositions)

#Plot histograms for each condition
#LMLum
pylab.subplot(311)
LMLumOrder = copy.copy(LMLumPositions)
LMLumOrder.sort()

for n in range(len(LMLumOrder)):
    LMLumOrder[n] *= -1.0
    LMLumOrder[n] += 0.05
LMLumMean *= -1.0
LMLumMean += 0.05

LMLumgauss = (1/(LMLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*LMLumSTD**2))+0.05

LMSalmonBackground = pylab.axvspan(-0.1, 0.05, facecolor = 'lightcoral', alpha = 0.25)
LMGreenBackground = pylab.axvspan(0.05, 0.15, facecolor = 'mediumaquamarine', alpha = 0.25)
LumBlkBackground = pylab.axvspan(-0.1, 0.0, facecolor = 'white', alpha = 0.5)
LumWhiteBackground = pylab.axvspan(0.0, 0.15, facecolor = 'gray', alpha = 0.25)

LMLumHist = pylab.hist(LMLumOrder, bins=10, facecolor='cornflowerblue', label='LM Lum')
LMLumGaussPlot = pylab.plot(LMLumOrder, LMLumgauss, 'r-')

LMLumError = pylab.axvspan((LMLumMean-LMLumSE), (LMLumMean+LMLumSE), facecolor = 'gray', alpha = 0.25)
LMLine = pylab.axvline(x=0.05, color = 'k', linestyle = '--')
LumLine = pylab.axvline(x=0.0, color = 'k', linestyle = '--')
LMLumMeanLine = pylab.axvline(x=LMLumMean, color = 'k', linestyle = ':')

pylab.title('LM + Lum')
#Label
pylab.xlabel('0.00 = Lum (White to Black)      0.05 = LM (Salmon to Turquoise)      Centre = Dark Salmon')
pylab.xlim(-0.1, 0.15)

#SLum
pylab.subplot(312)
SLumOrder = copy.copy(SLumPositions)
SLumOrder.sort()

for n in range(len(SLumOrder)):
    SLumOrder[n] *= -1.0
    SLumOrder[n] += 0.05
SLumMean *= -1.0
SLumMean += 0.05

SLumgauss = (1/(SLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(SLumOrder-SLumMean)**2 / (2*SLumSTD**2))+0.05

SPurpleBackground = pylab.axvspan(-0.1, 0.05, facecolor = 'yellowgreen', alpha = 0.25)
SLimeBackground = pylab.axvspan(0.05, 0.15, facecolor = 'mediumpurple', alpha = 0.25)
LumBlkBackground = pylab.axvspan(-0.1, 0.0, facecolor = 'white', alpha = 0.5)
LumWhiteBackground = pylab.axvspan(0.0, 0.15, facecolor = 'gray', alpha = 0.25)

SLumHist = pylab.hist(SLumOrder, bins=10, facecolor='cornflowerblue')
SLumGaussPlot = pylab.plot(SLumOrder, SLumgauss, 'r-')

SLumError = pylab.axvspan((SLumMean-SLumSE), (SLumMean+SLumSE), facecolor = 'gray', alpha = 0.25)

SLine = pylab.axvline(x=0.05, color = 'k', linestyle = '--')
LumLine = pylab.axvline(x=0.0, color = 'k', linestyle = '--')
SLumMeanLine = pylab.axvline(x=SLumMean, color = 'k', linestyle = ':')

pylab.xlabel('0.00 = Lum (White to Black)           0.05 = S (Lime to Purple)           Centre = Dark Lime')
pylab.xlim(-0.1, 0.15)

pylab.title('S + Lum')

#LMS
pylab.subplot(313)
LMSOrder = copy.copy(LMSPositions)
LMSOrder.sort()

for n in range(len(LMSOrder)):
    LMSOrder[n] *= -1.0
    LMSOrder[n] += 0.05
LMSMean *= -1.0
LMSMean += 0.05

LMSgauss = (1/(LMSSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMSOrder-LMSMean)**2 / (2*LMSSTD**2))+0.05

LMSalmonBackground = pylab.axvspan(-0.1, 0.0, facecolor = 'lightcoral', alpha = 0.25)
LMGreenBackground = pylab.axvspan(0.0, 0.15, facecolor = 'mediumaquamarine', alpha = 0.25)
SPurpleBackground = pylab.axvspan(-0.1, 0.05, facecolor = 'yellowgreen', alpha = 0.25)
SLimeBackground = pylab.axvspan(0.05, 0.15, facecolor = 'mediumpurple', alpha = 0.25)

LMSHist = pylab.hist(LMSOrder, bins=10, facecolor='cornflowerblue')
LMSGaussPlot = pylab.plot(LMSOrder, LMSgauss, 'r-')

LMSError = pylab.axvspan((LMSMean-LMSSE), (LMSMean+LMSSE), facecolor = 'gray', alpha = 0.25)

SLine = pylab.axvline(x=0.05, color = 'k', linestyle = '--')
LMLine = pylab.axvline(x=0.0, color = 'k', linestyle = '--')
LMSMeanLine = pylab.axvline(x=LMSMean, color = 'k', linestyle = ':')

#Label 
pylab.xlabel('0.00 = LM (Salmon to Turquoise)           0.05 = S (Lime to Purple)           Centre = Green')
pylab.xlim(-0.1, 0.15)

pylab.title('LM + S')

pylab.legend(frameon=False)
pylab.tight_layout()
pylab.show()