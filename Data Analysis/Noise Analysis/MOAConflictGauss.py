#MOA Analysis, Plotting Gaussians - April 2012

from psychopy import data, gui, core, misc, compatibility
import numpy as np
import pylab, copy

#Import file to analyse
files = gui.fileOpenDlg('.')
if not files:
    core.quit()
    
LMLumPositions = []
SLumPositions = []
LMSPositions = []
#LMLumFlipPositions = []
#SLumFlipPositions = []
#LMSFlipPositions = []

LMLumZ = []
SLumZ = []
LMSZ = []
#LMLumFlipZ = []
#SLumFlipZ = []
#LMSFlipZ = []
   
for thisFileName in files:
    dat = compatibility.fromFile(thisFileName)
    conditions = dat.trialList
    for n in range(len(dat.data['Condition'])):
        for m in range(dat.nReps):
            markerPos = dat.data['Marker'][n][m]
#            finalPos = np.abs(markerPos - dat.data['LumEdge'][n][m])
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

                
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)
#LMLumFlipMean = np.mean(LMLumFlipPositions)
#SLumFlipMean = np.mean(SLumFlipPositions)
#LMSFlipMean = np.mean(LMSFlipPositions)

LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)
#LMLumFlipSTD = np.std(LMLumFlipPositions)
#SLumFlipSTD = np.std(SLumFlipPositions)
#LMSFlipSTD = np.std(LMSFlipPositions)

lmlumCounter = 0
slumCounter = 0
lmsCounter = 0
#lmlumFlipCounter = 0
#slumFlipCounter = 0
#lmsFlipCounter = 0

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

#for n in LMLumFlipPositions:
#    temp = (n-LMLumFlipMean)/LMLumFlipSTD
#    LMLumFlipZ.append(temp)
#    if (temp>3.0) or (temp<-3.0):
#        LMLumFlipZ.remove(temp)
#
#for n in SLumFlipPositions:
#    temp = (n-SLumFlipMean)/SLumFlipSTD
#    SLumFlipZ.append(temp)
#    if (temp>3.0) or (temp<-3.0):
#        SLumFlipZ.remove(temp)

#for n in LMSFlipPositions:
#    temp = (n-LMSFlipMean)/LMSFlipSTD
#    LMSFlipZ.append(temp)
#    if (temp>3.0) or (temp<-3.0):
#        LMSFlipZ.remove(temp)
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
        
#for n in LMLumFlipPositions:
#    print ((n-LMLumFlipMean)/LMLumFlipSTD)
#    if (((n-LMLumFlipMean)/LMLumFlipSTD)>3.0) or (((n-LMLumFlipMean)/LMLumFlipSTD)<-3.0):
#        LMLumFlipPositions.remove(n)
#        lmlumFlipCounter +=1

#for n in SLumFlipPositions:
#    if (((n-SLumFlipMean)/SLumFlipSTD)>3.0) or (((n-SLumFlipMean)/SLumFlipSTD)<-3.0):
#        SLumFlipPositions.remove(n)
#        slumFlipCounter +=1
#        
#for n in LMSFlipPositions:
#    if (((n-LMSFlipMean)/LMSFlipSTD)>3.0) or (((n-LMSFlipMean)/LMSFlipSTD)<-3.0):
#        LMSFlipPositions.remove(n)
#        lmsCounter +=1
        
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)

LMLumSTD = np.std(LMLumPositions)
SLumSTD = np.std(SLumPositions)
LMSSTD = np.std(LMSPositions)

#LMLumFlipMean = np.mean(LMLumFlipPositions)
#SLumFlipMean = np.mean(SLumFlipPositions)
#LMSFlipMean = np.mean(LMSFlipPositions)
#
#LMLumFlipSTD = np.std(LMLumFlipPositions)
#SLumFlipSTD = np.std(SLumFlipPositions)
#LMSFlipSTD = np.std(LMSFlipPositions)

#print 'LmLum Mean', LMLumMean, 'Std', LMLumSTD
#print 'SLum Mean', SLumMean, 'Std', SLumSTD
#print 'LMS Mean', LMSMean, 'Std', LMSSTD

LMLumSE = (LMLumSTD/np.sqrt(dat.nReps))
SLumSE = (SLumSTD/np.sqrt(dat.nReps))
LMSSE = (LMSSTD/np.sqrt(dat.nReps))

#LMLumFlipSE = (LMLumFlipSTD/np.sqrt(dat.nReps))
#SLumFlipSE = (SLumFlipSTD/np.sqrt(dat.nReps))
#LMSFlipSE = (LMSFlipSTD/np.sqrt(dat.nReps))

print 'lmlum Outliers', lmlumCounter
print 'slum Outliers', slumCounter
print 'lms Outliers', lmsCounter
#print 'lmlum Flip Outliers', lmlumFlipCounter
#print 'slum Flip Outliers', slumFlipCounter
#print 'lms Flip Outliers', lmsFlipCounter

#Plot histograms for each condition

#LMLum
pylab.subplot(311)
LMLumOrder = copy.copy(LMLumPositions)
LMLumOrder.sort()

#LMLumFlipOrder = copy.copy(LMLumFlipPositions)
#LMLumFlipOrder.sort()


#for n in range(len(LMLumFlipOrder)):
#    LMLumFlipOrder[n] *= -1.0

LMLumgauss = (1/(LMLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMLumOrder-LMLumMean)**2 / (2*LMLumSTD**2))
#LMLumFlipgauss = (1/(LMLumFlipSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMLumFlipOrder-(LMLumFlipMean*-1.0))**2 / (2*LMLumFlipSTD**2))

