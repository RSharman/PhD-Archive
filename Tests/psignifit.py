#Using psignifit for bootstrapping - Aug 2011

from psychopy import data, gui, misc, core
import pypsignifit as psi
import numpy as np
import matplotlib

files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses, extraInfo, positions, reversalIntensities = [],[],[],[],[]
for thisFileName in files:
    thisDat = misc.fromFile(thisFileName)
    assert isinstance(thisDat, data.StairHandler)
    allIntensities.append( thisDat.intensities)
    allResponses.append( thisDat.data)
    extraInfo.append(thisDat.extraInfo)
    reversalIntensities.append(thisDat.reversalIntensities)
    
channels = []

for n in range(len(extraInfo)):
    temp = extraInfo[n]
    positions.append(temp['lumEdgePos'])
    channels.append(temp['Channel'])
    
newIntensities=[]
for n in range(len(allIntensities)):
    allIntensities[n]=np.array(allIntensities[n])
    allIntensities[n]-=positions[n]
    reversalIntensities[n]=np.array(reversalIntensities[n])
    reversalIntensities[n]-=positions[n]
    
combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(allIntensities, allResponses, bins = 'unique')
             
#for n in range(len(combinedInten)):
#    combinedInten[n]+=10

data = np.c_[combinedInten, combinedResp, combinedN]

nafc = 1
#Not sure if these settings are right
constraints = ('unconstrained', 'unconstrained', 'unconstrained', 'Beta(2,20)')
#constraints={'guess':'Uniform(0.01, 1.0)', 'lapse':'Beta(2,20)', 'a':'unconstrained', 'b':'unconstrained'}

boots = psi.BootstrapInference(data, core='mw0.25', sigmoid='logistic', priors=constraints, nafc=1)
#boots = psi.BootstrapInference(data, core='weibull', sigmoid='gumbel_l', priors=constraints, nafc=nafc)
#
#print boots.estimate
#print 'pse', boots.getThres(0.5)
#print 'slope', boots.getSlope()
#print 'jnd', (boots.getThres(0.75)-boots.getThres(0.25))
#
#print boots.deviance
#
boots.sample(5000)
#
print 'pse', boots.getThres(0.5)
print 'slope', boots.getSlope()
print 'jnd', (boots.getThres(0.75)-boots.getThres(0.25))
#
#psi.GoodnessOfFit(boots)
#psi.show()
#
print 'thresh ci', boots.getCI(0.5)
print 'slope ci', boots.getCI(0.5, thres_or_slope = 'slope')
#
#print 'ests', boots.mcestimates

#psi.ThresholdPlot(boots)
#
#psi.plotSensitivity(boots)
#
#print boots.getCI(0.5)

#psi.ParameterPlot(boots)

#psi.show()

#
#bayes = psi.BayesInference(data, priors=constraints, nafc=nafc)
#print bayes.estimate
#print bayes.deviance

