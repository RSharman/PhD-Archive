from psychopy import misc, data, gui, core
import pylab, scipy
import numpy as np

#Import file to analyse - currently only capable of analysing one file at a time.

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

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

#Create a list of all the condition types
modTrials = [0.05, 0.04, 0.03, 0.02, 0.01, 0]

#Collapse the two halves of together i.e. take the average accuracy for 1.05 and 0.95 and so on.
collapsedResps = []
collapsedResps.append((modMeanResps[0]+modMeanResps[10])/2)
collapsedResps.append((modMeanResps[1]+modMeanResps[9])/2)
collapsedResps.append((modMeanResps[2]+modMeanResps[8])/2)
collapsedResps.append((modMeanResps[3]+modMeanResps[7])/2)
collapsedResps.append((modMeanResps[4]+modMeanResps[6])/2)
collapsedResps.append(modMeanResps[5])

#print modTrials
#print collapsedResps

        
#Create the fit for the collapsed data
fit = data.FitWeibull(modTrials, collapsedResps, guess=[0.5,1.0], expectedMin=0.5)
smoothInt = pylab.arange(min(modTrials), max(modTrials), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.80)

print 'Threshold', thresh

pylab.plot(modTrials, collapsedResps, 'o-')
pylab.plot(smoothInt, smoothResp, '-')
pylab.xlim(0, 0.05)
pylab.ylim(0.5,1)
pylab.show()

