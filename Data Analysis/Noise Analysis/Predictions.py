import numpy as np

lum = 0.009717
lm = 0.009509
s = 0.01641

lm = (lm/(np.sqrt(2)))**2
s = (s/(np.sqrt(2)))**2
lum = (lum/(np.sqrt(2)))**2

lmlum = (lm*lum)/(lm+lum)
slum = (s*lum)/(s+lum)
lms = (lm*s)/(lm+s)

lmlum = (np.sqrt(lmlum))*(np.sqrt(2))
slum = (np.sqrt(slum))*(np.sqrt(2))
lms = (np.sqrt(lms))*(np.sqrt(2))

print 'lmlum', lmlum
print 'slum', slum
print 'lms', lms