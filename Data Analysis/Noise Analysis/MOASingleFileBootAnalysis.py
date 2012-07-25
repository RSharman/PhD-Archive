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
    width = 0.5
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

pylab.xlabel('Condition')
pylab.ylabel('Standard Deviation (degrees)')

RJSLinErr = np.std(comparisons['RJS']['LinErr'])
RJSWinErr = np.std(comparisons['RJS']['WinErr'])
DJHLinErr = np.std(comparisons['DJH']['LinErr'])
DJHWinErr = np.std(comparisons['DJH']['WinErr'])
DSLinErr = np.std(comparisons['DS']['LinErr'])
DSWinErr = np.std(comparisons['DS']['WinErr'])


comparisons['All'] = {}
comparisons['All']['Lin'] = np.mean(comparisons['RJS']['Lin'], comparisons['DJH']['Lin'], comparisons['DS']['Lin'])
AllLin = comparisons['All']['Lin']
AllLinErr = np.std(comparisons['RJS']['LinErr'] + comparisons['DJH']['LinErr'] + comparisons['DS']['LinErr'])
comparisons['All'] = {}
comparisons['All']['Win'] = np.mean(comparisons['RJS']['Win'], comparisons['DJH']['Win'], comparisons['DS']['Win'])
AllWinErr = np.std(comparisons['RJS']['WinErr'] + comparisons['DJH']['WinErr'] + comparisons['DS']['WinErr'])


#pylab.subplot(223)
#RJSCompLin = pylab.bar(1.5, comparisons['RJS']['Lin'], width, facecolor = '#0032ff', alpha = 0.75, label = 'MLE')
#RJSCompLin2 = pylab.bar(1.5, comparisons['RJS']['Lin'], width, facecolor = 'none', yerr = (RJSLinErr*1.96), ecolor = 'black')
RJSCompLin2 = pylab.bar(1.5, (comparisons['RJS']['Lin'])*-1, width, facecolor = 'dimgrey', yerr = (RJSLinErr*1.96), ecolor = 'black', label = 'MLE')
#RJSCompWin = pylab.bar(2.5, comparisons['RJS']['Win'], width, facecolor = '#0032ff', alpha = 0.25, label = 'Winner Takes All')
#RJSCompWin2 = pylab.bar(2.5, comparisons['RJS']['Win'], width, facecolor = 'none', yerr = (RJSWinErr*1.96), ecolor = 'black')
RJSCompWin2 = pylab.bar(2.5, (comparisons['RJS']['Win'])*-1, width, facecolor = 'gainsboro', yerr = (RJSWinErr*1.96), ecolor = 'black', label = 'Winner Takes All')
#DJHCompLin = pylab.bar(4.5, comparisons['DJH']['Lin'], width, facecolor = '#0032ff', alpha = 0.75)
#DJHCompLin2 = pylab.bar(4.5, comparisons['DJH']['Lin'], width, facecolor = 'none', yerr = (DJHLinErr*1.96), ecolor = 'black')
DJHCompLin2 = pylab.bar(4.5, (comparisons['DJH']['Lin'])*-1, width, facecolor = 'dimgrey', yerr = (DJHLinErr*1.96), ecolor = 'black')
#DJHCompWin = pylab.bar(5.5, comparisons['DJH']['Win'], width, facecolor = '#0032ff', alpha = 0.25)
#DJHCompWin2 = pylab.bar(5.5, comparisons['DJH']['Win'], width, facecolor = 'none', yerr = (DJHWinErr*1.96), ecolor = 'black')
DJHCompWin2 = pylab.bar(5.5, (comparisons['DJH']['Win'])*-1, width, facecolor = 'gainsboro', yerr = (DJHWinErr*1.96), ecolor = 'black')
#DSCompLin = pylab.bar(7.5, comparisons['DS']['Lin'], width, facecolor = '#0032ff', alpha = 0.75)
#DSCompLin2 = pylab.bar(7.5, comparisons['DS']['Lin'], width, facecolor = 'none', yerr = (DSLinErr*1.96), ecolor = 'black')
DSCompLin2 = pylab.bar(7.5, comparisons['DS']['Lin']*-1, width, facecolor = 'dimgrey', yerr = (DSLinErr*1.96), ecolor = 'black')
#DSCompWin = pylab.bar(8.5, comparisons['DS']['Win'], width, facecolor = '#0032ff', alpha = 0.25)
#DSCompWin2 = pylab.bar(8.5, comparisons['DS']['Win'], width, facecolor = 'none', yerr = (DSWinErr*1.96), ecolor = 'black')
DSCompWin2 = pylab.bar(8.5, comparisons['DS']['Win']*-1, width, facecolor = 'gainsboro', yerr = (DSWinErr*1.96), ecolor = 'black')
#AllCompLin = pylab.bar(10.5, AllLin, width, facecolor = '#0032ff', alpha = 0.75)
#AllCompLin2 = pylab.bar(10.5, AllLin, width, facecolor = 'none', yerr = (AllLinErr*1.96), ecolor = 'black')
AllCompLin2 = pylab.bar(10.5, AllLin*-1, width, facecolor = 'dimgrey', yerr = (AllLinErr*1.96), ecolor = 'black')
#AllCompWin = pylab.bar(11.5, comparisons['All']['Win'], width, facecolor = '#0032ff', alpha = 0.25)
#AllCompWin2 = pylab.bar(11.5, comparisons['All']['Win'], width, facecolor = 'none', yerr = (AllWinErr*1.96), ecolor = 'black')
AllCompWin2 = pylab.bar(11.5, comparisons['All']['Win']*-1, width, facecolor = 'gainsboro', yerr = (AllWinErr*1.96), ecolor = 'black')

print comparisons['RJS']['Lin'], comparisons['RJS']['Win']
print comparisons['DJH']['Lin'], comparisons['DJH']['Win']
print comparisons['DS']['Lin'], comparisons['DS']['Win']
xlabels = pylab.xticks(((np.arange(12))+width*3.0)+0.75, ('RJS', '', '', 'DJH', '', '', 'DS', '', '', 'All', ''))
pylab.xlim(0.5, 13.0)
pylab.ylim(-0.015, 0.010)
pylab.ylabel('Difference between predicted and observed variance (degrees)')
pylab.xlabel('Participants')
pylab.legend(frameon=False)
pylab.tight_layout()

pylab.show()