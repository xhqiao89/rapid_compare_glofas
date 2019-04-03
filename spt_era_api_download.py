import requests
import os
import pandas as pd

data = pd.read_excel(r'./GlofasStations.xlsx',
                     sheet_name="Sheet2", usecols='A:H')

# Reading Data From the Spreadsheet
watersheds = data.iloc[:, 3].values
subbasins = data.iloc[:, 4].values
reach_ids = data.iloc[:, 2].values

for watershed, subbasin, reach_id in zip(watersheds, subbasins, reach_ids,):

    request_params = dict(watershed_name=watershed, subbasin_name=subbasin, reach_id=reach_id, return_format='csv')
    request_headers = dict(Authorization='Token 84139ea5673c426dbddb0299e2e9bd15a5a546cd')
    res = requests.get('https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetHistoricData/', params=request_params, headers=request_headers)

    csv = open(r'./api_output.csv', "w")
    csv.write(res.content)



