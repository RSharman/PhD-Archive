#Boynton illusion code using pylab
from psychopy import visual, core, event
import pylab
from scipy import *
from pylab import *

#Define the sine waves
lineWidth = 3
Amplitude = 10
Frequency = 3
figSize = 5

#Define Inner Square
xy = 0,0
width, height = 200, 200

#Generate the pair of horizontal sine waves
x = arange(1, 201, 0.1)
y01 = Amplitude*sin(Frequency*pi*x/100)+200
y02 = Amplitude*sin(Frequency*pi*x/100)

#Generate the pair of vertical sine waves
x02 = (reshape(x, -1))
y03 = Amplitude*sin(Frequency*pi*x02/100)
y04 = Amplitude*sin(Frequency*pi*x02/100)+200

#Plot everything
fig = figure(figsize=[figSize, figSize])

ax =subplot(111)

plot(x, y01, color = 'black', linewidth=lineWidth)
plot(x, y02, color = 'black', linewidth=lineWidth)

plot(y03, x02, color = 'black', linewidth=lineWidth)
plot(y04, x02, color = 'black', linewidth=lineWidth)

square = Rectangle(xy, width, height, facecolor = '#0032FF', alpha = 0.05, edgecolor = 'none')

ax.set_frame_on(False)
ax.add_patch(square)

#Get rid of the ticks and axis labels
ax.xaxis.set_major_formatter(NullFormatter())
ax.xaxis.set_major_locator(NullLocator())
ax.yaxis.set_major_formatter(NullFormatter())
ax.yaxis.set_major_locator(NullLocator())

pylab.show()