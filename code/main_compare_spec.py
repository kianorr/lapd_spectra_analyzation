from IterateTempClass import CompareSpectra

import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

metastable_levels = np.array([0]) # for colradpy
path = os.getcwd() + '/adf_files'
dat_file = '/mom97_ls#c1.dat'
fil = path + dat_file # path to adf04 files

max_index_synth = 150 # highest index for synth
max_index_obs = 150 # highest index for observed wavelengths
tolerance = 0.1 # maxium allowed difference between synthetic and observed

ne = 1835785212873.8594 # observed electron density
observed_ne_arr = np.array([ne, ne])

# For iterating through temperatures since Te isn't known
initial_te = 4
final_te = 7
step = 1
te_range = np.arange(initial_te, final_te, step)

# Reading in observed data, which is already ordered from
# highest to lowest intensity
df = pd.read_csv("/home/kian/Documents/Code/spec/oct01_highest_vals.csv")
observed_wavelengths = df["Wavelength"][0:max_index_obs] # already ordered
observed_intensities = df["Intensity"][0:max_index_obs]
observed_norm_intensities = observed_intensities / observed_intensities[0] # normalized by biggest intensity

t = CompareSpectra(fil, metastable_levels, observed_wavelengths)
# Creating arrays
te_arr = t.get_array(te_range)
t.set_density(observed_ne_arr)

# iterating through temperatures.
for i, electron_temperature in enumerate(te_arr):
    t.set_temperature(electron_temperature)
    t.set_col_rad_equ()
    t.set_synthetic_intensities()
    t.set_norm_synth_intensities()
    t.set_synthetic_wavelengths()
    t.order_spectra(i)
    ordered_synth_wavelengths = t.get_ordered_spectra(max_index=max_index_synth)[0]
    t.set_ordered_synth_wavelengths(ordered_synth_wavelengths)
    t.get_compared_values(observed_wavelengths, observed_norm_intensities, tolerance)
