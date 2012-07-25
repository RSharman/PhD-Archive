#Plots for SynthEdgesReport - Apr 2012

import pylab
import numpy as np

#No Noise Values
RJS = [0.01781, 0.015422, 0.01502, 0.01245, 0.0141, 0.018557]
RJSerr = [0.00151*2, 0.00135*2, 0.00106*2, 0.001065*2, 0.00119*2, 0.001506*2]

CDS = [0.0199, 0.0241, 0.015966, 0.014038, 0.0294, 0.0152]
CDSerr = [0.001568*2, 0.00205*2, 0.001179*2, 0.001209*2, 0.002667*2, 0.00112*2]

DJH = [0.0174, 0.01578, 0.01355, 0.01876, 0.0192, 0.01777]
DJHerr = [0.00113*2, 0.00143*2, 0.001315*2, 0.001862*2, 0.001691*2, 0.001464*2]

#Noise Values
#RJS = [0.02162, 0.02726, 0.01957, 0.020345, 0.01695, 0.019778]
#RJSerr = [0.001937*2, 0.002406*2, 0.002319*2, 0.001381*2, 0.001728*2, 0.001254*2]
#
#CDS = [0.01577, 0.0192, 0.02257, 0.01893, 0.0199, 0.02182]
#CDSerr = [0.00212*2, 0.002089*2, 0.001885*2, 0.00149*2, 0.00178*2, 0.00184*2]
#
#DJH = [0.02038, 0.0127, 0.02227, 0.01369, 0.01873, 0.01762]
#DJHerr = [0.001753*2, 0.001463*2, 0.002045*2, 0.001554*2, 0.001465*2, 0.001525*2]

RJSLocations = np.arange(0.25, 6.0, 1.0)
CDSLocations = np.arange(0.5, 6.0, 1.0)
DJHLocations = np.arange(0.75, 6.0, 1.0)

width = 0.2

#RJSBar = pylab.bar(RJSLocations, RJS, width, facecolor = '#0032ff', alpha = 0.75, label='RJS')
#RJSBar2 = pylab.bar(RJSLocations, RJS, width, facecolor = 'none', yerr = RJSerr, ecolor='black')
#CDSBar = pylab.bar(CDSLocations, CDS, width, facecolor = '#0032ff', alpha = 0.5, label='CDS')
#CDSBar2 = pylab.bar(CDSLocations, CDS, width, facecolor = 'none', yerr = CDSerr, ecolor='black')
#DJHBar = pylab.bar(DJHLocations, DJH, width, facecolor = '#0032ff', alpha = 0.25, label='DJH')
#DJHBar2 = pylab.bar(DJHLocations, DJH, width, facecolor = 'none', yerr = DJHerr, ecolor='black')
pylab.subplot(121)
RJSLine1 = pylab.errorbar(RJSLocations[:3], RJS[:3], marker = 'o', color = 'k', linestyle = '-', label = 'RJS', yerr = RJSerr[:3])
CDSLine1 = pylab.errorbar(RJSLocations[:3], CDS[:3], marker = 'D', color = 'k', linestyle = '--', label = 'CDS', yerr = CDSerr[:3])
DJHLine1 = pylab.errorbar(RJSLocations[:3], DJH[:3], marker = 's', color = 'k', linestyle = ':', label = 'DJH', yerr = DJHerr[:3])
pylab.xticks((np.arange(3))+width, ('Lum', 'LM', 'S'))
pylab.ylabel('Beta (degrees)')
pylab.ylim(0,0.035)
pylab.xlabel('Individual Cues')

pylab.subplot(122)
RJSLine2 = pylab.errorbar(RJSLocations[:3], RJS[3:], marker = 'o', color = 'k', linestyle = '-', yerr = RJSerr[3:], label = 'RJS')
CDSLine2 = pylab.errorbar(RJSLocations[:3], CDS[3:], marker ='D', color = 'k', linestyle = '--', yerr = CDSerr[3:], label = 'CDS')
DJHLine2 = pylab.errorbar(RJSLocations[:3], DJH[3:], marker = 's', color = 'k', linestyle = ':', yerr = DJHerr[3:], label = 'DJH')
pylab.xlabel('Combined Cues')
pylab.yticks([])
#DivideLine = pylab.axvline(x = 2.7, color = 'k', linestyle = '--')

pylab.xticks((np.arange(3))+width, ('LM + Lum', 'S + Lum', 'LM + S'))
pylab.ylim(0,0.035)


#pylab.xlabel('Individual Cues', horizontalalignment = 'left')

pylab.legend(frameon=False)
pylab.tight_layout()

pylab.show()