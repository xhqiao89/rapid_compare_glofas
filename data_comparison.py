from netCDF4 import Dataset
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import xarray
import requests
from bs4 import BeautifulSoup


## get forecast of one stream from netcdf file
nc_file_path = "/home/sherry/Downloads/COSMO/output/LP_rapid/Qout_COSMO_cosmo_grid_1hr_2018082112to2018082818.nc"
f = Dataset(nc_file_path, "r")
t = f.variables["time"][:]
t_datetime = [dt.datetime.utcfromtimestamp(e) for e in t]
print str(t_datetime[0].day) +'/'+ str(t_datetime[0].month) + '/'+ str(t_datetime[0].year)

# get index of the stream
rivid = f.variables["rivid"][:]
stream_id = 174912
n = np.argwhere(rivid==stream_id)[0][0]

# get observations
codEstacao = '63010000'
DataInicio = str(t_datetime[0].day) +'/'+ str(t_datetime[0].month) + '/'+ str(t_datetime[0].year)
DataFim = str(t_datetime[-1].day) +'/'+ str(t_datetime[-1].month) + '/'+ str(t_datetime[-1].year)

print DataInicio, DataFim

url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/DadosHidrometeorologicos?codEstacao=' + codEstacao + '&DataInicio=' + DataInicio + '&DataFim=' + DataFim

response = requests.get(url)

soup = BeautifulSoup(response.content, "xml")

times = soup.find_all('DataHora')
values = soup.find_all('Vazao')

dates = []
flows = []

for time in times:
    dates.append(dt.datetime.strptime(time.get_text().strip(), "%Y-%m-%d %H:%M:%S"))

for value in values:
    flows.append(float(value.get_text().strip()))

flows_new= flows[::-1]
dates_new = dates[::-1]

plt.plot(t_datetime, f.variables["Qout"][:, n], 'r-',dates_new, flows_new, 'b-')
plt.xlabel('Time (s)')
plt.ylabel('Discharge(m3/s)')
plt.show()

f.close()

