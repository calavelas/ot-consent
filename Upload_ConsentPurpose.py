from App_Module import *

if __name__ == "__main__":
    print('========== Parsing CSV ==========')
    csv_dict = parse_csv_purpose() #Parse CSV file with function
    print('========== Creating Purpose on OneTrust ==========')
    api_create_consent_purpose(csv_dict)
    print('========== Matching new Purpose ID from OneTrust ==========')
    csv_dict = update_csv_purpose(csv_dict) #Add Purpose ID to recently create purpose
    print('========== Updating Purpose Languages ==========')
    api_update_consent_purpose(csv_dict)
    print('========== Save to CSV ==========')
    write_csv_purpose(csv_dict)
