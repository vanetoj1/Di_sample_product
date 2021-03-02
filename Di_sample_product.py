# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 08:57:58 2021

@author: VTodorova
"""

from __future__ import print_function

import requests

from requests.auth import HTTPBasicAuth

import datetime 
from datetime import datetime, timedelta


today = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-7] 




headers_North = { 'Content-Type': 'application/json','MAC':'80:1F:12:73:3C:89'}


#response = requests.get('http://192.168.254.16/api/data/historical/line/count?element=Line 0&format=json&from={}&to={}&granularity=ONE_HOUR'.format(week_ago,today), headers=headers,auth=HTTPBasicAuth('Admin', 'dimin3421'))

response_North= requests.get('http://10.40.110.200/api/data/historical/zone/inoutcount?element=Lobby - South&format=json&from=2020-12-25T09:00:00&to={}&granularity=ONE_HOUR'.format(today), headers=headers_North,auth=HTTPBasicAuth('Admin', 'pass'))

json_data_N = response_North.json()
print(response_North.content)
