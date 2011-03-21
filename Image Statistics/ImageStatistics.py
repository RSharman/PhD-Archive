#Image statistics to analyse LM and S in natural images - February 2011

from psychopy import colorFunctions
import numpy as np
import copy
import Image

range = range(512)

#Import picture and convert from RGB to DKL
pictures = ["Leaf512.jpg", "Pansy512.jpg", "Pelican512.jpg", "Pumpkin512.jpg"]

picture=np.array(Image.open("Pumpkin512.jpg").transpose(Image.FLIP_TOP_BOTTOM))/127.5-1

dklPicture = colorFunctions.rgb2dklCart(picture)
dklPicture = np.array(dklPicture)

lum = copy.copy(dklPicture[:,:,0])
lm = copy.copy(dklPicture[:,:,1])
s = copy.copy(dklPicture[:,:,2])


print 'rms lm', lm.std()
print 'rms s', s.std()
print 'rms lum', lum.std()

#print np.min(lm)
#print np.max(lm)

#Calculate the range of lm, s and lum
print 'lum min', np.min(lum), 'lum max', np.max(lum)
print 'lm min', np.min(lm), 'lm max', np.max(lm)
print 's min', np.min(s), 's max', np.max(s)

#Creating some counters and empty lists
lmCounter = 512
sCounter = 512
lumCounter = 512

positiveLum=[]
positiveLm = []
positiveS = []

negativeLum=[]
negativeLm = []
negativeS = []

positiveBoundLmCounter = 0
negativeBoundLmCounter = 0
positiveBoundSCounter = 0
negativeBoundSCounter = 0
positiveBoundLumCounter = 0
negativeBoundLumCounter = 0

positiveBoundLm = []
positiveBoundS = []
positiveBoundLum = []

negativeBoundLm = []
negativeBoundS =[]
negativeBoundLum = []

#Calculating the number of type of pixel that is active - defined as being over 0.05 or under -0.05
for n in range:
    if lm[0, n]<=0.05:
        if lm[0,n]>=-0.05:
            lmCounter-=1

    if s[0,n]<=0.05:
        if s[0,n]>=-0.05:
            sCounter-=1

    if lum[0,n]<=0.05:
        if lum[0,n]>=-0.05:
            lumCounter-=1


#Calculating the number of active pixels either side of zero - defined as being over 0.05 or under -0.05
#and the mean of the negative and positive activation
    if lm[0,n]>=0.05:
        positiveBoundLmCounter +=1
        temp = lm[0,n]
        positiveBoundLm.append(temp)

    if lm[0,n]<=-0.05:
        negativeBoundLmCounter +=1
        temp = lm[0,n]
        negativeBoundLm.append(temp)

    if s[0,n]>=0.05:
        positiveBoundSCounter +=1
        temp = s[0,n]
        positiveBoundS.append(temp)
        
    if s[0,n]<=-0.05:
        negativeBoundSCounter +=1
        temp = s[0,n]
        negativeBoundS.append(temp)

    if lum[0,n]>=0.05:
        positiveBoundLumCounter +=1
        temp = lum[0,n]
        positiveBoundLum.append(temp)
        
    if lum[0,n]<=-0.05:
        negativeBoundLumCounter +=1
        temp = lum[0,n]
        negativeBoundLum.append(temp)

#Calculating the total amount of activation above or below 0
#    if lm[0,n]<0:
#        temp = lm[0,n]*(-1)
#        negativeLm.append(temp)
#
#    if lm[0,n]>=0:
#        temp = lm[0,n]
#        positiveLm.append(temp)
#
#    if s[0,n]<0:
#        temp = s[0,n]*(-1)
#        negativeS.append(temp)
#
#    if s[0,n]>=0:
#        temp = s[0,n]
#        positiveS.append(temp)
#
#    if lum[0,n]<0:
#        temp = lum[0,n]*(-1)
#        negativeLum.append(temp)
#
#    if lum[0,n]>=0:
#        temp = lum[0,n]
#        positiveLum.append(temp)



#Printing all the results
print 'lum', lumCounter
print 'lm', lmCounter
print 's', sCounter
#print 'lm mean', np.mean(lm)
#print 's mean', np.mean(s)
#print 'lum mean', np.mean(lum)

print 'Bound lm mean positive from zero', np.mean(positiveBoundLm), 'size', positiveBoundLmCounter, 'Bound lm mean negative from zero', np.mean(negativeBoundLm), 'size', negativeBoundLmCounter
print 'Bound s mean positive from zero', np.mean(positiveBoundS), 'size', positiveBoundSCounter, 's mean negative from zero', np.mean(negativeBoundS), 'size', negativeBoundSCounter
print 'Bound lum mean positive from zero', np.mean(positiveBoundLum), 'size', positiveBoundLumCounter, 'lum mean negative from zero', np.mean(negativeBoundLum), 'size', negativeBoundLumCounter











