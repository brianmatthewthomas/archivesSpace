import pandas as PD
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import time

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

myTime = time.asctime()
post_back = {}
container_profiles = {'Capitol drawings cabinet drawer (434-445)':'/container_profiles/11',
                      'Card file box A':'/container_profiles/21',
                      'Card file box B':'/container_profiles/22',
                      'Card file box C':'/container_profiles/23',
                      'Card file box D':'/container_profiles/24',
                      'Card file box E':'/container_profiles/25',
                      'Card file double drawer A':'/container_profiles/29',
                      'Card file double drawer B':'/container_profiles/30',
                      'Card file double drawer C':'/container_profiles/31',
                      'Card file double drawer D':'/container_profiles/32',
                      'Half RS':'/container_profiles/20',
                      'LittleMS':'/container_profiles/2',
                      'Map drawer A (51-70, 81-100)':'/container_profiles/12',
                      'Map drawer B (1-5, 26-30, 136-165, 196-210)':'/container_profiles/13',
                      'Map drawer C (71-80)':'/container_profiles/14',
                      'Map drawer D (31-50, 101-135, 166-195, 211-413)':'/container_profiles/15',
                      'Map drawer E (6-25, 141-160)':'/container_profiles/16',
                      'Microfilm':'/container_profiles/9',
                      'MS':'/container_profiles/1',
                      'Oversize 12x18':'/container_profiles/26',
                      'Oversize 15x19':'/container_profiles/27',
                      'Oversize 16x20':'/container_profiles/4',
                      'Oversize 21x25':'/container_profiles/17',
                      'Oversize 23x31':'/container_profiles/18',
                      'Oversize 24x36':'/container_profiles/19',
                      'Public debt':'/container_profiles/28',
                      'RS':'/container_profiles/3',
                      'Volume':'/container_profiles/33',
                      'Film container': '/container_profiles/37'}
baseline = {'jsonmodel_type': 'top_container',
                  'active_restrictions': [],
                  'series': [],
                  'collection': [],
                  'indicator': 'turkey-002',
                  'type': 'Box',
                  'barcode': '',
                  'repository': {'ref': '/repositories/2'},
                  'restricted': 'false',
                  'container_profile': {'ref': ''},
                  'container_locations': [{'ref': '', 'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': '2021-11-09'}]}
df1 = PD.read_excel("C:/Users/bthomas/Documents/topContainer_csv_zavala_2026017.xlsx", sheet_name="Sheet1", dtype=object)
print(df1[:5])
df2 = PD.read_csv("K:/1_Working/research/archivespace/locations_list2.csv", dtype=object)
print(df2[:5])
df3 = df1.merge(df2, how='left', on=['structure_name','location_label_1_text','location_label_2_text','coordinate_1_label','coordinate_1_text','coordinate_2_label','coordinate_2_text','coordinate_3_label','coordinate_3_text'])
print(df3[:])
listy = df3.columns
for row in df3.itertuples():
    valuables = row_converter(row, listy)
    thisContainer = baseline
    thisContainer['indicator'] = valuables['Box or container number']
    thisContainer['type'] = valuables['Container type']
    thisContainer['container_profile']['ref'] = container_profiles[valuables['container profile']]
    if valuables['structure_name'] == 'Zavala' or valuables['repository'] == 'Lorenzo de Zavala' or valuables['structure_name'] == 'State Records Center':
        thisContainer['repository']['ref'] = '/repositories/2'
    if valuables['structure_name'] == 'Sam Houston Center':
        thisContainer['repository']['ref'] = '/repositories/11'
    if valuables['repository'] == "Review":
        thisContainer['repository']['ref'] = '/repositories/12'
    if str(valuables['repository']) != 'nan' and str(valuables['type of linked record']) != 'nan' and str(valuables['id_number']) != 'nan':
        collectionString = thisContainer['repository']['ref'] + "/" + valuables['type of linked record'] + "/" + str(valuables['id_number'])
        if collectionString not in post_back.keys():
            post_back[collectionString] = []
        thisContainer['series'] = []
        thisContainer['series'].append({'ref': collectionString, 'jsonmodel_type':valuables['type of linked record']})
    if str(valuables['location_ref']) != 'nan':
        thisContainer['container_locations'][0]['ref'] = valuables['location_ref']
    if str(valuables['location_ref']) == 'nan':
        thisContainer['container_locations'] = []
    print(thisContainer)
    endpoint = thisContainer['repository']['ref'] + "/top_containers"
    response = client.post(endpoint, json=thisContainer).json()
    post_back[collectionString].append(response['uri'])
    print(response)
print("waiting 30 seconds for the containers to register in the system")
time.sleep(30)
listy = post_back.keys()
for thing in listy:
    temp = client.get(thing).json()
    if "instances" not in temp.keys():
        temp['instances'] = []
    for item in post_back[thing]:
        temp['instances'].append({'jsonmodel_type': 'instance', 'instance_type': 'mixed_materials',
                                  'sub_container': {'jsonmodel_type': 'sub_container', 'top_container': {'ref': item}}})
    temp2 = client.post(thing, json=temp)
    print(temp2.status_code)
print("all done")

'''
print("waiting 30 seconds for changes to take effect")
time.sleep(30)
listy = post_back.keys()
for thing in listy:
    temp = (client.get(thing)).json()
    temp_list = thing.split("/")
    endpoint = "/" + temp_list[1] + "/" + temp_list[2] + "/top_containers"
    for item in post_back[thing]:
        response = (client.get(endpoint + "/search?q=" + item).json())
        print(response['response']['docs'])
        # add switch to ensure multiple containers of the same name aren't paired multiple times
        my_match = False
        while my_match is False:
            for widget in response['response']['docs']:
                typee = f"{widget['type_u_ssort']} "
                my_string = widget['display_string'].replace(typee, '')
                if my_string == item and my_match is False:
                    temp['instances'].append({'jsonmodel_type': 'instance', 'instance_type': 'mixed_materials',
                                              'sub_container':{'jsonmodel_type': 'sub_container','top_container':{'ref':widget['id']}}})
                    print(f"found match for {widget['id']}")
                    my_match = True
    temp2 = (client.post(thing, json=temp))
    print(temp)
    print(temp2.status_code)
yourTime = time.asctime()
print(f"process started at {myTime} and completed at {yourTime}")
'''

