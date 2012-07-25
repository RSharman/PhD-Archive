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
comparisons = {}
stds = {}
sems = {}

subPosition = 310

#Open the pickle files
files = ['0.2_0.002MOABootsNoOutliers_DJHAll.pickle', '0.2_0.002MOABootsNoOutliers_DSAll.pickle', '0.2_0.002MOABootsNoOutliers_RJSAll.pickle']

for file in files:
    pkl_file1 = open(file, 'rb')

    everything = cPickle.load(pkl_file1)

    #Calculate the bootstrapped means
    LumMean = np.mean(everything['bootLumPositions'])
    LMMean = np.mean(everything['bootLMPositions'])
    SMean = np.mean(everything['bootSPositions'])
    LMLumMean = np.mean(everything['bootLMLumPositions'])
    SLumMean = np.mean(everything['bootSLumPositions'])
    LMSMean = np.mean(everything['bootLMSPositions'])

    #Calculate the bootstrapped stds
    LumStd = np.std(everything['bootLumPositions'])
    LMStd = np.std(everything['bootLMPositions'])
    SStd = np.std(everything['bootSPositions'])
    LMLumStd = np.std(everything['bootLMLumPositions'])
    SLumStd = np.std(everything['bootSLumPositions'])
    LMSStd = np.std(everything['bootLMSPositions'])

    #SEM
    LumSem = np.std(everything['bootStd']['bootLumStd'])
    LMSem = np.std(everything['bootStd']['bootLMStd'])
    SSem = np.std(everything['bootStd']['bootSStd'])
    LMLumSem = np.std(everything['bootStd']['bootLMLumStd'])
    SLumSem = np.std(everything['bootStd']['bootSLumStd'])
    LMSSem = np.std(everything['bootStd']['bootLMSStd'])

    #Linear Summation
    LMLumLin = np.mean(everything['LMLumLin'])
    SLumLin = np.mean(everything['SLumLin'])
    LMSLin = np.mean(everything['LMSLin'])

    #Linear Summation SEM
    LMLumLinSem = np.std(everything['LMLumLin'])
    SLumLinSem = np.std(everything['SLumLin'])
    LMSLinSem = np.std(everything['LMSLin'])

    #calculate winner takes all values
    if LumStd<LMStd:
        lmlumWin = LumStd
        lmlumWinSem = LumSem
        everything['LMLumWin'] = everything['bootStd']['bootLumStd']
    if LumStd>LMStd:
        lmlumWin = LMStd
        lmlumWinSem = LMSem
        everything['LMLumWin'] = everything['bootStd']['bootLMStd']
    if LumStd<SStd:
        slumWin = LumStd
        slumWinSem = LumSem
        everything['SLumWin'] = everything['bootStd']['bootLumStd']
    if LumStd>SStd:
        slumWin = SStd
        slumWinSem = SSem
        everything['SLumWin'] = everything['bootStd']['bootSStd']
    if LMStd<SStd:
        lmsWin = LMStd
        lmsWinSem = LMSem
        everything['LMSWin'] = everything['bootStd']['bootLMStd']
    if LMStd>SStd:
        lmsWin = SStd
        lmsWinSem = SSem
        everything['LMSWin'] = everything['bootStd']['bootSStd']
        
    #Calculate the difference between model and behaviour
    participant = str(everything['Participant'])
    comparisons[participant] = {}
    comparisons[participant]['Lin'] = np.mean((LMLumStd-LMLumLin), (SLumStd-SLumLin), (LMSStd-LMSLin))
    comparisons[participant]['Win'] = np.mean((LMLumStd-lmlumWin), (SLumStd-slumWin), (LMSStd-lmsWin))
    comparisons[participant]['LinErr'] = []
    comparisons[participant]['WinErr'] = []
    
    stds[participant] = {}
    stds[participant]['Lum'] = LumStd
    stds[participant]['LM'] = LMStd
    stds[participant]['S'] = SStd
    stds[participant]['LMLum'] = LMLumStd
    stds[participant]['SLum'] = SLumStd
    stds[participant]['LMS'] = LMSStd
    sems[participant] = {}
    sems[participant]['Lum'] = LumSem
    sems[participant]['LM'] = LMSem
    sems[participant]['S'] = SSem
    sems[participant]['LMLum'] = LMLumSem
    sems[participant]['SLum'] = SLumSem
    sems[participant]['LMS'] = LMSSem

    for n in range(5000):
        LinErr = np.mean(((everything['bootStd']['bootLMLumStd'][n])-(everything['LMLumLin'][n])), \
                                        ((everything['bootStd']['bootSLumStd'][n])-(everything['SLumLin'][n])), \
                                        ((everything['bootStd']['bootLMSStd'][n])-(everything['LMSLin'][n])))
        comparisons[participant]['LinErr'].append(LinErr)
        
        WinErr = np.mean(((everything['bootStd']['bootLMLumStd'][n])-(everything['LMLumWin'][n])), \
                                        ((everything['bootStd']['bootSLumStd'][n])-(everything['SLumWin'][n])), \
                                        ((everything['bootStd']['bootLMSStd'][n])-(everything['LMSWin'][n])))
        comparisons[participant]['WinErr'].append(WinErr)

    #Plot EVERYTHING!!
