import numpy as np
import sys
sys.path.append('/home/kian/ColRadPy')
from colradpy.ionization_balance_class import ionization_balance
from colradpy import colradpy

class CompareSpectra():
    '''Creates synthetic spectra using `colradpy` and compares it to observed spectra.'''
    
    def __init__(self, fil,
                 metastable_levels,
                 real_wavelengths,
                 col_rad_equ=None, 
                 electron_density=None, 
                 temperature_density=None, 
                 synthetic_wavelengths=None,
                 norm_synth_intensities=None):
        '''Constructor method for CreateSpectra class.'''
        
        self.real_wavelengths = real_wavelengths
        self.metastable_levels = metastable_levels
        self.fil = fil
        
        if electron_density != None:
            self.electron_density = electron_density
        if temperature_density != None:
            self.electron_temperature = electron_temperature
        if col_rad_equ != None:
            self.col_rad_equ = col_rad_equ
        if synthetic_wavelengths != None:
            self.synthetic_wavelengths = synthetic_wavelengths
        if norm_synth_intensities != None:
            self.norm_synth_intensities = norm_synth_intensities
            
    def set_temperature(self, electron_temperature):
        '''Sets the electron temperature.'''
        self.electron_temperature = electron_temperature
        
    def set_density(self, electron_density):
        '''Sets electron density.'''
        self.electron_density = electron_density
        
    def get_temperature(self):
        '''Gets electron temperature.'''
        return self.electron_temperature
    
    def get_density(self):
        '''Gets electron density.'''
        return self.electron_density
    
    def set_col_rad_equ(self, recombination=False, 
                        recombination_three_body=False, 
                        ionization=False, 
                        suppliment_with_ecip=True):
        '''Solves the collisional radiative equation given by colradpy.'''
        
        self.col_rad_equ = colradpy(self.fil,
                                    self.metastable_levels,
                                    self.electron_temperature,
                                    self.electron_density,
                                    use_recombination=recombination, 
                                    use_recombination_three_body=recombination_three_body,
                                    use_ionization=ionization,
                                    suppliment_with_ecip=suppliment_with_ecip)
        
        self.col_rad_equ.solve_cr()
    
    def set_synthetic_wavelengths(self, synthetic_wavelengths=None):
        '''Sets the synthetic wavelengths using colradpy.'''
        self.synthetic_wavelengths = self.col_rad_equ.data['processed']['wave_air']
#        if synthetic_wavelengths != None:
#            self.synthetic_wavelengths = synthetic_wavelengths
            
    def set_ordered_synth_wavelengths(self, ordered_synth_wavelengths):
    	'''Sets the ordered synthetic wavelengths.'''
        self.ordered_synth_wavelengths = ordered_synth_wavelengths
    
    def set_synthetic_intensities(self):
    	'''Sets the synthetic intensities.'''
        self.synthetic_intensities = self.col_rad_equ.data['processed']['pecs'][:, 0, 0, 0]
        
    def set_norm_synth_intensities(self):
    	'''Normalizes the synthetic intensities.'''
        self.norm_synth_intensities = self.synthetic_intensities / np.max(self.synthetic_intensities)
        
    def set_real_wavelengths(self, real_wavelengths):
    	'''Sets the real wavelengths observed in the lapd.'''
        self.real_wavelengths = real_wavelengths
    
    def get_array(self, property_range):
    	'''Gets the array for either electron temperature or density.'''
        property_arr = []
        for electron_property in property_range:
            single_arr = np.array([electron_property, electron_property])
            property_arr = np.append(property_arr, single_arr)
        
        property_arr = np.reshape(property_arr, (len(property_range), 2))
        return property_arr
    
    
    def order_spectra(self, index, max_index=None, min_index=0, te=1, ne=1, met=0):
    	'''Orders the synthetic wavelengths by their intensity from highest to lowest.'''
        highest = sorted(((intensity, self.synthetic_wavelengths[i]) for i, intensity in enumerate(self.norm_synth_intensities)), reverse=True)
        
        self.ordered_norm_synth_intensities = []
        self.ordered_synth_wavelengths = []
        for pair in highest:
            self.ordered_norm_synth_intensities.append(pair[0])
            self.ordered_synth_wavelengths.append(pair[1])
        
    def get_ordered_spectra(self, min_index=0, max_index=200):
    	'''
    	Gets the ordered wavelengths and intensities.
    	
    	Returns
    	-------
    	ordered_spectra : `tuple`
    		In the form of (ordered wavelengths, ordered intensities), where wavelengths and intensities are arrays.
    	'''
        ordered_spectra = (self.ordered_synth_wavelengths[min_index:max_index], self.ordered_norm_synth_intensities[min_index:max_index])
        return ordered_spectra
    
    def get_compared_values(self, real_wavelengths, norm_real_intensity, tolerance):
    	'''
    	Compares the synthetic spectra and real spectra.
    	
    	Prints out the wavelengths that are close together with it's respective relative intensity.
    	'''
        print(f"-------------- {self.electron_temperature[0]} eV --------------")
        for i, real_wavelength in enumerate(real_wavelengths):
            for j, synthetic_wavelength in enumerate(self.ordered_synth_wavelengths):
                if abs(real_wavelength - synthetic_wavelength) < tolerance:
                    print(f"Observed wavelength : {real_wavelength} ({i}) (i: {norm_real_intensity[i]})\n" 
                          f"Synthetic wavelength: {synthetic_wavelength} ({j}) (i: {self.ordered_norm_synth_intensities[j]})\n")
