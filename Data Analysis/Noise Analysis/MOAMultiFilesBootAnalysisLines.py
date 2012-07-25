#Plotting data from boots - make sure you analyse the correct pickle files - Apr 2012

import cPickle
from psychopy import data, gui, core, misc
import numpy as np
import pylab

LumPositions = []
LMPositions = []
SPositions = []
LMLumPositions = []
SLumPositions = []
LMSPositions = []

#Open the pickle files
file1 = ('MOABootsNoOutliers_RJSAll.pickle')
file2 = ('0.02MOABootsNoOutliers_RJSAll.pickle')

pkl_file1 = open(file1, 'rb')
pkl_file2 = open(file2, 'rb')

everything1 = cPickle.load(pkl_file1)
everything2 = cPickle.load(pkl_file2)

#Calculate the bootstrapped means
LumMean = np.mean(everything1['bootLumPositions'])
Lum002Mean = np.mean(everything2['bootLumPositions'])
LMMean = np.mean(everything1['bootLMPositions'])
SMean = np.mean(everything1['bootSPositions'])
LMLumMean = np.mean(everything1['bootLMLumPositions'])
LMLum002Mean = np.mean(everything2['bootLMLumPositions'])
SLumMean = np.mean(everything1['bootSLumPositions'])
SLum002Mean = np.mean(everything2['bootSLumPositions'])
LMSMean = np.mean(everything1['bootLMSPositions'])

#Calculate the bootstrapped stds
LumStd = np.std(everything1['bootLumPositions'])
Lum002Std = np.std(everything2['bootLumPositions'])
LMStd = np.std(everything1['bootLMPositions'])
SStd = np.std(everything1['bootSPositions'])
LMLumStd = np.std(everything1['bootLMLumPositions'])
LMLum002Std = np.std(everything2['bootLMLumPositions'])
SLumStd = np.std(everything1['bootSLumPositions'])
SLum002Std = np.std(everything2['bootSLumPositions'])
LMSStd = np.std(everything1['bootLMSPositions'])

#SEM
LumSem = np.std(everything1['bootStd']['bootLumStd'])
Lum002Sem = np.std(everything2['bootStd']['bootLumStd'])
LMSem = np.std(everything1['bootStd']['bootLMStd'])
SSem = np.std(everything1['bootStd']['bootSStd'])
LMLumSem = np.std(everything1['bootStd']['bootLMLumStd'])
LMLum002Sem = np.std(everything2['bootStd']['bootLMLumStd'])
SLumSem = np.std(everything1['bootStd']['bootSLumStd'])
SLum002Sem = np.std(everything2['bootStd']['bootSLumStd'])
LMSSem = np.std(everything1['bootStd']['bootLMSStd'])

#Calculate linear summation for 0.02 values, combining information from both files
for n in range (5000):
    lum2 = everything2['bootStd']['bootLumStd'][n]
    lm2 = everything1['bootStd']['bootLMStd'][n]
    s2 = everything1['bootStd']['bootSStd'][n]
    
    lm2 = (lm2/(np.sqrt(2)))**2
    s2 = (s2/(np.sqrt(2)))**2
    lum2 = (lum2/(np.sqrt(2)))**2

    lmlum2 = (lm2*lum2)/(lm2+lum2)
    slum2 = (s2*lum2)/(s2+lum2)
    lms2 = (lm2*s2)/(lm2+s2)

    lmlumLin2 = (np.sqrt(lmlum2))*(np.sqrt(2))
    slumLin2 = (np.sqrt(slum2))*(np.sqrt(2))
    lmsLin2 = (np.sqrt(lms2))*(np.sqrt(2))
    
    everything2['LMLumLin'].append(lmlumLin2)
    everything2['SLumLin'].append(slumLin2)
    
#Linear Summation
LMLumLin = np.mean(everything1['LMLumLin'])
LMLum002Lin = np.mean(everything2['LMLumLin'])
SLumLin = np.mean(everything1['SLumLin'])
SLum002Lin =  np.mean(everything2['SLumLin'])
LMSLin = np.mean(everything1['LMSLin'])

#Linear Summation SEM
LMLumLinSem = np.std(everything2['LMLumLin'])
LMLum002LinSem = np.std(everything2['LMLumLin'])
SLumLinSem = np.std(everything1['SLumLin'])
SLum002LinSem = np.std(everything2['SLumLin'])
LMSLinSem = np.std(everything1['LMSLin'])
LMS002LinSem = np.std(everything1['LMSLin'])



#calculate winner takes all values
if LumStd<LMStd:
    lmlumWin = LumStd
    lmlumWinSem = LumSem
if LumStd>LMStd:
    lmlumWin = LMStd
    lmlumWinSem = LMSem
if LumStd<SStd:
    slumWin = LumStd
    slumWinSem = LumSem
if LumStd>SStd:
    slumWin = SStd
    slumWinSem = SSem
if LMStd<SStd:
    lmsWin = LMStd
    lmsWinSem = LMSem
if LMStd>SStd:
    lmsWin = SStd
    lmsWinSem = SSem

if Lum002Std<LMStd:
    lmlum002Win = LumStd
    lmlum002WinSem = Lum002Sem
if Lum002Std>LMStd:
    lmlum002Win = LMStd
    lmlum002WinSem = LMSem
if Lum002Std<SStd:
    slum002Win = Lum002Std
    slum002WinSem = Lum002Sem
if Lum002Std>SStd:
    slum002Win = SStd
    slum002WinSem = SSem

#Plot EVERYTHING!!
Locations = [0.25, 0.5, 0.75]

pylab.subplot(221)
RJSLine1 = pylab.errorbar(Locations, [LumStd, LMStd, SStd], marker = 'o', color = 'k', yerr = [LumSem, LMSem, SSem])
pylab.ylim(0, 0.08)
pylab.xticks(Locations, ('Lum', 'LM', 'S'))
pylab.ylabel('Standard Deviation (degrees)')
pylab.xlabel('Individual Cues')

pylab.subplot(222)
RJSLine2 = pylab.errorbar(Locations, [LMLumStd, SLumStd, LMSStd], marker = 'o', color = 'k', yerr = [LMLumSem, SLumSem, LMSSem])
pylab.ylim(0, 0.08)
pylab.xlabel('Combined Cues')
pylab.yticks([])
pylab.xticks(Locations, ('LM + Lum', 'S + Lum', 'LM + S'))

pylab.subplot(212)
LineOne = pylab.errorbar(Locations, [LumStd, LMLumStd, SLumStd], marker = 'o', color = 'k', yerr = [LumSem, LMLumSem, SLumSem], label = 'Luminance Contrast: 0.1')
Line225 = pylab.errorbar(Locations, [Lum002Std, LMLum002Std, SLum002Std], marker = 's', linestyle = ':', color = 'k', yerr = [Lum002Sem, LMLum002Sem, SLum002Sem], label = 'Luminance Contrast: 0.02')
pylab.ylim(0,0.08)
pylab.ylabel('Standard Deviation (degrees)')
pylab.xticks((np.arange(0.25, 1.0, 0.25)), ('Luminance', 'LM + Lum', 'S + Lum'))
pylab.legend(frameon=False)

pylab.tight_layout()

#pylab.legend()
pylab.show()
pkl_file1.close()
pkl_file2.close()