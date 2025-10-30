import pandas as pd
from tqdm import tqdm
from copy import deepcopy
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import pandas as PD
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")

client = ASnakeClient()

def row_converter(row, listy):
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = str(row[count])
        count += 1
    print(pictionary)
    return pictionary

spreadsheet = input("excel filename to parse: ")
datea = input("today as YYYY-MM-DD: ")

accession_dict = {}

this_container = {'jsonmodel_type': 'top_container',
                  'active_restrictions': [],
                  'series': [],
                  'collection': [],
                  'indicator': 'turkey-002',
                  'type': 'Box',
                  'barcode': '',
                  'repository': {'ref': '/repositories/2'},
                  'restricted': 'false',
                  'container_profile': {'ref': '/container_profiles/3'},
                  'container_locations': [{'ref': '/locations/2960', 'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': f'{datea}'}]}

df = pd.read_excel(spreadsheet)
listy = df.columns
accession_counter = 0
accession_name = ""
barcode = ""
for row in df.itertuples():
    valuables = row_converter(row, listy)
    current_container = this_container
    current_container['container_locations'][0]['ref'] = valuables['location_uuid']
    current_container['indicator'] = valuables['Box_number']
    if barcode != valuables['SRC_Barcodes']:
        current_container['barcode'] = valuables['SRC_Barcodes']
        barcode = valuables['SRC_Barcodes']
    if current_container['barcode'].endswith(".0"):
        current_container['barcode'] = current_container['barcode'][:-2]
    accession_id = valuables['accession_uuid']
    if accession_name != accession_id:
        accession_name = accession_id
        accession_counter = 0
    if accession_counter <= 199:
        current_container['series'].append({'ref': accession_id, 'jsonmodel_type':'accession'})
        accession_counter += 1
    if accession_counter >= 200:
        accession_counter +=1
    endpoint = '/repositories/2/top_containers'
    print(current_container)
    response = client.post(endpoint, json=current_container).json()
    print(f'{response}')
    current_container['barcode'] = ""
    new_ref = response['uri']
    if accession_id not in accession_dict.keys():
        accession_dict[accession_id] = []
    accession_dict[accession_id].append(new_ref)

my_list = accession_dict.keys()
for accession in my_list:
    print(accession)
    if len(accession_dict[accession]) <= 200:
        temp = client.get(f'/repositories/2/{accession}').json()
        print(temp)
        if "instances" not in temp.keys():
            temp['instances'] = []
        for item in accession_dict[accession]:
            temp['instances'].append({"jsonmodel_type": "instance", "instance_type": "mixed_materials",
                                      "sub_container": {"jsonmodel_type": "sub_container", "top_container": {"ref": item}}})
        print(temp)
        temp2 = client.post(f'/repositories/2/{accession}', json=temp)
        print(temp2)
