import sys

from tqdm import tqdm
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import json
import time
start = time.asctime()
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")
item_log = open("/home/brian/itemlog.txt", "a")
item_log.close()
itemlog = []
with open("/home/brian/itemlog.txt", "r") as r:
    for line in r:
        itemlog.append(line[:-1])
item_log = open("/home/brian/itemlog.txt", "a")
this_container = {'jsonmodel_type': 'top_container',
                  'active_restrictions': [],
                  'series': [],
                  'collection': [],
                  'indicator': 'turkey-002',
                  'type': 'Volume',
                  'barcode': '',
                  'repository': {'ref': '/repositories/2'},
                  'restricted': 'false',
                  'container_profile': {},
                  'container_locations': []}

client = ASnakeClient()

archival_objects = (client.get("repositories/2/archival_objects", params={'all_ids': True})).json()
#print(archival_objects)
address = f'repositories/2/archival_objects/' + "{0}"
for archival_object in tqdm(archival_objects):
    selection = False
    if str(archival_object) not in itemlog:
        rec_uri = address.format(archival_object)
        res_record = client.get(rec_uri).json()
        # output = open("sample.json", "w")
        # output.write(json.dumps(res_record))
        # output.close()
        listy = []
        for instance in res_record['instances']:
            #print(instance)
            if 'type_3' in instance['sub_container']:
                if instance['sub_container']['type_3'] == "Volume":
                    print("yes, applicable key 3 exists")
                    print("with archival object url",res_record['uri'])
                    top_container = client.get(instance['sub_container']['top_container']['ref']).json()
                    if top_container['type'] == "Microfilm":
                        print("yes, microfilm is the top container; with name",top_container['display_string'],"at",time.asctime())
                        selection = True
                        exists = False
                        temp1 = "Volume"
                        temp2 = instance['sub_container']['indicator_3']
                        temp3 = temp1 + " " + temp2
                        print(f"checking for {temp3} in top containers before creating it")
                        response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                        #print(response)
                        if response['response']['numFound'] > 0:
                            for widget in response['response']['docs']:
                                if widget['title'] == temp3:
                                    listy.append({'jsonmodel_type': 'instance', 'instance_type': 'mixed_materials',
                                                  'sub_container': {'jsonmodel_type': 'sub_container',
                                                                    'top_container': {'ref': widget['id']}}})
                                    exists = True
                                    selection = True
                                    try:
                                        del instance['sub_container']['type_3']
                                        del instance['sub_container']['indicator_3']
                                    except:
                                        continue
                        if exists is False:
                            print("this microfilm doesn't exist yet, creating it")
                            current = this_container
                            current['indicator'] = temp2
                            response = client.post('/repositories/2/top_containers', json=this_container)
                            print("created top container, waiting 30 seconds for changes to take effect")
                            time.sleep(30)
                            response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                            #print(response)
                            for widget in response['response']['docs']:
                                if widget['title'] == temp3:
                                    listy.append({'jsonmodel_type': 'instance', 'instance_type': 'mixed_materials',
                                                  'sub_container': {'jsonmodel_type': 'sub_container',
                                                                    'top_container': {'ref': widget['id']}}})
                                    selection = True
                                    try:
                                        del instance['sub_container']['type_3']
                                        del instance['sub_container']['indicator_3']
                                    except:
                                        continue
            if 'type_2' in instance['sub_container']:
                if instance['sub_container']['type_2'] == "Volume":
                    print("yes, applicable key 2 exists")
                    print("with archival object url",res_record['uri'])
                    #print(instance)
                    top_container = client.get(instance['sub_container']['top_container']['ref']).json()
                    if top_container['type'] == "Microfilm":
                        print("yes, microfilm is the top container; with name",top_container['display_string'],"at",time.asctime())
                        exists = False
                        temp1 = "Volume"
                        temp2 = instance['sub_container']['indicator_2']
                        temp3 = temp1 + " " + temp2
                        #temp2 = "2022/008-6"
                        print(f"checking for {temp3} in top containers before creating it")
                        response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                        #print(response)
                        if response['response']['numFound'] > 0:
                            for widget in response['response']['docs']:
                                if widget['title'] == temp3:
                                    listy.append({'jsonmodel_type': 'instance', 'instance_type': 'mixed_materials',
                                                  'sub_container': {'jsonmodel_type': 'sub_container',
                                                                    'top_container': {'ref': widget['id']}}})
                                    exists = True
                                    selection = True
                                    try:
                                        del instance['sub_container']['type_2']
                                        del instance['sub_container']['indicator_2']
                                    except:
                                        continue
                        if exists is False:
                            print("this microfilm doesn't exist yet, creating it")
                            current = this_container
                            current['indicator'] = temp2
                            response = client.post('/repositories/2/top_containers', json=this_container)
                            print("created top container, waiting 30 seconds for changes to take effect")
                            time.sleep(30)
                            response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                            #print(response)
                            for widget in response['response']['docs']:
                                if widget['title'] == temp3:
                                    listy.append({'jsonmodel_type': 'instance', 'instance_type': 'mixed_materials',
                                                  'sub_container': {'jsonmodel_type': 'sub_container',
                                                                    'top_container': {'ref': widget['id']}}})
                                    selection = True
                                    try:
                                        del instance['sub_container']['type_2']
                                        del instance['sub_container']['indicator_2']
                                    except:
                                        continue
        if selection is True:
            print(listy)
            if listy != []:
                for item in listy:
                    res_record['instances'].append(item)
                response = (client.post(rec_uri, json=res_record)).json()
                print(response)
                res_record = client.get(rec_uri).json()
                output = open("sample.json", "w")
                output.write(json.dumps(res_record))
                output.close()
                item_log.write(str(archival_object) + "\n")
            else:
                sys.exit()
        else:
            item_log.write(str(archival_object) + "\n")
item_log.close()
end = time.asctime()
print(f"all done! Started at {start} and ended at {end}")