#    print subPosition
#    pylab.figure(figsize=(10,4))
#    pylab.subplot(subPosition)
#    subPosition +=1
#    width = 0.5
#    LumBar = pylab.bar(0.5, LumStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'Lum', yerr = LumSem, ecolor = 'black')
#    LMBar = pylab.bar(1.5, LMStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'LM', yerr = LMSem, ecolor = 'black')
#    SBar = pylab.bar(2.5, SStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'S', yerr = SSem, ecolor = 'black')
#
#    LMLumBar = pylab.bar(4.5, LMLumStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMLum', yerr = LMLumSem, ecolor = 'black')
#    LMLumLinBar = pylab.bar(5.5, LMLumLin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMLumLin', yerr = LMLumLinSem, ecolor = 'black', hatch = '/')
#    LMLumWinBar = pylab.bar(6.5, lmlumWin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMLumWin', yerr = lmlumWinSem, ecolor = 'black', hatch = 'x')
#
#    SLumBar = pylab.bar(8.5, SLumStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'SLum', yerr = SLumSem, ecolor = 'black')
#    SLumLinBar = pylab.bar(9.5, SLumLin, width, facecolor = '#0032ff', alpha = 0.75, label = 'SLumLin', yerr = SLumLinSem, ecolor = 'black',  hatch = '/')
#    SLumWinBar = pylab.bar(10.5, slumWin, width, facecolor = '#0032ff', alpha = 0.75, label = 'SLumWin', yerr = slumWinSem, ecolor = 'black', hatch = 'x')
#
#    LMSBar = pylab.bar(12.5, LMSStd, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMS', yerr = LMSSem, ecolor = 'black')
#    LMSLinBar = pylab.bar(13.5, LMSLin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMSLin', yerr = LMSLinSem, ecolor = 'black', hatch = '/')
#    LMSWinBar = pylab.bar(14.5, lmsWin, width, facecolor = '#0032ff', alpha = 0.75, label = 'LMSWin', yerr = lmsWinSem, ecolor = 'black', hatch = 'x')
#
#    xlabels = pylab.xticks(((np.arange(15))+width/2.0)+0.5, ('Lum', 'LM', 'S', '', 'LMLum', 'LMLum Lin', 'LMLum Win', '', \
#                             'SLum', 'SLum Lin', 'SLum Win', '', 'LMS', 'LMS Lin', 'LMS Win'), rotation = 'vertical')
#    pylab.ylim(0,0.035)
#    pylab.title(everything['Participant'])
#    pylab.tight_layout()

    #pylab.legend()
    pkl_file1.close()

Locations = [0.25, 0.5, 0.75]

pylab.subplot(121)
RJSLine1 = pylab.errorbar(Locations, [stds['RJS']['Lum'], stds['RJS']['LM'], stds['RJS']['S']], marker = 'o', color = 'k', linestyle = '-', yerr = [sems['RJS']['Lum'], sems['RJS']['LM'], sems['RJS']['S']])
DJHLine1 = pylab.errorbar(Locations, [stds['DJH']['Lum'], stds['DJH']['LM'], stds['DJH']['S']], marker = 'D', color = 'k', linestyle = '--', yerr = [sems['DJH']['Lum'], sems['DJH']['LM'], sems['DJH']['S']])
DSLine1 = pylab.errorbar(Locations, [stds['DS']['Lum'], stds['DS']['LM'], stds['DS']['S']], marker = 's', color = 'k', linestyle = ':', yerr = [sems['DS']['Lum'], sems['DS']['LM'], sems['DS']['S']])
pylab.ylim(0, 0.08)
pylab.ylabel('Standard Deviation (degrees)')
pylab.xlabel('Individual Cues')
pylab.xticks(Locations, ('Lum', 'LM', 'S'))

pylab.subplot(122)
RJSLine2 = pylab.errorbar(Locations, [stds['RJS']['LMLum'], stds['RJS']['SLum'], stds['RJS']['LMS']], marker = 'o', color = 'k', linestyle = '-', yerr = [sems['RJS']['LMLum'], sems['RJS']['SLum'], sems['RJS']['LMS']], label = 'RJS')
DJHLine2 = pylab.errorbar(Locations, [stds['DJH']['LMLum'], stds['DJH']['SLum'], stds['DJH']['LMS']], marker = 'D', color = 'k', linestyle = '--', yerr = [sems['DJH']['LMLum'], sems['DJH']['SLum'], sems['DJH']['LMS']], label = 'DJH')
DSLine2 = pylab.errorbar(Locations, [stds['DS']['LMLum'], stds['DS']['SLum'], stds['DS']['LMS']], marker = 's', color = 'k', linestyle = ':', yerr = [sems['DS']['LMLum'], sems['DS']['SLum'], sems['DS']['LMS']], label = 'DS')
pylab.ylim(0, 0.08)
pylab.xticks(Locations, ('LM + Lum', 'S + Lum', 'LM + S'))
pylab.yticks([])

pylab.xlabel('Combined Cues')

pylab.legend(frameon=False)

pylab.tight_layout()

pylab.show()