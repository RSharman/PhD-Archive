from psychopy import misc, data, gui, core
import pylab, scipy
import numpy as np

#Import file to analyse
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

counter = 0
pylab.figure(figsize=(12,10))

for thisFileName in files:
    dat=misc.fromFile(thisFileName)

    conditions = dat.trialList

    #Create some lists to store intermediate variables
    meanResps = []
    Trials = []
    modMeanResps = []
    modTrials = []

    #Number and divided up the conditions
    for condN, condition in enumerate(conditions):
    #    print condition, dat.data['response'][condN], numpy.mean(dat.data['response'][condN])
        
        #Create a variable which stores the responses divided up by condition
        Resps = dat.data['response'][condN]
        #Take the mean of the responses for each condition
        meanResps.append(np.mean(dat.data['response'][condN]))
        
        #Separate the trial details from their key
        for cond, condN in condition.iteritems():
            Trials.append(condN)

    #As the data file has 0.95-1.05, the correct answer is different for two halves of the trial list, this corrects that
    for RespN, Resp in enumerate(meanResps):
        if RespN<=5:
            modResp = Resp
            modMeanResps.append(modResp)
        if RespN>5:
            modResp = 1-Resp
            modMeanResps.append(modResp)
    
    observer = str(thisFileName[-21])+str(thisFileName[-20])+str(thisFileName[-19])
    print observer

    #Create a list of all the condition types
    if observer=='001': 
        print '*******************'
        modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]
        range=0.05
        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
        collapsedResps.append(modMeanResps[5])

    elif observer=='002': 
        print '*******************'
        modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]
        range=0.05
        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
        collapsedResps.append(modMeanResps[5])
        
    elif observer=='003': 
        print '*******************'
        modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]
        range=0.05
        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
        collapsedResps.append(modMeanResps[5])
        
    elif observer=='004': 
        print '*******************'
        modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]
        range=0.05
        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
        collapsedResps.append(modMeanResps[5])

    elif observer=='005': 
        print '*******************'
        modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]
        range=0.05
        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
        collapsedResps.append(modMeanResps[5])
        
    elif observer=='006': 
        print '*******************'
        modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]
        range=0.05
        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
        collapsedResps.append(modMeanResps[5])
        
    else:#if observer!=('001' or '002' or '003' or '004' or '005' or '006'):
        range=0.1
        print '22222222222222'
        modTrials = [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]

        #Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
        collapsedResps = []
        collapsedResps.append((modMeanResps[0]+modMeanResps[19])/2)
        collapsedResps.append((modMeanResps[1]+modMeanResps[18])/2)
        collapsedResps.append((modMeanResps[2]+modMeanResps[17])/2)
        collapsedResps.append((modMeanResps[3]+modMeanResps[16])/2)
        collapsedResps.append((modMeanResps[4]+modMeanResps[15])/2)
        collapsedResps.append((modMeanResps[5]+modMeanResps[14])/2)
        collapsedResps.append((modMeanResps[6]+modMeanResps[13])/2)
        collapsedResps.append((modMeanResps[7]+modMeanResps[12])/2)
        collapsedResps.append((modMeanResps[8]+modMeanResps[11])/2)
        collapsedResps.append((modMeanResps[9]+modMeanResps[10])/2)

    #print modTrials
            
    #Create the fit for the collapsed data
    fit = data.FitWeibull(modTrials, collapsedResps, expectedMin=0.5)
    smoothInt = pylab.arange(min(modTrials), max(modTrials), 0.001)
    smoothResp = fit.eval(smoothInt)
    thresh = fit.inverse(0.80)

    print 'Threshold', thresh
    
    counter+=1

    print 'observer', observer, 'last point', collapsedResps[0]

    label = observer, 'Threshold', ("%.2f" %thresh), 'lastpoint', '%.1f' %collapsedResps[0]
    
    pylab.subplot(3, 2, counter)
    
    pylab.title(label)
    pylab.plot([0.5, 0], [0.5, 0.5], 'k--')
    pylab.plot(modTrials, collapsedResps, 'o-')
    pylab.plot(smoothInt, smoothResp, '-')

    
    pylab.xlim(0, 0.1)
    pylab.ylim(0,1)

pylab.show()

