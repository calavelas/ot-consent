import os
from Purpose_Module import *

path = os.getcwd()+'/csv/consent_purpose/initial'
dir = os.listdir(path)

if __name__ == "__main__":
    print('Verify a List of Files')
    for file in dir:
        print(file)
    verify = input('Press "Y" to Proceed : ')
    if verify == 'Y':
        for file in dir:
            print('========== Parsing CSV ==========')
            print('File name : ' +file)
            csv_dict = parse_csv_purpose(file) #Parse CSV file with function
            print('========== Creating Purpose on OneTrust ==========')
            api_create_consent_purpose(csv_dict)
            print('========== Matching new Purpose ID from OneTrust ==========')
            csv_dict = update_csv_purpose(csv_dict) #Add Purpose ID to recently create purpose
            print('========== Updating Purpose Languages ==========')
            api_update_consent_purpose(csv_dict)
            print('========== Save to CSV ==========')
            write_csv_purpose(csv_dict,file)
            print('save to txt')
            write_json_purpose(csv_dict,file)
