#Creating Figures for Natural Image Blur Paper

from psychopy import data, gui, misc, core
import matplotlib
#matplotlib.use('WXAgg')
import pylab, scipy, numpy, csv
import numpy as np

fontsize = 30

#Reverse Data
#AchromThresh = [0.75, 1.167, 0.917, 1.0, 1.0, 0.667, 1.167, 0.833, 1.167,1.167,1.167,1,1.333,1.917,1.083,1.333,5.083,6.167,3.75,3.083,3.667,3.167,1.583,2.333, 2.583,2.25,1.417,2.75,3.5,2.417,1.917,0.917,2.417,1.75,2.583,1.75,2.917,2.75,2.083,1.333,2.417,2.0,1.417,2.5,3.5,2.083,1.5,1.833,2.083,1.667,1.583,1.617,2.167,1.917,2.333,6.75,3.667,1.0,1.833,1.417,1.583,1.083,1.5,1.0,1.917,1.083,1.333,1.333,1.667,1.583,1.583,0.917,4.083,2.75,2.917,2.583,2.583,3.167,3.0,4.167]
#LumThresh = [0.417,1.0,1.5,1.0,0.583,0.833,1.0,0.75,1.5,1.75,0.833,1.25,2.75,3.75,1.75,12.0,8.167,11.333,3.583,27.25,5.333,4.833,4.5,5.583,3.167,2.75,2.0,13.333,5.833,2.5,2.083,1.833,3.083,6.833,1.333,2.667,2.0,3.167,1.75,1.833,2.417,1.25,1.5,5.333,3.05,2.333,4.583,2.167,1.583,2.25,1.917,2.667,2.833,2.833,1.583,1.917,1.75,1.667,1.583,1.667,2.5,2.25,1.25,2.167,1.333,1.75,1.667,1.5,1.5,1.5,1.167,8.667,1.833,2.75,2.083,29.833,4.25,3.167,2.917]
#IsolumThresh = [2.5,1.5,1.167,1.917,1.917,0.833,1.25,3.083,4.25,1.333,0.833,2.5,4.417,3.0,2.5,5.833,5.167,4.833,4.75,6.667,2.667,4.167,1.167,3.917,2.833,2.75,2.917,3.25,5.583,10.0,3.833,6.833,4.167,2.5,2.667,3.917,4.333,2.333,2.333,4.0,3.083,1.417,2.167,2.083,2.5,3.083,1.25,4.0,1.917,2.417,2.333,3.5,2.583,3.75,2.25,4.083,1.417,0.917,1.417,3.5,2.083,1.833,1.5,3.333,1.583,1.67,0.833,2.25,2.583,3.0,6.417,5.25,6.083,2.917,4.5,3.167,3.5,1.917,7.833]
#ChromThresh = [9.833,2.167,1.167,13.0,10.417,4.75,2.083,18.917,7.083,3.667,17.2,26.333,9.75,11.5,15.333,61.667,32.833,29.5,23.167,12.167,5.0,28.333,46.833,8.5,50.167,38.667,13.25,12.083,51.5,11.417,30.667,5.75,27.75,48.25,21.333,25.167,31.25,69.833,62.0,7.833,53.667,63.0,16.5,20.167,11.25,15.0,32.083,22.8,50.4,30.4,12.583,11.417,30.5,58.333,28.25,8.167,7.333,23.333,15.0,4.833,11.75,16.833,27.083,12.333,1.333,26.333,14.75,5.75,1.75,18.0,34.333,20.167,12.667,48.917,28.0,13.167,33.833,43.0]
#ChromThresh = [9.833,2.167,1.167,13.0,10.417,4.75,2.083,18.917,7.083,3.667,9.75,11.5,15.333,23.167,12.167,5.0,8.5,13.25,12.083,11.417,30.667,5.75,27.75,48.25,21.333,25.167,11.25,15.0,12.583,11.417,28.25,8.167,7.333,15.0,4.833,11.75,16.833,27.083,12.333,1.333,14.75,5.75,1.75,34.333,20.167,12.667,28.0,13.167,33.833]

#Blur Data
#AchromThresh = [0.844, 1.673, 0.768, 0.896, 1.46, 0.501, 0.913, 0.639, 0.519, 0.498, 0.433, 0.494, 0.489, 0.469, 0.787, 0.694, 1.442, 1.294, 2.259, 1.845]
#LumThresh = [0.692, 1.723, 0.987, 0.99, 1.474, 0.69, 0.744, 0.481, 0.754, 0.564, 0.474, 0.649, 0.478, 0.49, 0.727, 0.724, 2.565, 1.87, 1.742, 1.317]
#IsolumThresh = [3.372, 6.996, 5.771, 5.28, 3.758, 2.218, 8.032, 8.762, 4.554, 3.235, 6.01, 12.398, 9.921, 10.199, 3.998, 2.704, 2.974, 4.197, 8.179, 4.751]
#ChromThresh = [5.872, 15.026, 8.934, 12.87, 15.998, 7.167, 17.316, 6.301, 15.78, 8.433, 4.696, 21.992, 8.346, 22.62, 7.383, 3.366, 18.804, 8.024, 26.236, 12.483]

