#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 14:00:09 2019

@author: coreyaustin
"""
#%%

from MakeSpectrograms.makeSpectrograms import *

# Update the matplotlib configuration parameters:
plt.rcParams.update({'text.usetex': False})

#%%

channels = ['L1:CAL-DELTAL_EXTERNAL_DQ','L1:GDS-CALIB_STRAIN']
start    = 'May 23 2019 07:35:00 UTC'
end      = 'May 23 2019 07:40:00 UTC'
filename = '190619_test'
    
darm_now = SensorSpec()
#darm_now.data = getData(channels,start,end,'./data/{}'.format(filename),
#                        fftl=10,ovlp=7)
darm_now.data = loadNPY('./data/{}.npy'.format(filename))
darm_now.calib_asd = calDARM(darm_now.data[channels[0]]['sp_asd'])
darm_now.export('./data/L1_DARM_190523')
#darm_now.minMax()


#%%

plt.style.use('seaborn-whitegrid')

limx   = [10,5000]
limy   = [1e-24,2e-18]


f1, (ax1) = plt.subplots(1, sharex=False, figsize=[16,9])

ax1.plot(darm_now.calib_asd,label='L1 DARM (23 May 2019)')
#ax1.plot_mmm(darm_now.calib_asd,darm_now.min,darm_now.max)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlim(limx)
ax1.set_ylim(limy)
ax1.set_xlabel('Frequency (Hz)',color='dimgray',fontsize=14)
ax1.set_ylabel(r'Strain/$\sqrt{Hz}$',color='dimgray',fontsize=14)
ax1.set_title(r'L1 Gravitational Wave Strain $[h(t)]$',color='dimgray',fontsize=16)
ax1.legend()
ax1.grid(which='both',axis='both',color='darkgrey',linestyle='dotted')  
ax1.tick_params(axis='both', colors='dimgrey', labelsize=14) 
#plt.tight_layout(rect=[0,0,.99,.99])