#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 21:04:21 2019

@author: coreyaustin
"""

#%%
from gwpy.timeseries import TimeSeriesDict
import numpy as np
from scipy import interpolate
from os import path

#%%

################################################################################
## Some helper functions for fetching and preparing data. Saves time series 
## data in an .hdf5 file and saves spectrograms and spectra in a .npy file
################################################################################

# return a spectrogram and a normalized spectrogram 
# both are cropped in frequency to speed things up
def specgram(channel,fftl,ovlp):
    spec = channel.spectrogram2(fftlength=fftl,overlap=ovlp)**(1/2.)
    norm = spec.ratio('median')
    return spec,norm

#fetch data for given channels at a given time and save the data, then 
#calculate spectrogram, normalized spectrogram, and spectra and save in a separate file
#return both spectrograms
def getData(channels,start,stop,filename,fftl=4,ovlp=2):
    if path.exists('{}.hdf5'.format(filename)):
        data = TimeSeriesDict.read('{}.hdf5'.format(filename))
    else:
        data = TimeSeriesDict.fetch(channels,start,stop)
        data.write('{}.hdf5'.format(filename),overwrite=True)
    spec = {}
    for i in channels:
        spec[i] = {}
        spec[i]['sp'],spec[i]['norm'] = specgram(data[i],fftl,ovlp)
        spec[i]['sp_asd'] = spec[i]['sp'].percentile(50)
    np.save(filename,spec)
    return spec 

#load time series data stored in an .hdf5 file and return the spectrogram,
#normalized spectrogram, and spectra
def loadHDF5(filename,fftl=4,ovlp=2):
    data = TimeSeriesDict.read('{}.hdf5'.format(filename))
    spec = {}
    for i in data.keys():
        spec[i] = {}
        spec[i]['sp'],spec[i]['norm'] = specgram(data[i],fftl,ovlp)
        spec[i]['sp_asd'] = spec[i]['sp'].percentile(50)
    np.save(filename,spec)
    return spec

#return contents of a numpy file 
def loadNPY(filename):
    return np.load(filename).item()

#return calibrated DARM in strain from a given DARM spectrum
def calDARM(SensorSpec,calfile='./data/L1darmcal_Apr17.txt'):
    caldarm = np.loadtxt(calfile)
    darmcal = interpolate.interp1d(caldarm[:,0],caldarm[:,1],
                fill_value='extrapolate')(SensorSpec.frequencies)
    SensorSpec *= 10**(darmcal/20)/4000
    return SensorSpec

def calAccel(SensorSpec,cal=6.1e-6):
    SensorSpec *= cal/((2*np.pi*SensorSpec.frequencies)**2)

###############################################################################
# Class for making calibrated DARM spectrum
###############################################################################
    
class SensorSpec:
    
    def export(self,filename):
        channels = self.data.keys()
        freqs = np.array(self.data[channels[0]]['sp_asd'].frequencies)
        asd   = np.array(self.data[channels[0]]['sp_asd'])
        np.savez(filename,freqs=freqs,asd=asd)
        
    def minMax(self):
        channels = self.data.keys()
        self.min = calDARM(self.data[channels[0]]['sp'].percentile(5))
        self.max = calDARM(self.data[channels[0]]['sp'].percentile(95))













