#-----------------------------------------------------------------------------------------------

import numpy as np
import h5py
from numba import jit
from math import e

#------------------------------------------------------------------------------------------------

def FT(x):
    unit_imag = 1j 
    rand = np.random.randn(len(x))  

    fx = np.fft.fft(x)  
    fra = np.fft.fft(rand)

    phx = np.angle(fx)
    phra = np.angle(fra)

    phx[1:] = phra[1:]

    fy = np.abs(fx)*e**(unit_imag*phx)  
    y = np.fft.ifft(fy) 
    recovery = np.real(y) 
    
    random=recovery
    real=x
    
    key1=sorted(range(len(random.real)), key=lambda k:  random[k])
    key2=sorted(range(len(real)), key=lambda k:  real[k])
    
    null_model=random
    
    null_model[key1]=real[key2]
    
    return null_model  

#--------------------------------------------------------------------------

absolute_address = '/mnt/data208/ChenJin/DOG/Work1/data'
data_address = absolute_address + '/RAW_DATA/M2I3NXGAS_AOD_remove_leapyear.h5'

f = h5py.File(data_address,'r')
data = f['Global'][:]
lat = f['lat'][:]
lon = f['lon'][:]
f.close()

#--------------------------------------------------------------------------

for k in range (10):

    FT_data = np.zeros((365*43,73,144))
    for i in range(len(lat)):
        for j in range (len(lon)):
            FT_data[...,i,j] = FT(np.reshape(data[...,i,j],-1))

    dataset_name = f'FT_{k+1}.h5'
    save_address = absolute_address + f'/SHUFFLED_DATA/{dataset_name}'
    f_w = h5py.File(save_address,'w')
    f_w['Global'] = FT_data
    f_w['lat'] = lat
    f_w['lon'] = lon
    f_w.close()

#----------------------------------------------------------------------------
#threshold
all_FT_data = np.zeros((365*43,10,73,144))
for i in range (10):
    dataset_name = f'FT_{i+1}.h5'
    FT_data_address = absolute_address + f'/SHUFFLED_DATA/{dataset_name}'
    f_FT = h5py.File(FT_data_address,'r')
    FT_data = f_FT['Global'][:]
    f_FT.close()

    all_FT_data[:,i,...] = FT_data

events_threshold = np.zeros((73,144))
for i in range (73):
    for j in range (144):
        events_threshold[i,j] = np.percentile(all_FT_data[:,:,i,j],90)

threshold_address = absolute_address + f'/SHUFFLED_DATA/event_threshold.h5'
f_threshold = h5py.File(threshold_address,'w')
f_threshold['threshold'] = events_threshold
f_threshold.close()

