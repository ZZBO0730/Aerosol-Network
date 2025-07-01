#-----------------------------------------------------------------------------------------------------------------
# events synchronization
#
# Compute every points events synchronization  
#
#-----------------------------------------------------------------------------------------------------------------

import numpy as np
import h5py


# Obtain time series of the start time of extreme events
def get_time (data_array):

    date = np.zeros((len(data_array),))
    threshold = np.percentile(data_array,90)
    date[data_array>threshold] = 1

    tmp = date[1:] + date[:-1]
    if date[0] == 0:
        tmp = np.insert(tmp,0,0)
    else:
        tmp = np.insert(tmp,0,1)

    loc = np.arange(len(data_array))
    tmp_1 = loc[tmp == 1]

    events_time = []
    for k in range (0,len(tmp_1),2):
        time_tmp = tmp_1[k]
        events_time.append(time_tmp)
    
    return(np.array(events_time))

# Compute event synchronization between each node of the network
def EvSy(i,j,k):

    timestamp_array1 = i
    timestamp_array2 = j
    
    event1= len(timestamp_array1)
    event2= len(timestamp_array2)

    EvSy_all = 0
    EvSy_ij = 0
    EvSy_ji = 0 

    for i in range (1,(event1-1)):
        for j in range (1,(event2-1)):
            delay = (min (timestamp_array1[i+1]-timestamp_array1[i],timestamp_array1[i]-timestamp_array1[i-1],timestamp_array2[j+1]-timestamp_array2[j],timestamp_array2[j]-timestamp_array2[j-1]))/2
                    
            waiting_time = timestamp_array1[i] - timestamp_array2[j]

            if -delay < waiting_time and waiting_time <= 0 and abs(waiting_time) <= k:
                EvSy_ij += 1
            if 0 <= waiting_time and waiting_time < delay and abs(waiting_time) <= k:
                EvSy_ji += 1
            if abs(waiting_time) <= delay and abs(waiting_time) <= k :
                EvSy_all += 1

    return(EvSy_ij,EvSy_ji,EvSy_all)

def get_events (data_array):

    date = np.zeros((len(data_array),))
    threshold = np.percentile(data_array,90)
    date[data_array>threshold] = 1

    tmp = date[1:] + date[:-1]
    if date[0] == 0:
        tmp = np.insert(tmp,0,0)
    else:
        tmp = np.insert(tmp,0,1)

    loc = np.arange(len(data_array))
    tmp_1 = loc[tmp == 1]

    events_time = []
    for k in range (0,len(tmp_1),2):
        time_tmp = tmp_1[k]
        events_time.append(time_tmp)

    events_num = len(events_time)
    return(events_num)

#-----------------------------------------------------------------------------------------------------------------

absolute_address = '/mnt/data208/ChenJin/DOG/Work1/data'
data_address = absolute_address + '/RAW_DATA/M2I3NXGAS_AOD_remove_leapyear.h5'
realES_address = absolute_address + '/ALL/EvSy_real.h5'

f = h5py.File(data_address,'r')
data = f['Global'][:]
lat = f['lat'][:]
lon = f['lon'][:]
f.close()
    
#-----------------------------------------------------------------------------------------------------------------
events  = np.zeros((len(lat),len(lon)))
EvSy_all = np.zeros((len(lat),len(lon),len(lat),len(lon)))
EvSy_ij = np.zeros((len(lat),len(lon),len(lat),len(lon)))
EvSy_ji = np.zeros((len(lat),len(lon),len(lat),len(lon)))

for i in range (0,len(lat),1):
    for j in range (0,len(lon),1):
        events[i,j] = get_events(np.reshape(data[...,i,j],-1))
    
for m in range(0,len(lat),1):
    for n in range(0,len(lon),1):
        for p in range(0,len(lat),1):
            for q in range(0,len(lon),1):
                if m == p and n == q :
                    continue
                else:
                    ij,ji,ES = EvSy(get_time(np.reshape(data[...,m,n],-1)),get_time(np.reshape(data[...,p,q],-1)),30)
                    EvSy_ij[m][n][p][q] = ij
                    EvSy_ji[m][n][p][q] = ji
                    EvSy_all[m][n][p][q] = ES

f_w = h5py.File(realES_address,'w')
f_w['events'] = events
f_w['EvSy_ij'] = EvSy_ij
f_w['EvSy_ji'] = EvSy_ji
f_w['EvSy_all'] = EvSy_all
f_w['lat'] = lat
f_w['lon'] = lon
f_w.close()


    