LMLumHist = pylab.hist(LMLumOrder, bins=10, facecolor='cornflowerblue', label='LM Lum')
#LMLumFlipHist = pylab.hist(LMLumFlipOrder, bins=10, facecolor='indianred', alpha = 0.5)
LMLumGaussPlot = pylab.plot(LMLumOrder, LMLumgauss, 'r-')
#LMLumFlipGaussPlot = pylab.plot(LMLumFlipOrder, LMLumFlipgauss, 'r-')
LMLine = pylab.axvline(x=0.05, color = 'k', linestyle = '--')
LumLine = pylab.axvline(x=0.0, color = 'k', linestyle = '--')
LMLumMeanLine = pylab.axvline(x=LMLumMean, color = 'k', linestyle = ':')
#LMLumFlipLine = pylab.axvline(x=LMLumFlipMean*-1.0, color = 'k', linestyle = ':')
pylab.title('LM + Lum')
#Label for Luminance central
pylab.xlabel('0.00 = Lum (Black to White)      0.05 = LM (Turquoise to Salmon)      Centre = Pale Turquoise')
pylab.xlim(-0.08, 0.09)
#Label for LM Central
#pylab.xlabel('0.00 =LM (Turquoise to Salmon)       0.05 = Lum (Black to White)      Centre = Dark Turquoise')
#pylab.xlim(0.09, -0.08)

#pylab.ylim(0,20)

#pylab.legend(frameon=False)

#SLum
pylab.subplot(312)
SLumOrder = copy.copy(SLumPositions)
SLumOrder.sort()
#SLumFlipOrder = copy.copy(SLumFlipPositions)
#SLumFlipOrder.sort()

#for n in range(len(SLumFlipOrder)):
#    SLumFlipOrder[n] *= -1.0

SLumgauss = (1/(SLumSTD*(np.sqrt(2*np.pi))))*np.exp(-(SLumOrder-SLumMean)**2 / (2*SLumSTD**2))
#SLumFlipgauss = (1/(SLumFlipSTD*(np.sqrt(2*np.pi))))*np.exp(-(SLumFlipOrder-(SLumFlipMean*-1.0))**2 / (2*SLumFlipSTD**2))

SLumHist = pylab.hist(SLumOrder, bins=10, facecolor='cornflowerblue', label = 'S Lum')
#SLumFlipHist = pylab.hist(SLumFlipOrder, bins=10, facecolor='indianred', alpha = 0.5)
SLumGaussPlot = pylab.plot(SLumOrder, SLumgauss, 'r-')
#SLumFlipGaussPlot = pylab.plot(SLumFlipOrder, SLumFlipgauss, 'r-')
SLine = pylab.axvline(x=0.05, color = 'k', linestyle = '--')
LumLine = pylab.axvline(x=0.0, color = 'k', linestyle = '--')
SLumMeanLine = pylab.axvline(x=SLumMean, color = 'k', linestyle = ':')
#SLumFlipLine = pylab.axvline(x=SLumFlipMean*-1.0, color = 'k', linestyle = ':')

#Label for Luminance central
pylab.xlabel('0.00 = Lum (Black to White)           0.05 = S (Purple to Lime)           Centre = Pale Purple')
pylab.xlim(-0.08, 0.09)
#Label for LM Central
#pylab.xlabel('0.00 =S (Purple to Lime)            0.05 = Lum (Black to White)           Centre = Dark Purple')
#pylab.xlim(0.09, -0.08)

pylab.title('S + Lum')

#pylab.ylim(0,20)

#pylab.legend(frameon=False)

#LMS
pylab.subplot(313)
LMSOrder = copy.copy(LMSPositions)
LMSOrder.sort()
#LMSFlipOrder = copy.copy(LMSFlipPositions)
#LMSFlipOrder.sort()

#for n in range(len(LMSFlipOrder)):
#    LMSFlipOrder[n] *= -1.0

LMSgauss = (1/(LMSSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMSOrder-LMSMean)**2 / (2*LMSSTD**2))
#LMSFlipgauss = (1/(LMSFlipSTD*(np.sqrt(2*np.pi))))*np.exp(-(LMSFlipOrder-(LMSFlipMean*-1.0))**2 / (2*LMSFlipSTD**2))

LMSHist = pylab.hist(LMSOrder, bins=10, facecolor='cornflowerblue', label='LM S')
#LMSFlipHist = pylab.hist(LMSFlipOrder, bins=10, facecolor='indianred', alpha = 0.5)
LMSGaussPlot = pylab.plot(LMSOrder, LMSgauss, 'r-')
#LMSFlipGaussPlot = pylab.plot(LMSFlipOrder, LMSFlipgauss, 'r-')

SLine = pylab.axvline(x=0.05, color = 'k', linestyle = '--')
LMLine = pylab.axvline(x=0.0, color = 'k', linestyle = '--')
LMSMeanLine = pylab.axvline(x=LMSMean, color = 'k', linestyle = ':')
#LMSFlipLine = pylab.axvline(x=LMSFlipMean*-1.0, color = 'k', linestyle = ':')

#Label for Luminance central
pylab.xlabel('0.00 = LM (Turquoise to Salmon)           0.05 = S (Purple to Lime)           Centre = Pink')
pylab.xlim(-0.08, 0.09)
#Label for LM Central
#pylab.xlabel('0.00 =S (Purple to Lime)            0.05 = LM (Turquoise to Salmon)           Centre = Green')
#pylab.xlim(0.09,-0.08)

pylab.title('LM + S')

#pylab.legend(frameon=False)
pylab.tight_layout()
pylab.show()