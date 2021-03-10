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

response_North= requests.get('http://10.40.110.200/api/data/historical/zone/inoutcount?element=Lobby - South&format=json&from=2020-12-25T09:00:00&to={}&granularity=ONE_HOUR'.format(today), headers=headers_North,auth=HTTPBasicAuth('Admin', 'pass'))

json_data_N = response_North.json()
print(response_North.content)
#parse the json data
times_N=[]

in_number_N=[]
out_number_N=[]

for result1 in json_data_N['content']['element'][0]['measurement']:
    times_N.append(result1['from'])
for results2 in json_data_N['content']['element'][0]['measurement']:
    in_number_N.append(results2['value'][0]['value'])
for results3 in json_data_N['content']['element'][0]['measurement']:
    out_number_N.append(results3['value'][1]['value'])

#get data for counting
response_North2= requests.get('http://10.40.110.200/api/data/historical/line/count?element=Line 1&format=json&from=2020-12-25T09:00:00&to={}&granularity=ONE_HOUR'.format(today), headers=headers_North,auth=HTTPBasicAuth('Admin', 'pass'))
json_data_N2 = response_North.json()
print(response_North2.content)

time_N=[]
count_N=[]
for result in json_data_N2['content']['element'][0]['measurement']:
    time_N.append(result['from'])
    #print('Counts from{} to to{}'.format(result['from'], result['to']))
    for counts in result['value']:
        for val in counts.values():
            count_N.append(val)
        #print('\t{}:{}'.format(counts['label'], counts['value']))
counts_N=[]
for e in count_N:
    #ifinstance(e,int)
    try:
        counts_N.append(int(e))
    except ValueError:
        pass

#dwell data

response_all_N = requests.get('http://10.40.110.200/api/data/historical/zone/dwell/summary?element=Lobby - South&format=json&from=2020-12-25T09:00:00&to={}&granularity=ONE_HOUR'.format(today), headers=headers_North,auth=HTTPBasicAuth('Admin', 'pass'))
ja_data_N=response_all_N.json()
print(response_all_N.content)

stat_all_N=[]
counts_all_N=[]

for results2 in ja_data_N['content']['element'][0]['measurement']:
    stat_all_N.append(results2['value'][0]['value'])
for results in ja_data_N['content']['element'][0]['measurement']:
    counts_all_N.append(results2['value'][1]['value'])
    
#make the data into pandas data frames
    
import pandas as pd
#pandas.set_option('display.max_rows')
data_S = pd.DataFrame(times_N, columns=['Time_N'])
data_S['Counts_line_N']= pd.DataFrame(counts_N)
data_S['Counts_zone_N']= pd.DataFrame(in_number_N)
data_S['Counts_dwell_N']= pd.DataFrame(counts_all_N)
data_S['Stat_N']= pd.DataFrame(stat_all_N)
data_S = data_S.fillna(0)

#export to gsheets

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

#change this by your sheet ID
SAMPLE_SPREADSHEET_ID_input = '1vFwTLvu59RxhQf8vPMnerjBCF2Xn9XP9gHf6Ha2lqOo'

#change the range if needed
SAMPLE_RANGE_NAME = 'A:E'

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    global service
    SCOPES = [scope for scope in scopes[0]]
    #print(SCOPES)
    
    cred = None

    if os.path.exists('token_write.pickle'):
        with open('token_write.pickle', 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open('token_write.pickle', 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        #return service
    except Exception as e:
        print(e)
        #return None
        
# change 'my_json_file.json' by your downloaded JSON file.
Create_Service('credentials.json', 'sheets', 'v4',['https://www.googleapis.com/auth/spreadsheets'])
    
def Export_Data_To_Sheets():
    
    response_date = service.spreadsheets().values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
        valueInputOption='RAW',
        range=SAMPLE_RANGE_NAME,
        body=dict(
            majorDimension='ROWS',
            values=data_S.values.tolist())
    ).execute()
    print('Sheet successfully Updated')

Export_Data_To_Sheets()

#export to aws athena 
"""
