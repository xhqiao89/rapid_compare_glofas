from netCDF4 import Dataset
import numpy as np
import pandas as pd
import os
import datetime

## Define the directory that contains all of the NetCDF files here:
# workdir = r'/run/user/1000/gvfs/smb-share:server=10.32.120.131,share=files,user=ciwater/ERAI_Land_discharge'
# first_date = '1980-01-01'
# last_date = '2016-10-31'


workdir = "./data"
first_date = '1980-01-01'
last_date = '1980-02-29'



outputdir = "./output"


t = datetime.datetime.now()


def print_time(t, prt=True):
    s = t.strftime("%Y-%m-%d %H:%M:%S")
    if prt:
        print(s)
    return s

def print_time_elasped(t_start):

    now = datetime.datetime.now()
    delta = now - t_start
    print("{} --- {}".format(print_time(now, prt=False), delta))


def get_indices(original, search):

    original = np.array(original)
    search = np.array(search)
    original_indices_argsort = np.argsort(original)
    original_sorted = original[original_indices_argsort]
    search_indices_sort = np.searchsorted(original_sorted, search)
    search_indices = original_indices_argsort[search_indices_sort]
    return search_indices


def extract_spt_data2(data_df, workdir, first_date, last_date):
    files = os.listdir(workdir)
    files.sort()
    fpaths = [os.path.join(workdir, d) for d in files if d[-2:] == "nc"]

    root_grp = Dataset(fpaths[0])
    lat_search = data_df["lat_y"].values

    lat_list = np.round(root_grp.variables['lat'][:], decimals=2).tolist()
    lat_search_indices = get_indices(lat_list, lat_search)

    lon_search = data_df["lon_x"].values
    lon_list = np.round(root_grp.variables['lon'][:], decimals=2).tolist()
    lon_search_indices = get_indices(lon_list, lon_search)

    total_dis_narray = None

    for fpath in fpaths:
        print(fpath)
        root_grp = Dataset(fpath)
        dis = root_grp.variables['dis']

        time = root_grp.variables['time'].shape[0]

        discharge = dis[:, lat_search_indices, lon_search_indices]
        if isinstance(discharge, np.ma.MaskedArray):
            discharge = np.ma.filled(discharge, fill_value=0)

        if total_dis_narray is None:
            total_dis_narray = discharge
        else:
            total_dis_narray = np.concatenate((total_dis_narray, discharge), axis=0)
        print_time_elasped(t)

    time_index = pd.date_range(first_date, last_date)

    outputbase = os.path.join(outputdir, "out_{}".format(print_time(t, prt=False)))
    os.makedirs(outputbase)
    for i in range(total_dis_narray.shape[1]):
        df = pd.DataFrame(total_dis_narray[:,i,i], index=time_index, columns=['Discharge (m^3/s)'])
        row = data_df.iloc[i]

        filename = "{c}_{b}_{s}_{lon_x}x_{lat_y}y.csv".format(c=row["country"],
                                                    b=row["basin"],
                                                    s=row["station"],
                                                    lon_x=row["lon_x"],
                                                    lat_y=row["lat_y"],
                                                    )
        df.to_csv(os.path.join(outputbase, filename), index_label='Datetime')
    return df

print_time(t)
data = pd.read_excel(r'./GlofasStationswade_rev.xlsx', sheet_name="Sheet2", usecols='A:F')

# Reading Data From the Spreadsheet
longitudes = data.iloc[:, 0].values
latitudes = data.iloc[:, 1].values
basins = data.iloc[:, 4].values
countries = data.iloc[:, 3].values
stations = data.iloc[:, 5].values


data = zip(countries, basins, stations, longitudes, latitudes)
data_df = pd.DataFrame(data, columns=["country", "basin", "station", "lon_x", "lat_y"])
print(data_df)
extract_spt_data2(data_df, workdir=workdir, first_date=first_date, last_date=last_date)
print("done")