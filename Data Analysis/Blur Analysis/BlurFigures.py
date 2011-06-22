#Creating Figures for Natural Image Blur Paper

from psychopy import data, gui, misc, core
import matplotlib
matplotlib.use('WXAgg')
import pylab, scipy, numpy, csv
import numpy as np

fontsize = 16

#Blur Data
AchromThresh = [0.844, 1.673, 0.768, 0.896, 1.46, 0.501, 0.913, 0.639, 0.519, 0.498, 0.433, 0.494, 0.489, 0.469, 0.787, 0.694, 1.442, 1.294, 2.259, 1.845]
LumThresh = [0.692, 1.723, 0.987, 0.99, 1.474, 0.69, 0.744, 0.481, 0.754, 0.564, 0.474, 0.649, 0.478, 0.49, 0.727, 0.724, 2.565, 1.87, 1.742, 1.317]
IsolumThresh = [3.372, 6.996, 5.771, 5.28, 3.758, 2.218, 8.032, 8.762, 4.554, 3.235, 6.01, 12.398, 9.921, 10.199, 3.998, 2.704, 2.974, 4.197, 8.179, 4.751]
ChromThresh = [5.872, 15.026, 8.934, 12.87, 15.998, 7.167, 17.316, 6.301, 15.78, 8.433, 4.696, 21.992, 8.346, 22.62, 7.383, 3.366, 18.804, 8.024, 26.236, 12.483]

#Blur Thresh Data
#AchromThresh = [1.558, 1.866, 1.422, 1.43, 2.302, 1.236, 1.502, 1.225, 1.623, 1.006, 0.5, 1.176, 1.091, 0.574, 1.143, 1.145, 2.37, 1.603, 2.247, 1.717]
#LumThresh = [1.346, 1.773, 2.376, 1.211, 1.999, 0.5, 1.687, 1.65, 1.522, 0.982, 1.551, 1.302, 1.548, 0.397, 2.116, 1.46, 2.133, 2.664, 2.497, 1.925]
#IsolumThresh = [9.585, 8.809, 8.018, 9.533, 3.548, 15.828, 5.344, 5.008, 4.697, 2.09, 6.736, 3.824, 5.652, 8.19, 4.764, 10.434, 10.215]
#ChromThresh = [9.452, 14.649, 17.204, 26.914, 6.042, 18.273, 16.853, 29.014, 4.083, 7.373, 11.185, 4.937, 17.609, 19.124]
#
#AchromMean = np.mean(AchromThresh)
#LumMean = np.mean(LumThresh)
#IsolumMean = np.mean(IsolumThresh)
#ChromMean = np.mean(ChromThresh)
#
#print 'Achrom mean', AchromMean
#print 'Lum mean', LumMean
#print 'Isolum mean', IsolumMean
#print 'Chrom mean', ChromMean
#
#AchromStd = np.std(AchromThresh)
#LumStd = np.std(LumThresh)
#IsolumStd = np.std(IsolumThresh)
#ChromStd = np.std(ChromThresh)
#
#AchromSEM = AchromStd/np.sqrt(len(AchromThresh))
#LumSEM = LumStd/np.sqrt(len(LumThresh))
#IsolumSEM = IsolumStd/np.sqrt(len(IsolumThresh))
#ChromSEM = ChromStd/np.sqrt(len(ChromThresh))
#
#print 'Achrom', AchromSEM, 'Lum', LumSEM, 'Isolum', IsolumSEM, 'Chrom', ChromSEM

conditions = [1, 2, 3, 4]
labels = ["Luminance Blur", "Chromatic Blur"]

#Blur Data
#loneMeans = [0.94585, 5.86545]
#comboMeans = [1.00675, 12.38235]
#loneStandardErrors = [0.116250102688, 0.625416974806]
#comboStandardErrors = [0.12711785624, 1.43284851131]

#Blur Thresh Data
loneMeans = [1.4368, 7.1926]
comboMeans = [1.6320, 14.4794]
loneStandardErrors = [0.11036, 0.79632]
comboStandardErrors = [0.12988, 1.99703]

pylab.figure(1, (11,8))
xLoneLocations = [0.5, 2.0]
xComboLocations = [1.0, 2.5]
xwidth = 0.5
#xlocations = np.array(range(len(means)))+0.5
ticks = [1.0, 2.5]
yticks = [5.0, 10.0, 15.0, 20.0]

lone = pylab.bar(xLoneLocations, loneMeans, facecolor = '#0032ff', facealpha = 0.2, edgecolor = 'Black', width = xwidth, bottom =0, yerr=loneStandardErrors, ecolor = 'Black')
combo = pylab.bar(xComboLocations, comboMeans, facecolor = '#0132fa', facealpha = 0.82, width = xwidth, bottom =0, yerr=comboStandardErrors, ecolor = 'Black')
pylab.xlim([0, 3.5])
pylab.xticks(ticks, labels)
pylab.yticks(yticks, yticks)
pylab.xlabel('Conditions', fontsize = fontsize)
pylab.ylabel('Blur Discrimination Threshold (Degrees)', fontsize = fontsize)
pylab.gca().get_xaxis().tick_bottom()
pylab.gca().get_yaxis().tick_left()

ax3 = pylab.gca()
for tick in ax3.xaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)
for tick in ax3.yaxis.get_major_ticks():
    tick.label1.set_fontsize(fontsize)

pylab.legend((lone[0], combo[0]), ('Alone', 'Combined'), loc='upper left')
leg = pylab.gca().get_legend()
ltext = leg.get_texts()

pylab.setp(ltext, fontsize=fontsize)

pylab.show()

