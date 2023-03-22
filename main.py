import pandas as pd
import numpy as np
import baseline

import urllib.request
import certifi
import json

url = 'https://data.nationalgrideso.com/api/3/action/datastore_search?resource_id=18c69c42-f20d-46f0-84e9-e279045befc6&limit=17520'
fileobj = urllib.request.urlopen(url, cafile=certifi.where())
json_version = json.loads(fileobj.read().decode())

demand_data = pd.DataFrame(json_version['result']['records'])
demand_data = demand_data.sort_values([ 'SETTLEMENT_DATE',  'SETTLEMENT_PERIOD'])
demand_data.index = pd.DatetimeIndex(pd.date_range(start="2021-01-01", freq='30T', periods=17520, tz='Europe/London'))
demand_data['ND'] = demand_data['ND'].astype(float)
demand_data['power'] = demand_data['ND']
demand_data['energy'] = demand_data['power'] * 0.5
demand_data = demand_data[['power', 'energy']]

flexibility_start_time = pd.Timestamp(year=2021, month=12, day=24,
                                      hour=17, minute=00, second=0, tz="Europe/London")
flexibility_finish_time = pd.Timestamp(year=2021, month=12, day=24,
                                       hour=20, minute=00, second=0, tz="Europe/London")

