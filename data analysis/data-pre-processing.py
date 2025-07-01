#-----------------------------------------------------------------------------------------------------------------
# data per processing
#
# Interpolation of data precision from 0.5 x 0.625 to 2.5 x 2.5，removing leap year effects and season effects
#
#-----------------------------------------------------------------------------------------------------------------

import numpy as np
import netCDF4 as nc
import h5py

#-----------------------------------------------------------------------------------------------------------------
# Data interpolation precision from 0.5 x 0.625 to 2.5 x 2.5, removing leap year effects
def per_processing(address,lat_interpolation_number,lon_interpolation_number,save_address):

    year_list = []
    for i in range (2001,2023,1):
        year_list.append(str(i))

    conclude_data = np.zeros((len(year_list),365,73,144))
    for j in range (0,len(year_list),1):
        read_address = address + year_list[j] +'-mean.nc'
        ncData = nc.Dataset(read_address,'r',format = 'NETCDF4')
        AOD = ncData.variables['AODANA'][:,::lat_interpolation_number,::lon_interpolation_number]
        
        if AOD.shape[0] == 366:
            AOD = np.delete(AOD,59,0)
        conclude_data[j] = AOD

    f_w = h5py.File(save_address,'w')
    f_w['Global'] = conclude_data
    lat = ncData.variables['lat'][::lat_interpolation_number]
    lon = ncData.variables['lon'][::lon_interpolation_number]
    f_w['lat'] = lat
    f_w['lon'] = lon

    f_w.close()


# geopotentialheight and windspeed data

def geoh_processing(address,lat_interpolation_number,lon_interpolation_number,save_address):

    year_list = []
    for i in range (2001,2023,1):
        year_list.append(str(i))

    conclude_data = np.zeros((len(year_list),365,73,144))
    Conclude_data = np.zeros((len(year_list),365,73,144))
    for j in range (0,len(year_list),1):
        read_address = address + year_list[j] +'-mean.nc'
        ncData = nc.Dataset(read_address,'r',format = 'NETCDF4')
        H = ncData.variables['H'][:,0,::lat_interpolation_number,::lon_interpolation_number]
        
        if H.shape[0] == 366:
            H = np.delete(H,59,0)
        conclude_data[j] = H

    year_average=np.average(conclude_data,axis = 0)

    for k in range (0,len(year_list),1):
        Conclude_data[k] = conclude_data[k] - year_average

    f_w = h5py.File(save_address,'w')
    f_w['H'] = Conclude_data
    lat = ncData.variables['lat'][::lat_interpolation_number]
    lon = ncData.variables['lon'][::lon_interpolation_number]
    f_w['lat'] = lat
    f_w['lon'] = lon

    f_w.close()

def windspeed_u(address,lat_interpolation_number,lon_interpolation_number,save_address):

    year_list = []
    for i in range (2001,2023,1):
        year_list.append(str(i))

    conclude_data = np.zeros((len(year_list),365,73,144))
    Conclude_data = np.zeros((len(year_list),365,73,144))
    for j in range (0,len(year_list),1):
        read_address = address + year_list[j] +'-mean.nc'
        ncData = nc.Dataset(read_address,'r',format = 'NETCDF4')
        U = ncData.variables['U'][:,0,::lat_interpolation_number,::lon_interpolation_number]
        
        if U.shape[0] == 366:
            U = np.delete(U,59,0)
        conclude_data[j] = U

    year_average=np.average(conclude_data,axis = 0)

    for k in range (0,len(year_list),1):
        Conclude_data[k] = conclude_data[k] - year_average

    f_w = h5py.File(save_address,'w')
    f_w['U'] = Conclude_data
    lat = ncData.variables['lat'][::lat_interpolation_number]
    lon = ncData.variables['lon'][::lon_interpolation_number]
    f_w['lat'] = lat
    f_w['lon'] = lon

    f_w.close()

def windspeed_v(address,lat_interpolation_number,lon_interpolation_number,save_address):

    year_list = []
    for i in range (2001,2023,1):
        year_list.append(str(i))

    conclude_data = np.zeros((len(year_list),365,73,144))
    Conclude_data = np.zeros((len(year_list),365,73,144))
    for j in range (0,len(year_list),1):
        read_address = address + year_list[j] +'-mean.nc'
        ncData = nc.Dataset(read_address,'r',format = 'NETCDF4')
        V = ncData.variables['V'][:,0,::lat_interpolation_number,::lon_interpolation_number]
        
        if V.shape[0] == 366:
            V = np.delete(V,59,0)
        conclude_data[j] = V

    year_average=np.average(conclude_data,axis = 0)

    for k in range (0,len(year_list),1):
        Conclude_data[k] = conclude_data[k] - year_average

    f_w = h5py.File(save_address,'w')
    f_w['V'] = Conclude_data
    lat = ncData.variables['lat'][::lat_interpolation_number]
    lon = ncData.variables['lon'][::lon_interpolation_number]
    f_w['lat'] = lat
    f_w['lon'] = lon

    f_w.close()

#-----------------------------------------------------------------------------------------------------------------
absolute_address = 'data'

'''

M2I3NXGAS_address = absolute_address + '/M2I3NXGAS-DAY-MEAN/'
AOD_address = absolute_address + '/2001_2022_M2I3NXGAS_AOD_remove_leapyear.h5'
per_processing(M2I3NXGAS_address,5,4,AOD_address)

'''
M2I3NPASM_address = absolute_address + '/M2I3NPASM-DAY-MEAN/'
H_address = absolute_address + '/M2I3NPASM_H_remove_leapyear_season_Network3.h5'
U_address = absolute_address + '/M2I3NPASM_U_remove_leapyear_season_Network3.h5'
V_address = absolute_address + '/M2I3NPASM_V_remove_leapyear_season_Network3.h5'
                  
geoh_processing(M2I3NPASM_address,5,4,H_address)
windspeed_u(M2I3NPASM_address,5,4,U_address)
windspeed_v(M2I3NPASM_address,5,4,V_address)
