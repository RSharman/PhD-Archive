#Creating and storing noise - August 2011

from psychopy import data, filters
import numpy as np
import os, cPickle

#Function to Create Filtered White Noise
def makeFilteredNoise(res, radius, shape='gauss'):
    noise = np.random.random([res, res])
    kernel = filters.makeMask(res, shape='gauss', radius=radius)
    filteredNoise = filters.conv2d(kernel, noise)
    filteredNoise = ((filteredNoise-filteredNoise.min())/(filteredNoise.max()-filteredNoise.min())*2-1)
    return filteredNoise
   
noise=[]
for n in range(100):
    temp = makeFilteredNoise(512, radius=0.2)
    noise.append(temp)

temp = cPickle.HIGHEST_PROTOCOL

f = open('noise02.pickle', "wb")
cPickle.Pickler(f, temp).dump(noise)
#cPickle.dump(noise, f[.temp])
f.close()

pkl_file = open('noise02.pickle', 'rb')
noise = cPickle.load(pkl_file)
print noise