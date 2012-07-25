#Bootstrapping for MOA - March 2012

from psychopy import data, gui, core, misc
import numpy as np
import pylab, copy, os, cPickle

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

nBoots = 5000

#Create dictionaries/lists
LumPositions = []
#LMPositions = []
#SPositions = []
LMLumPositions = []
SLumPositions = []
LMSPositions = []

bootLumPositions = []
#bootLMPositions = []
#bootSPositions = []
bootLMLumPositions = []
bootSLumPositions = []
bootLMSPositions = []

bootLumStd = []
#bootLMStd = []
#bootSStd = []
bootLMLumStd = []
bootSLumStd = []
bootLMSStd = []

everything={}
everything['bootStd'] = {}
everything['bootLin'] = {}
everything['StdHiLowCI'] = {}
everything['LinHiLowCI']={}
everything['LMLumLin']=[]
everything['SLumLin']=[]
everything['LMSLin']=[]

#Open files
for thisFileName in files:
    dat = misc.fromFile(thisFileName)
    conditions = dat.trialList
    #Extract edge positions relative to the markers
    for n in range(len(dat.data['Condition'])):
        for m in range(dat.nReps):
            markerPos = dat.data['Marker'][n][m]
            finalPos = (markerPos - dat.data['LumEdge'][n][m])
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

#Remove outliers
LumMean = np.mean(LumPositions)
LMMean = -0.004545
SMean = 0.009807
LMLumMean = np.mean(LMLumPositions)
SLumMean = np.mean(SLumPositions)
LMSMean = np.mean(LMSPositions)

LumSTD = np.std(LumPositions)
LMSTD = 0.03382
SSTD = 0.07144
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
    if (((n-LumMean)/LumSTD)>3.0) or (((n-LumMean)/LumSTD)<-3.0):
        LumPositions.remove(n)
        lumCounter +=1
        
#for n in LMPositions:
#    if (((n-LMMean)/LMSTD)>3.0) or (((n-LMMean)/LMSTD)<-3.0):
#        LMPositions.remove(n)
#        lmCounter +=1
#        
#for n in SPositions:
#    if (((n-SMean)/SSTD)>3.0) or (((n-SMean)/SSTD)<-3.0):
#        SPositions.remove(n)
#        sCounter +=1
        
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

#participant = dat.extraInfo['Participant']
positions = [LumPositions, LMLumPositions, SLumPositions, LMSPositions]
#positions = [LumPositions, LMPositions, SPositions, LMLumPositions, SLumPositions, LMSPositions]

#Bootstrap the conditions individually
for n in positions:
    rawDat = [n]  
    bootSamples = data.bootStraps(rawDat, n=nBoots)
    for bootN in range(nBoots):
        thisBoot = bootSamples[:,:,bootN]
    #    bootLum = np.take(dat, thisBoot)
        if n == LumPositions:
            bootLumPositions.append(thisBoot)
            thisLumBootStd = np.std(thisBoot)
            bootLumStd.append(thisLumBootStd)
#        if n == LMPositions:
#            bootLMPositions.append(thisBoot)
#            thisLMBootStd = np.std(thisBoot)
#            bootLMStd.append(thisLMBootStd)
#        if n == SPositions:
#            bootSPositions.append(thisBoot)
#            thisSBootStd = np.std(thisBoot)
#            bootSStd.append(thisSBootStd)
        if n == LMLumPositions:
            bootLMLumPositions.append(thisBoot)
            thisLMLumBootStd = np.std(thisBoot)
            bootLMLumStd.append(thisLMLumBootStd)
        if n == SLumPositions:
            bootSLumPositions.append(thisBoot)
            thisSLumBootStd = np.std(thisBoot)
            bootSLumStd.append(thisSLumBootStd)
        if n == LMSPositions:
            bootLMSPositions.append(thisBoot)
            thisLMSBootStd = np.std(thisBoot)
            bootLMSStd.append(thisLMSBootStd)
            
#for n in range(nBoots):
    lum = bootLumStd[n]
    lm = bootLMStd[n]
    s = bootSStd[n]
    
    lm = (lm/(np.sqrt(2)))**2
    s = (s/(np.sqrt(2)))**2
    lum = (lum/(np.sqrt(2)))**2

    lmlum = (lm*lum)/(lm+lum)
    slum = (s*lum)/(s+lum)
    lms = (lm*s)/(lm+s)

    lmlumLin = (np.sqrt(lmlum))*(np.sqrt(2))
    slumLin = (np.sqrt(slum))*(np.sqrt(2))
    lmsLin = (np.sqrt(lms))*(np.sqrt(2))
    
    everything['LMLumLin'].append(lmlumLin)
    everything['SLumLin'].append(slumLin)
    everything['LMSLin'].append(lmsLin)

