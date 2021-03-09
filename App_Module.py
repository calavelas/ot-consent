import csv
import requests
import pprint
import json
import os
import datetime
from Setting import *

def api_get_token():
    #API Call
    #Get token from client_id and Secret
    now = datetime.datetime.now()
    request_payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    request_url = f'{site_url}/api/access/v1/oauth/token'
    respond = requests.post(request_url, params=request_payload)
    respond_json = respond.json()
    if 'error' in respond_json:
            print(str(now)+' : Get Token Error | '+respond_json['error'] +' | ' +respond_json['error_description']) #Print Error Message
    access_token = respond_json['access_token']
    return(access_token)

def api_get_purpose_list():
    #API Call
    #Get Purpose List from OneTrust
    access_token = api_get_token()
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    request_payload = {
        'size':'200', #Default was 20 which is not enough
        'latestVersion': 'true' #Not sure if this needed
    }
    request_url = f'{site_url}/api/consentmanager/v2/purposes/'
    respond = requests.get(request_url, headers=headers, params=request_payload)
    respond_json = respond.json()
    purpose_list = respond_json
    return purpose_list

def parse_csv_purpose():
    #Parse CSV File to build JSON format for API
    purpose_csv = []
    now = datetime.datetime.now()
    with open(f'csv/consent_purpose/{consent_file_name}', mode='r') as csv_file:
        csv_dict = csv.DictReader(csv_file)
        for row in csv_dict:
            purpose_csv.append(
                {
                    "Name": row['\ufeffName'],
                    "DefaultLanguage": row['DefaultLanguage'],
                    "Description": row['Description'],
                    "ConsentLifeSpan": row['ConsentLifeSpan'],
                    "Organizations": [
                        row['Organizations']
                    ], #API Require this field as list
                    "Languages":[
                        {
                            'Language': row['Language1'],
                            'Name': row['NameLanguage1'],
                            'Default': row['DefaultLanguage1'].lower(),
                            'Description': row['DescriptionLanguage1']
                        },
                        {
                            'Language': row['Language2'],
                            'Name': row['NameLanguage2'],
                            'Default': row['DefaultLanguage2'].lower(),
                            'Description': row['DescriptionLanguage2']
                        }
                    ]
                }
            )
    print('Parsed Result')
    for item in purpose_csv:
        print(str(now)+' : '+'Parsed! | Purpose Name : '+item['Name']+ ' |' + ' Organizations : '+item['Organizations'][0])
    return purpose_csv

def api_create_consent_purpose(purpose_csv):
    #API Call
    #Create purpose from parsed CSV file
    create_consent_purpose_result = []
    now = datetime.datetime.now()
    access_token = api_get_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    request_url = f'{site_url}/api/consentmanager/v1/purposes'
    for item in purpose_csv:
        request_payload = item
        respond = requests.post(request_url, headers=headers, data=json.dumps(request_payload))
        respond_json = respond.json()
        create_consent_purpose_result.append(respond_json)
    print('Purpose Created Result')
    for item in create_consent_purpose_result:
        if 'message' in item:
            print(str(now)+' : '+item['message']) #Print Error Message
        else:
            print(str(now)+' : '+'Created! | Purpose Name : '+item['Label']+ ' |' + ' ID : '+item['Id']+ ' |' ' Status : '+item['Status']) #Print Success Message + Items


def update_csv_purpose(purpose_csv):
    # Get recently created consent id from API and Update to the purpose
    purpose_list = api_get_purpose_list() #Get CSV List from API
    for purpose in purpose_csv:
        for content in purpose_list['content']:
            if purpose['Name'] in content['versions'][0]['label']: #Match Purpose ID of recently created purpose to existing data
                purpose['purposeId'] = content['purposeId']
                purpose['Label'] = content['versions'][0]['label']
                purpose['Version'] = content['versions'][0]['version']
                purpose['Status'] = content['versions'][0]['status']
    return purpose_csv

def api_update_consent_purpose(purpose_csv):
    # Update recently created purpose with API from Updated CSV (with ID)
    update_consent_purpose_result = []
    now = datetime.datetime.now()
    access_token = api_get_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    for items in purpose_csv:
        purposeId = items['purposeId']
        request_url = f'{site_url}/api/consentmanager/v1/purposes/{purposeId}'
        request_payload = items
        respond = requests.put(request_url, headers=headers, data=json.dumps(request_payload)) #Data have to be sent in JSON format
        respond_json = respond.json()
        update_consent_purpose_result.append(respond_json)
    print('Updated Result')
    for item in update_consent_purpose_result:
        if 'message' in item:
            print(str(now)+' : '+item['message'])
        else:
            print(str(now)+' : '+'Updated! | Purpose Name : '+item['Label']+ ' |' + ' ID : '+item['Id']+ ' |' ' Status : '+item['Status'])

def write_csv_purpose(purpose_csv):
    now = datetime.datetime.now()
    with open('csv/consent_purpose/'+'updated_'+consent_file_name, 'w',encoding="utf-8") as csv_file:
        csv_dict = csv.DictWriter(csv_file, purpose_csv[0].keys())
        csv_dict.writeheader()
        for item in purpose_csv:
            csv_dict.writerow(item)
    print('Save to CSV File Result')
    print(str(now)+' : '+f'Saved to CSV file Complete!, File Name >> updated_{consent_file_name}')




