import os
from Purpose_Module import *

path = os.getcwd()+'/csv/consent_purpose/final_product'
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
            csv_dict = parse_updated_csv_purpose(file) #Parse CSV file with function
            print(csv_dict)
            print('========== Updating Purpose Languages ==========')
            api_update_consent_purpose(csv_dict)
