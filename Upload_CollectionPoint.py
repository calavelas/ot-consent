import os
import pprint
from CollectionPoint_Module import *


path = os.getcwd()+'/csv/collection_point/initial'
dir = os.listdir(path)

for file in dir:
    #collection_point_list = api_get_collection_point_list()
    #pprint.pprint(collection_point_list)
    csv = parse_csv_collection_point(file)
    api_create_collection_point(csv)
