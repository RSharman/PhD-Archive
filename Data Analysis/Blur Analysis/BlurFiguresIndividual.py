#Creating Figures for Natural Image Blur Paper

from psychopy import data, gui, misc, core
import matplotlib
matplotlib.use('WXAgg')
import pylab, scipy, numpy, csv
import numpy as np

fontsize = 16

#Blur Data
#AchromThresh = [0.844, 1.673, 0.768, 0.896, 1.46, 0.501, 0.913, 0.639, 0.519, 0.498, 0.433, 0.494, 0.489, 0.469, 0.787, 0.694, 1.442, 1.294, 2.259, 1.845]
#LumThresh = [0.692, 1.723, 0.987, 0.99, 1.474, 0.69, 0.744, 0.481, 0.754, 0.564, 0.474, 0.649, 0.478, 0.49, 0.727, 0.724, 2.565, 1.87, 1.742, 1.317]
#IsolumThresh = [3.372, 6.996, 5.771, 5.28, 3.758, 2.218, 8.032, 8.762, 4.554, 3.235, 6.01, 12.398, 9.921, 10.199, 3.998, 2.704, 2.974, 4.197, 8.179, 4.751]
#ChromThresh = [5.872, 15.026, 8.934, 12.87, 15.998, 7.167, 17.316, 6.301, 15.78, 8.433, 4.696, 21.992, 8.346, 22.62, 7.383, 3.366, 18.804, 8.024, 26.236, 12.483]
#
#Blur Thresh Data
#AchromThresh = [1.558, 1.866, 1.422, 1.43, 2.302, 1.236, 1.502, 1.225, 1.623, 1.006, 0.5, 1.176, 1.091, 0.574, 1.143, 1.145, 2.37, 1.603, 2.247, 1.717]
#LumThresh = [1.346, 1.773, 2.376, 1.211, 1.999, 0.5, 1.687, 1.65, 1.522, 0.982, 1.551, 1.302, 1.548, 0.397, 2.116, 1.46, 2.133, 2.664, 2.497, 1.925]
#IsolumThresh = [9.585, 8.809, 8.018, 9.533, 3.548, 15.828, 5.344, 5.008, 4.697, 2.09, 6.736, 3.824, 5.652, 8.19, 4.764, 10.434, 10.215]
#ChromThresh = [9.452, 14.649, 17.204, 26.914, 6.042, 18.273, 16.853, 29.014, 4.083, 7.373, 11.185, 4.937, 17.609, 19.124]
#
#Blur Data
#AchromRJS = [0.844, 0.501, 0.433, 0.694]
#LumRJS = [0.692, 0.69, 0.474, 0.724]
#IsolumRJS = [3.372, 2.218, 6.01, 2.704]
#ChromRJS = [5.872, 7.167, 4.696, 3.366]
#
#AchromSH = [1.673, 0.913, 0.494, 1.442]
#LumSH = [1.723, 0.744, 0.649, 2.565]
#IsolumSH = [6.996, 8.032, 12.398, 2.974]
#ChromSH = [15.026, 17.316, 21.992, 18.804]
#
#AchromAP = [0.768, 0.639, 0.489, 1.294]
#LumAP = [0.987, 0.481, 0.478, 1.87]
#IsolumAP = [5.771, 8.762, 9.921, 4.197]
#ChromAP = [8.934, 6.301, 8.346, 8.024]
#
#AchromKB = [0.896, 0.519, 0.469, 2.259]
#LumKB = [0.99, 0.754, 0.49, 1.742]
#IsolumKB = [5.28, 4.554, 10.199, 8.179]
#ChromKB = [12.87, 15.78, 22.62, 26.236]
#
#AchromDJH = [1.46, 0.498, 0.787, 1.845]
#LumDJH = [1.474, 0.564, 0.727, 1.317]
#IsolumDJH = [3.758, 3.235, 3.998, 4.751]
#ChromDJH = [15.998, 8.433, 7.383, 12.483]
#
#AchromMeanDJH = np.mean(AchromDJH)
#LumMeanDJH = np.mean(LumDJH)
#IsolumMeanDJH = np.mean(IsolumDJH)
#ChromMeanDJH = np.mean(ChromDJH)
#
#print 'DJH Achrom mean', AchromMeanDJH
#print 'DJH Lum mean', LumMeanDJH
#print 'DJH Isolum mean', IsolumMeanDJH
#print 'DJH Chrom mean', ChromMeanDJH
#
#AchromStdDJH = np.std(AchromDJH)
#LumStdDJH = np.std(LumDJH)
#IsolumStdDJH = np.std(IsolumDJH)
#ChromStdDJH = np.std(ChromDJH)
#
#AchromSEMDJH = AchromStdDJH/np.sqrt(len(AchromDJH))
#LumSEMDJH = LumStdDJH/np.sqrt(len(LumDJH))
#IsolumSEMDJH = IsolumStdDJH/np.sqrt(len(IsolumDJH))
#ChromSEMDJH = ChromStdDJH/np.sqrt(len(ChromDJH))
#
#print 'AchromDJH', AchromSEMDJH, 'LumDJH', LumSEMDJH, 'IsolumDJH', IsolumSEMDJH, 'ChromDJH', ChromSEMDJH

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



