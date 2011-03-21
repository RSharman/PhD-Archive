#Creating Figures for Natural Image Blur Paper

from psychopy import data, gui, misc, core
import matplotlib
matplotlib.use('WXAgg')
import pylab, scipy, numpy
import numpy as np

conditions = [1, 2, 3, 4]
labels = ["Luminance Blur", "Chromatic Blur"]
loneMeans = [1.4368, 7.1926]
comboMeans = [1.6320, 14.4794]
loneStandardErrors = [0.1123, 0.82084]
comboStandardErrors = [0.13326, 2.07242]

xLoneLocations = [0.5, 2.0]
xComboLocations = [1.0, 2.5]
xwidth = 0.5
#xlocations = np.array(range(len(means)))+0.5
ticks = [1.0, 2.5]
yticks = [5.0, 10.0, 15.0, 20.0]

lone = pylab.bar(xLoneLocations, loneMeans, color = 'LightSkyBlue', width = xwidth, bottom =0, yerr=loneStandardErrors, ecolor = 'Black')
combo = pylab.bar(xComboLocations, comboMeans, color = 'RoyalBlue', width = xwidth, bottom =0, yerr=comboStandardErrors, ecolor = 'Black')
pylab.xlim([0, 3.5])
pylab.xticks(ticks, labels)
pylab.yticks(yticks, yticks)
pylab.xlabel('Conditions')
pylab.ylabel('Blur Discrimination Threshold (Degrees)')
pylab.gca().get_xaxis().tick_bottom()
pylab.gca().get_yaxis().tick_left()

pylab.legend((lone[0], combo[0]), ('Alone', 'Combined'), loc='upper left')


pylab.show()

