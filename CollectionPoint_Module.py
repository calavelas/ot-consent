import requests
import datetime
import csv
import json
import pprint
from GetToken_Module import api_get_token
from Setting import site_url

def parse_csv_collection_point(collection_point_csv_file):
    #Parse CSV File to build JSON format for API
    collection_point_csv = []
    now = datetime.datetime.now()
    with open(f'csv/collection_point/initial/{collection_point_csv_file}', mode='r') as csv_file:
        csv_dict = csv.DictReader(csv_file)
        for row in csv_dict:
            row_dict = {
                "Name": row['\ufeffName'],
                "CollectionPointType": row['CollectionPointType'],
                "ConsentType": row['ConsentType'],
                "SubjectIdentifier": row['Identifier'],
                #"DataElements": row['DataElements'].split(',\n'),
                "Description": row['Description'],
                "DoubleOptIn": row.get('DoubleOptIn', 'false').lower(),
                "NoConsentTransactions": row.get('NotGiven', 'false').lower(),
                "PurposeIds": row['PurposeID'].split(',\n'),
                "Language": row['Language'],
                "OrganizationId": row['Organizations']
                }
            empty_key = {key: value for key, value in row_dict.items() if value == ""} #check empty key in dict
            for key in empty_key:
                del row_dict[key] #delete empty value key from dict
            collection_point_csv.append(row_dict)
    print('Parsed Result')
    for item in collection_point_csv:
        print(str(now)+' : '+'Parsed! | Collection Point Name : '+item['Name']+ ' |' + ' Organizations : '+item['OrganizationId'])
        pprint.pprint(item)
    return collection_point_csv

def api_create_collection_point(collection_point_csv):
    create_collection_point_result = []
    now = datetime.datetime.now()
    access_token = api_get_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    request_url = f'{site_url}/api/consentmanager/v1/collectionpoints'
    for item in collection_point_csv:
        request_payload = item
        respond = requests.post(request_url, headers=headers, data=json.dumps(request_payload))
        respond_json = respond.json()
        create_collection_point_result.append(respond_json)
    pprint.pprint(create_collection_point_result)
    print('Collection Point Created Result')
    for item in create_collection_point_result:
        if 'message' in item:
            print(str(now)+' : '+item['message']) #Print Error Message
        else:
            print(str(now)+' : '+'Created! | Collection Point Name : '+item['Name']+ ' |' + ' ID : '+item['Id']+ ' |' ' Status : '+item['Status']) #Print Success Message + Items

def api_get_collection_point_list():
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
    request_url = f'{site_url}/api/consentmanager/v1/collectionpoints'
    respond = requests.get(request_url, headers=headers, params=request_payload)
    respond_json = respond.json()
    purpose_list = respond_json
    return purpose_list

def update_csv_collection_point(collection_point_csv):
    # Get recently created consent id from API and Update to the purpose
    purpose_list = api_get_purpose_list() #Get OT Purpose List from API
    for purpose in purpose_csv:
        for content in purpose_list['content']:
            if purpose['Name'] in content['versions'][0]['label']: #Match Purpose ID of recently created purpose to existing data
                purpose['purposeId'] = content['purposeId']
                purpose['Label'] = content['versions'][0]['label']
                purpose['Version'] = content['versions'][0]['version']
                purpose['Status'] = content['versions'][0]['status']
    return purpose_csv