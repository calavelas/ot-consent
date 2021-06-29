import requests
from Setting import client_id,client_secret,site_url

def api_get_token():
    #API Call
    #Get token from client_id and Secret
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

if __name__ == '__main__':
    print(api_get_token())