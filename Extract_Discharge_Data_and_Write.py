from netCDF4 import Dataset
import numpy as np
import pandas as pd
import os

# Define the directory that contains all of the NetCDF files here:
workdir = r'./data'
# Enter the first date of the time series and the last date here:
first_date = '1980-01-01'
last_date = '1980-02-29'


def extract_spt_data(lat, lon, workdir, first_date, last_date):
    files = os.listdir(workdir)
    files.sort()
    fpaths = [os.path.join(workdir, d) for d in files if d[-2:] == "nc"]

    # Creating an empty list to append the discharge data to for the given lat and lon coordinates
    total_dis_list = []

    for fpath in fpaths:
        print(fpath)
        root_grp = Dataset(fpath)
        dis = root_grp.variables['dis']
        lat_list = np.round(root_grp.variables['lat'][:], decimals=2).tolist()
        lon_list = np.round(root_grp.variables['lon'][:], decimals=2).tolist()
        time = root_grp.variables['time'].shape[0]
        lat_index = lat_list.index(lat)
        lon_index = lon_list.index(lon)
        discharge = dis[:, lat_index, lon_index]
        if isinstance(discharge, np.ma.MaskedArray):
            discharge = np.ma.filled(discharge, fill_value=0)
        total_dis_list.extend(discharge.tolist())

    time_index = pd.date_range(first_date, last_date)
    df = pd.DataFrame(total_dis_list, index=time_index, columns=['Discharge (m^3/s)'])
    return df


data = pd.read_excel(r'./GlofasStationswade_rev.xlsx',
                     sheet_name="Sheet2", usecols='A:F')

# Reading Data From the Spreadsheet
countries = data.iloc[:, 3].values
basins = data.iloc[:, 4].values
stations = data.iloc[:, 5].values
longitudes = data.iloc[:, 0].values
latitudes = data.iloc[:, 1].values

print(countries)
print(basins)
print(stations)
print(longitudes)
print(latitudes)

# Reading from the NetCDF Files and writing to the correct directory
for country, basin, station, lat, lon in zip(countries, basins, stations, latitudes, longitudes):
    # Creating a Directory for Each Country
    dir = os.path.join(r'./GloFASreanalysis', country.title())
    if not os.path.isdir(dir):
        os.makedirs(dir)
    # Extracting the Data from the NetCDF files based on Lat and Lon
    df = extract_spt_data(lat=lat, lon=lon, workdir=workdir, first_date=first_date, last_date=last_date)
    station_name = station.replace(' ', '_')
    basin = basin.replace(' ', '_')
    file_name = '{}-{}_ECMWF_data.csv'.format(basin.lower(), station_name.lower())
    df.to_csv(os.path.join(dir, file_name), index_label='Datetime')


# for station, lat, lon in zip(stations, latitudes, longitudes):
#     print("Lat: {}, Lon {}, Station: {}".format(lat, lon, station))
#     df = extract_spt_data(lat=lat, lon=lon, workdir=workdir, first_date=first_date, last_date=last_date)
#     out_folder = r'C:\Users\wadear\Documents\Nepal_Data\ECMWF_Data'
#     file_name = '{}_ECMWF_data.csv'.format(station)
#     df.to_csv(os.path.join(out_folder, file_name), index_label='Datetime')