#Blur Thresh Data
AchromThresh = [1.558, 1.866, 1.422, 1.43, 2.302, 1.236, 1.502, 1.225, 1.623, 1.006, 0.5, 1.176, 1.091, 0.574, 1.143, 1.145, 2.37, 1.603, 2.247, 1.717]
LumThresh = [1.346, 1.773, 2.376, 1.211, 1.999, 0.5, 1.687, 1.65, 1.522, 0.982, 1.551, 1.302, 1.548, 0.397, 2.116, 1.46, 2.133, 2.664, 2.497, 1.925]
IsolumThresh = [9.585, 20.499, 8.809, 8.018, 9.533, 3.548, 15.828, 5.344, 5.008, 4.697, 2.09, 6.736, 3.824, 5.652, 8.19, 4.764, 25.218, 22.922, 10.434, 10.215]
ChromThresh = [9.452, 14.649, 17.204, 26.914, 6.042, 18.273, 7.338, 16.853, 29.014, 4.083, 7.373, 11.862, 11.185, 4.937, 27.654, 11.477, 17.609, 19.124]
#
AchromMean = np.mean(AchromThresh)
LumMean = np.mean(LumThresh)
IsolumMean = np.mean(IsolumThresh)
ChromMean = np.mean(ChromThresh)

print 'Achrom mean', AchromMean
print 'Lum mean', LumMean
print 'Isolum mean', IsolumMean
print 'Chrom mean', ChromMean
#
AchromStd = np.std(AchromThresh)
LumStd = np.std(LumThresh)
IsolumStd = np.std(IsolumThresh)
ChromStd = np.std(ChromThresh)
#
AchromSEM = AchromStd/np.sqrt(len(AchromThresh))
LumSEM = LumStd/np.sqrt(len(LumThresh))
IsolumSEM = IsolumStd/np.sqrt(len(IsolumThresh))
ChromSEM = ChromStd/np.sqrt(len(ChromThresh))
#
print 'Achrom', AchromSEM, 'Lum', LumSEM, 'Isolum', IsolumSEM, 'Chrom', ChromSEM

conditions = [1, 2, 3, 4]
labels = ["Luminance Blur", "Chromatic Blur"]

#Reverse Data
#loneMeans = [2.11189, 3.1435]
#achromMean = 2.11189
#isolumMean = 3.1435
#comboMeans = [3.54911, 22.98888]
#comboMeans = [3.54911, 14.3214]
#lumMean = 3.54911
#chromMean = 14.3214
#loneStandardErrors = [0.128524, 0.19252598]
#achromSE = 0.128524
#isolumSE = 0.19252598
#comboStandardErrors = [0.53034, 1.9238446]
#comboStandardErrors = [0.53034, 1.42164]
#lumSE = 0.53034
#chromSE = 1.42164

#Blur Data
#loneMeans = [0.94585, 5.86545]
#comboMeans = [1.00675, 12.38235]
#loneStandardErrors = [0.116250102688, 0.625416974806]
#comboStandardErrors = [0.12711785624, 1.43284851131]

#Blur Thresh Data
loneMeans = [1.4368, 9.5457]
achromMean = 1.4368
isolumMean = 9.5457
comboMeans = [1.6320, 14.5024]
lumMean = 1.6320
chromMean = 14.5024

loneStandardErrors = [0.11036, 1.4335]
achromSE = 0.11036
isolumSE = 1.4335
comboStandardErrors = [0.12988, 1.7761]
lumSE = 0.12988
chromSE = 1.7761

pylab.figure(1, (11,8))
xLoneLocations = [0.5, 2.0]
xAchromLocation = 0.5
xIsolumLocation = 2.0
xComboLocations = [1.0, 2.5]
xLumLocation = 1.0
xChromLocation = 2.5
xwidth = 0.5
#xlocations = np.array(range(len(means)))+0.5
ticks = [1.0, 2.5]
yticks = [5.0, 10.0, 15.0, 20.0]

#lone = pylab.bar(xLoneLocations, loneMeans, facecolor = '#0032ff', facealpha = 0.2, edgecolor = 'Black', width = xwidth, bottom =0, yerr=loneStandardErrors, ecolor = 'Black')
#lone = pylab.bar(xLoneLocations, loneMeans, facecolor = '#DCDCDC', edgecolor = 'Black', width = xwidth, bottom =0, yerr=loneStandardErrors, ecolor = 'Black')
#combo = pylab.bar(xComboLocations, comboMeans, facecolor = '#7F7F7F', width = xwidth, bottom =0, yerr=comboStandardErrors, ecolor = 'Black', hatch='/')

achromBar = pylab.bar(xAchromLocation, achromMean, facecolor = '#DCDCDC', edgecolor = 'Black', width = xwidth, bottom =0, yerr=achromSE, ecolor = 'Black', label = 'Alone')
isolumBar = pylab.bar(xIsolumLocation, isolumMean, facecolor = '#DCDCDC', edgecolor = 'Black', width = xwidth, bottom =0, yerr=isolumSE, ecolor = 'Black', hatch = '/')

lumBar = pylab.bar(xLumLocation, lumMean, facecolor = '#7F7F7F', edgecolor = 'Black', width = xwidth, bottom =0, yerr=lumSE, ecolor = 'Black', label = 'Combined')
chromBar = pylab.bar(xChromLocation, chromMean, facecolor = '#7F7F7F', edgecolor = 'Black', width = xwidth, bottom =0, yerr=chromSE, ecolor = 'Black', hatch = '/')

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

pylab.legend(loc = 'upper left')

#pylab.legend((lone[0], combo[0]), ('Alone', 'Combined'), loc='upper left')
leg = pylab.gca().get_legend()
ltext = leg.get_texts()

pylab.setp(ltext, fontsize=fontsize)

pylab.show()

