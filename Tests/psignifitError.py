import pypsignifit as psi
import numpy as np

num_of_sess = 3
num_of_block = 5
num_of_trials = 50

stimulus_intensities = [0.021, 0.079, 0.154, 0.255, 0.30]
percent_correct_1 = [0.5, 0.84, 0.96, 1.0, 1.0]
percent_correct_2 = [0.64, 0.92, 1.0, 0.96, 1.0]
percent_correct_3 = [0.58, 0.76, 0.98, 1.0, 1.0]

num_observations = [num_of_trials]*num_of_block
data_1 = np.c_[stimulus_intensities, percent_correct_1, num_observations]
data_2 = np.c_[stimulus_intensities, percent_correct_2, num_observations]
data_3 = np.c_[stimulus_intensities, percent_correct_3, num_observations]

data = np.r_[data_1, data_2, data_3]

nafc=2
priors = ('Gauss(0,5)', 'Gamma(1,3)', 'Beta(2,20)')

mcmc = psi.BayesInference(data, priors = priors, nafc=2)

print mcmc.estimate
print mcmc.deviance