#Blur Data
loneMeans = [0.618, 3.576, 1.1305, 7.6, 0.7975, 7.16275, 1.03575, 7.053, 1.1475, 3.9355, 0.94585, 5.86545]
comboMeans =  [0.645, 5.27525, 1.42025, 18.2845, 0.954, 7.90125, 0.994, 19.3765, 1.0205, 11.07425, 1.00675, 12.38235]
loneStandardErrors = [0.0809189409224, 0.731886261655, 0.229643337591, 1.67653138951, 0.151590938054, 1.14286331067, 0.36263846478, 1.13340532247, 0.266455085333, 0.272849890049, 0.116250102688, 0.625416974806]
comboStandardErrors =  [0.049822183814, 0.703366669579, 0.391651212018, 1.26420061205, 0.283994938335, 0.489913433042, 0.233336666643, 2.65568243348, 0.191720662684, 1.71080059384, 0.12711785624, 1.43284851131]

loneMeansRJS = [0.618, 3.576]
comboMeansRJS = [0.645, 5.27525]
loneStandardErrorsRJS = [0.0809189409224, 0.731886261655]
comboStandardErrorsRJS = [0.049822183814, 0.703366669579]

loneMeansSH = [1.1305, 7.6]
comboMeansSH = [1.42025, 18.2845]
loneStandardErrorsSH = [0.229643337591, 1.67653138951]
comboStandardErrorsSH = [0.391651212018, 1.26420061205]

loneMeansAP = [0.7975, 7.16275]
comboMeansAP = [0.954, 7.90125]
loneStandardErrorsAP = [0.151590938054, 1.14286331067]
comboStandardErrorsAP = [0.283994938335, 0.489913433042]

loneMeansKB = [1.03575, 7.053]
comboMeansKB = [0.994, 19.3765]
loneStandardErrorsKB = [0.36263846478, 1.13340532247]
comboStandardErrorsKB = [0.233336666643, 2.65568243348]

loneMeansDJH = [1.1475, 3.9355]
comboMeansDJH = [1.0205, 11.07425]
loneStandardErrorsDJH = [0.266455085333, 0.272849890049]
comboStandardErrorsDJH = [0.191720662684, 1.71080059384]

#Blur Thresh Data
#loneMeans = [1.4368, 7.1926]
#comboMeans = [1.6320, 14.4794]
#loneStandardErrors = [0.11036, 0.79632]
#comboStandardErrors = [0.12988, 1.99703]

conditions = [1, 2, 3, 4]
#labels = ["Luminance Blur", "Chromatic Blur"]
labels = ["RJS", "SH", "AP", "KB", "DJH", "Group"]

pylab.figure(1, (11,8))
xLoneLocations = [0.5, 2.0, 3.5, 5.0, 6.5, 8.0, 9.5, 11.0, 12.5, 14.0, 17.5, 19.0]
xComboLocations = [1.0, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0, 11.5, 13.0, 14.5, 18.0, 19.5]
xwidth = 0.5
#xlocations = np.array(range(len(means)))+0.5
#ticks = [1.0, 2.5, 4.0, 5.5, 7.0, 8.5, 10.0, 11.5, 13.0, 14.5, 16.0, 19.5]
ticks = [1.75, 4.75, 7.75, 10.75, 13.75, 18.75]
yticks = [5.0, 10.0, 15.0, 20.0]

lone = pylab.bar(xLoneLocations, loneMeans, color = 'LightSkyBlue', width = xwidth, bottom =0, yerr=loneStandardErrors, ecolor = 'Black')
combo = pylab.bar(xComboLocations, comboMeans, color = 'RoyalBlue', width = xwidth, bottom =0, yerr=comboStandardErrors, ecolor = 'Black')
#pylab.xlim([0, 3.5])
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

spacing = 0.025
line = matplotlib.lines.Line2D([16-0.5-spacing, 16+0.5-spacing], [-1, 1], linewidth=1, color='black', clip_on=False)
ax3.add_line(line)

line = matplotlib.lines.Line2D([16.5-0.5-spacing, 16.5+0.5-spacing], [-1, 1], linewidth=1, color='black', clip_on=False)
ax3.add_line(line)

pylab.setp(ltext, fontsize=fontsize)

pylab.show()

