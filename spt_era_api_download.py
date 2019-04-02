import requests

request_params = dict(watershed_name='South Asia', subbasin_name='Mainland', reach_id=58807, return_format = 'csv')
request_headers = dict(Authorization='Token 84139ea5673c426dbddb0299e2e9bd15a5a546cd')
res = requests.get('https://tethys.byu.edu/apps/streamflow-prediction-tool/api/GetHistoricData/', params=request_params, headers=request_headers)
print(res.content)
