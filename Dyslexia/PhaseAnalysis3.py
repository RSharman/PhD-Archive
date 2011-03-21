#Data Analysis of Phase Discrimination Test - January 2011
from psychopy import misc, data, gui, core
import numpy, pylab, scipy
import numpy as np

#Import files to analyse - does not combine data from the files but plots them individually.
#

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

counter = 0
pylab.figure(figsize=(12,10))

for thisFileName in files:
    dat=misc.fromFile(thisFileName)
    #
    conditions = dat.trialList
    
    #Create some lists to store intermediate variables
    meanResps = []
    Trials = []
    modMeanResps = []

    #Number and divide up the conditions
    for condN, condition in enumerate(conditions):
        #Create a variable which stores the responses divided up by condition
        Resps = dat.data['response'][condN]
        #Take the mean of the responses for each condition
        meanResps.append(np.mean(dat.data['response'][condN]))
        #Separate the trial details from their key
        for cond, condN in condition.iteritems():
            Trials.append(condN)
           
    #As the trials are half negative numbers, the correct answer is different for two halves of the trial list, this corrects that
    for RespN, Resp in enumerate(meanResps):
        if RespN<=8:
            modResp = Resp
            modMeanResps.append(modResp)
        if RespN>8:
            modResp = 1-Resp
            modMeanResps.append(modResp)

    #Create a list of all the condition types
    modTrials = [5, 10, 15, 20, 25, 30, 35, 40, 45]

    #Collapse the two halves of together i.e. take the average accuracy for 45 and -45 and so on.
    collapsedResps = []
    collapsedResps.append((modMeanResps[0]+modMeanResps[9])/2)
    collapsedResps.append((modMeanResps[1]+modMeanResps[10])/2)
    collapsedResps.append((modMeanResps[2]+modMeanResps[11])/2)
    collapsedResps.append((modMeanResps[3]+modMeanResps[12])/2)
    collapsedResps.append((modMeanResps[4]+modMeanResps[13])/2)
    collapsedResps.append((modMeanResps[5]+modMeanResps[14])/2)
    collapsedResps.append((modMeanResps[6]+modMeanResps[15])/2)
    collapsedResps.append((modMeanResps[7]+modMeanResps[16])/2)
    collapsedResps.append((modMeanResps[8]+modMeanResps[17])/2)

    #Create the fit
    fit = data.FitWeibull(modTrials, collapsedResps, expectedMin = 0.5)
    smoothInt = pylab.arange(min(Trials), max(Trials), 0.001)
    smoothResp = fit.eval(smoothInt)
    thresh = fit.inverse(0.80)

    print 'Threshold', thresh
    
    counter+=1
    
#    height = counter/2
#    if height==0:
#        height=1
#    width = counter/height
#    

    observer = str(thisFileName[-21])+str(thisFileName[-20])+str(thisFileName[-19])
    
    print 'observer', observer, 'last point', collapsedResps[8]
    
    label = observer, 'Threshold', ("%.2f" %thresh), 'lastpoint', '%.1f' %collapsedResps[0]
    
    
    pylab.subplot(3, 2, counter)

    pylab.title(label)
    pylab.plot([0.5, thresh], [0.5,0.5], 'k--')
    pylab.plot(modTrials, collapsedResps, 'o-')
    pylab.plot(smoothInt, smoothResp, '-')
    
    pylab.ylim(0,1)
    pylab.xlim(0, 50)
#pylab.legend(loc='upper left')

pylab.show()