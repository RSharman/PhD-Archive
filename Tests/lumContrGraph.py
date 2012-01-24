#Test plots of Beta values and different luminance contrasts

import pylab
import scipy

contrasts = [0.1, 0.075, 0.05, 0.025, 0.023, 0.0225, 0.022, 0.02]
betas = [0.005364, 0.005306, 0.006044, 0.00839, 0.00806, 0.008984, 0.01256, 0.01285]
SEM = [0.001812, 0.001437, 0.001582, 0.001172, 0.002347, 0.001392, 0.001362, 0.002358, 0.002902]

pylab.plot(contrasts, betas, 'ok-')

pylab.show()