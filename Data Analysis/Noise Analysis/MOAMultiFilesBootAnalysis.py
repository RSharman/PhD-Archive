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
width = 0.5
LumBar = pylab.bar(0.25, LumStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'Lum')
LumBar2 = pylab.bar(0.25, LumStd, width, facecolor = 'none', yerr = LumSem, ecolor = 'black')
Lum002Bar = pylab.bar(1.25, Lum002Std, width, facecolor =  '#0032ff', alpha = 0.25, label = 'Lum')
Lum002Bar2 = pylab.bar(1.25, Lum002Std, width, facecolor = 'none', yerr = Lum002Sem, ecolor = 'black')
LMBar = pylab.bar(2.25, LMStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'LM')
LMBar2 = pylab.bar(2.25, LMStd, width, facecolor = 'none', yerr = LMSem, ecolor = 'black')
SBar = pylab.bar(3.25, SStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'S')
SBar = pylab.bar(3.25, SStd, width, facecolor = 'none', yerr = SSem, ecolor = 'black')

LMLumBar = pylab.bar(5.25, LMLumStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMLum')
LMLumBar2 = pylab.bar(5.25, LMLumStd, width, facecolor = 'none', yerr = LMLumSem, ecolor = 'black')
#LMLumLinBar = pylab.bar(6.25, LMLumLin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMLumLin')
#LMLumLinBar2 = pylab.bar(6.25, LMLumLin, width, facecolor = 'none', yerr = LMLumLinSem, ecolor = 'black', hatch = '/')
#LMLumWinBar = pylab.bar(7.25, lmlumWin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMLumWin')
#LMLumWinBar2 = pylab.bar(7.25, lmlumWin, width, facecolor = 'none', yerr = lmlumWinSem, ecolor = 'black', hatch = 'x')

LMLum002Bar = pylab.bar(6.25, LMLum002Std, width, facecolor = '#0032ff', alpha = 0.25, label = 'LMLum')
LMLum002Bar2 = pylab.bar(6.25, LMLum002Std, width, facecolor = 'none', yerr = LMLum002Sem, ecolor = 'black')
#LMLum002LinBar = pylab.bar(10.25, LMLum002Lin, width, facecolor = '#0032ff', alpha = 0.25, label = 'LMLumLin')
#LMLum002LinBar = pylab.bar(10.25, LMLum002Lin, width, facecolor = 'none', yerr = LMLum002LinSem, ecolor = 'black', hatch = '/')
#LMLum002WinBar = pylab.bar(11.25, lmlum002Win, width, facecolor = '#0032ff', alpha = 0.25, label = 'LMLumWin')
#LMLum002WinBar2 = pylab.bar(11.25, lmlum002Win, width, facecolor = 'none', yerr = lmlum002WinSem, ecolor = 'black', hatch = 'x')

SLumBar = pylab.bar(8.25, SLumStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'SLum')
SLumBar2 = pylab.bar(8.25, SLumStd, width, facecolor = 'none', yerr = SLumSem, ecolor = 'black')
#SLumLinBar = pylab.bar(14.25, SLumLin, width, facecolor = '#0032ff', alpha = 0.75, label = 'SLumLin')
#SLumLinBar2 = pylab.bar(14.25, SLumLin, width, facecolor = 'none', yerr = SLumLinSem, ecolor = 'black',  hatch = '/')
#SLumWinBar = pylab.bar(15.25, slumWin, width, facecolor = '#0032ff', alpha = 0.75, label = 'SLumWin')
#SLumWinBar2 = pylab.bar(15.25, slumWin, width, facecolor = 'none', yerr = slumWinSem, ecolor = 'black', hatch = 'x')

SLum002Bar = pylab.bar(9.25, SLum002Std, width, facecolor = '#0032ff', alpha = 0.25, label = 'SLum')
SLum002Bar2 = pylab.bar(9.25, SLum002Std, width, facecolor = 'none', yerr = SLum002Sem, ecolor = 'black')
#SLum002LinBar = pylab.bar(18.25, SLum002Lin, width, facecolor = '#0032ff', alpha = 0.25, label = 'SLumLin')
#SLum002LinBar2 = pylab.bar(18.25, SLum002Lin, width, facecolor = 'none', yerr = SLum002LinSem, ecolor = 'black',  hatch = '/')
#SLum002WinBar = pylab.bar(19.25, slum002Win, width, facecolor = '#0032ff', alpha = 0.25, label = 'SLumWin')
#SLum002WinBar2 = pylab.bar(19.25, slum002Win, width, facecolor = 'none', yerr = slum002WinSem, ecolor = 'black', hatch = 'x')

LMSBar = pylab.bar(11.25, LMSStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMS')
LMSBar2 = pylab.bar(11.25, LMSStd, width, facecolor = 'none', yerr = LMSSem, ecolor = 'black')
#LMSLinBar = pylab.bar(22.25, LMSLin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMSLin')
#LMSLinBar2 = pylab.bar(22.25, LMSLin, width, facecolor = 'none', yerr = LMSLinSem, ecolor = 'black', hatch = '/')
#LMSWinBar = pylab.bar(23.25, lmsWin, width, facecolor = '#0032ff', label = 'LMSWin')
#LMSWinBar2 = pylab.bar(23.25, lmsWin, width, facecolor = 'none', yerr = lmsWinSem, ecolor = 'black', hatch = 'x')

#xlabels = pylab.xticks(((np.arange(24))+width/2.0)+0.25, ('Lum', 'Lum 0.02', 'LM', 'S', '', 'LMLum', 'LMLum Lin', 'LMLum Win', '', \
#                        'LMLum 0.02', 'LMLum Lin 0.02', 'LMLum Win 0.02', '', 'SLum', 'SLum Lin', 'SLum Win', '', 'SLum 0.02', \
#                        'SLum Lin 0.02', 'SLum Win 0.02', '', 'LMS', 'LMS Lin', 'LMS Win'), rotation = 'vertical')

xlabels = pylab.xticks(((np.arange(12))+width/2.0)+0.25, ('Lum', 'Lum 0.02', 'LM', 'S', '', 'LMLum', \
                        'LMLum 0.02', '', 'SLum', 'SLum 0.02', '', 'LMS'), rotation = 'vertical')
pylab.xlabel('Conditions')
pylab.ylabel('Standard Deviation (Degrees)')

pylab.tight_layout()

#pylab.legend()
pylab.show()
pkl_file1.close()
pkl_file2.close()