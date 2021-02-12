import csv
import requests
import pprint
import json
import os

#CIMB
clientId = os.environ.get("MSC_clientId")
clientSecret = os.environ.get("MSC_clientSecret")
SITE_URL = 'https://app-apac.onetrust.com'

print(clientId)
#CSV File Enviroment Variable
File_Name = 'msc_apidemo_purpose.csv'

def Get_Token():
    #Get token from clientId and Secret
    payload = {
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret
    }
    request_url = f'{SITE_URL}/api/access/v1/oauth/token'
    respond = requests.post(request_url, params=payload)
    respond_json = respond.json()
    accessToken = respond_json['access_token']
    return(accessToken)

def Get_Purpose():
    #Get Purpose List from OneTrust
    accessToken = Get_Token()
    headers = {
        'Authorization': f'Bearer {accessToken}'
    }
    payload = {
        'size':'200', #Default was 20 which is not enough
        'latestVersion': 'true' #Not sure if this needed
    }
    request_url = f'{SITE_URL}/api/consentmanager/v2/purposes/'
    respond = requests.get(request_url, headers=headers, params=payload)
    respond_json = respond.json()
    return respond_json

def Parse_CSV():
    # Parse CSV File to build JSON format for API
    CSV_Purpose = []
    with open(f'csv/{File_Name}', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            CSV_Purpose.append(
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
    return CSV_Purpose

def Create_Purpose(CSV):
    # Call API to create purpose from CSV file
    respond_list = []
    accessToken = Get_Token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}'
    }
    request_url = f'{SITE_URL}/api/consentmanager/v1/purposes'
    for items in CSV:
        payload = items
        respond = requests.post(request_url, headers=headers, data=json.dumps(payload))
        respond_json = respond.json()
        respond_list.append(respond_json)
    return respond_list

def Update_CSV_PurposeID(Parsed_CSV):
    # Get recently created consent id from API and Update to the purpose
    Purpose_List = Get_Purpose() #Get CSV List from API
    for purpose in Parsed_CSV:
        for content in Purpose_List['content']:
            if purpose['Name'] in content['versions'][0]['label']: #Match Purpose ID of recently created purpose to existing data
                purpose['purposeId'] = content['purposeId']
                purpose['Label'] = content['versions'][0]['label']
                purpose['Version'] = content['versions'][0]['version']
                purpose['Status'] = content['versions'][0]['status']
    return Parsed_CSV

def API_Update_Purpose(Updated_CSV):
    # Update recently created purpose with API from Updated CSV (with ID)
    respond_list = []
    accessToken = Get_Token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}'
    }
    for items in Updated_CSV:
        purposeId = items['purposeId']
        request_url = f'{SITE_URL}/api/consentmanager/v1/purposes/{purposeId}'
        payload = items
        respond = requests.put(request_url, headers=headers, data=json.dumps(payload)) #Data have to be sent in JSON format
        respond_json = respond.json()
        respond_list.append(respond_json)
    return respond_list

def Write_Update_CSV(CSV):
    pass

if __name__ == "__main__":
    CSV = Parse_CSV() #Parse CSV file with function
    pprint.pprint('========== Parse CSV ==========')
    pprint.pprint('Name | Organization')
    for item in CSV:
        print(item['Name']+' | '+ item['Organizations'][0])
    Create_Result = Create_Purpose(CSV)
    pprint.pprint('========== Create Result ==========')
    pprint.pprint(Create_Result)
    Updated_CSV = Update_CSV_PurposeID(CSV) #Add Purpose ID to recently create purpose
    #pprint.pprint(Updated_CSV)
    Update_Purpose_Result = API_Update_Purpose(Updated_CSV)
    pprint.pprint('========== Update Result ==========')
    pprint.pprint(Update_Purpose_Result)