#Calculate the 95% CI for the standard deviations
lowIndex = int(0.025*nBoots)
hiIndex = int(0.975*nBoots)

bootLumStdCopy = copy.copy(bootLumStd)
bootLumStdCopy.sort()
LumStdlow95 = bootLumStdCopy[lowIndex]
LumStdhi95 = bootLumStdCopy[hiIndex]

#bootLMStdCopy = copy.copy(bootLMStd)
#bootLMStdCopy.sort()
#LMStdlow95 = bootLMStdCopy[lowIndex]
#LMStdhi95 = bootLMStdCopy[hiIndex]
#
#bootSStdCopy = copy.copy(bootSStd)
#bootSStdCopy.sort()
#SStdlow95 = bootSStdCopy[lowIndex]
#SStdhi95 = bootSStdCopy[hiIndex]

bootLMLumStdCopy = copy.copy(bootLMLumStd)
bootLMLumStdCopy.sort()
LMLumStdlow95 = bootLMLumStdCopy[lowIndex]
LMLumStdhi95 = bootLMLumStdCopy[hiIndex]
#lmlumLinCopy = copy.copy(everything['LMLumLin'])
#lmlumLinCopy.sort()
#LMLumLinlow95 = lmlumLinCopy[lowIndex]
#LMLumLinhi95 = lmlumLinCopy[hiIndex]

bootSLumStdCopy = copy.copy(bootSLumStd)
bootSLumStdCopy.sort()
SLumStdlow95 = bootSLumStdCopy[lowIndex]
SLumStdhi95 = bootSLumStdCopy[hiIndex]
#slumLinCopy = copy.copy(everything['SLumLin'])
#slumLinCopy.sort()
#SLumLinlow95 = slumLinCopy[lowIndex]
#SLumLinhi95 = slumLinCopy[hiIndex]

bootLMSStdCopy = copy.copy(bootLMSStd)
bootLMSStdCopy.sort()
LMSStdlow95 = bootLMSStdCopy[lowIndex]
LMSStdhi95 = bootLMSStdCopy[hiIndex]
#lmsLinCopy = copy.copy(everything['LMSLin'])
#LMSLinlow95 = lmsLinCopy[lowIndex]
#LMSLinhi95 = lmsLinCopy[hiIndex]


#File everything to be saved
everything['bootLumPositions'] = bootLumPositions
#everything['bootLMPositions'] = bootLMPositions
#everything['bootSPositions'] = bootSPositions
everything['bootLMLumPositions'] = bootLMLumPositions
everything['bootSLumPositions'] = bootSLumPositions
everything['bootLMSPositions'] = bootLMSPositions
everything['bootStd']['bootLumStd'] = bootLumStd
#everything['bootStd']['bootLMStd'] = bootLMStd
#everything['bootStd']['bootSStd'] = bootSStd
everything['bootStd']['bootLMLumStd'] = bootLMLumStd
everything['bootStd']['bootSLumStd'] = bootSLumStd
everything['bootStd']['bootLMSStd'] = bootLMSStd
everything['StdHiLowCI']['LumLow'] = LumStdlow95
everything['StdHiLowCI']['LumHi'] = LumStdhi95
#everything['StdHiLowCI']['LMLow'] = LMStdlow95
#everything['StdHiLowCI']['LMHi'] = LMStdhi95
#everything['StdHiLowCI']['SLow'] = SStdlow95
#everything['StdHiLowCI']['SHi'] = SStdhi95
everything['StdHiLowCI']['LMLumLow'] = LMLumStdlow95
everything['StdHiLowCI']['LMLumHi'] = LMLumStdhi95
everything['StdHiLowCI']['SLumLow'] = SLumStdlow95
everything['StdHiLowCI']['SLumHi'] = SLumStdhi95
everything['StdHiLowCI']['LMSLow'] = LMSStdlow95
everything['StdHiLowCI']['LMSHi'] = LMSStdhi95
#everything['bootLin']['bootLMLumLinLow'] = LMLumLinlow95
#everything['bootLin']['bootLMLumLinHi'] = LMLumLinhi95
#everything['bootLin']['bootSLumLinLow'] = SLumLinlow95
#everything['bootLin']['bootSLumLinHi'] = SLumLinhi95
#everything['bootLin']['bootLMSLumLinLow'] = LMSLinlow95
#everything['bootLin']['bootLMSLumLinHi'] = LMSLinhi95

#Save the bootStraps
temp = cPickle.HIGHEST_PROTOCOL
fileName = ('0.02MOABootsNoOutliers_RJSAll.pickle')
f = open(fileName, "wb")
cPickle.Pickler(f, temp).dump(everything)
f.close()

#pkl_file = open(fileName, 'rb')
#data1 = cPickle.load(pkl_file)
#print data1
#pkl_file.close()

