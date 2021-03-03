from APP_Module import *

if __name__ == "__main__":
    pprint.pprint('========== Parsing CSV ==========')
    CSV = Parse_CSV() #Parse CSV file with function
    pprint.pprint('========== Creating Purpose on OneTrust ==========')
    Create_Result = Create_Purpose(CSV)
    pprint.pprint('========== Matching new Purpose ID from OneTrust ==========')
    Updated_CSV = Update_CSV_PurposeID(CSV) #Add Purpose ID to recently create purpose
    pprint.pprint('========== Updating Purpose Languages ==========')
    Update_Purpose_Result = API_Update_Purpose(Updated_CSV)
    pprint.pprint('========== Save to CSV Result ==========')
    Write_CSV(Updated_CSV)
