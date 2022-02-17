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
    rec_uri = address.format(archival_object)
    res_record = client.get(rec_uri).json()
    output = open("sample.json", "w")
    output.write(json.dumps(res_record))
    output.close()
    listy = []
    for instance in res_record['instances']:
        selection = False
        top_container = client.get(instance['sub_container']['top_container']['ref']).json()
        if top_container['type'] == "Microfilm":
            print(instance)
            if 'type_3' in instance['sub_container']:
                print("yes, key 3 exists")
                if instance['sub_container']['type_3'] == "Volume":
                    print("yes")
                    selection = True
                    exists = False
                    temp1 = "Volume"
                    temp2 = instance['sub_container']['indicator_3']
                    print(f"checking for microfilm {temp2} in top containers before creating it")
                    response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                    print(response)
                    if response['response']['numFound'] > 0:
                        for widget in response['response']['docs']:
                            if widget['indicator'] == temp2:
                                listy.append({'jsonmodel_type': 'instance', 'instance_type': 'Mixed Materials',
                                              'sub_container': {'jsonmodel_type': 'sub_container',
                                                                'top_container': {'ref': widget['id']}}})
                                exists = True
                                del instance['sub_container']['type_3']
                                del instance['sub_container']['indicator_3']
                    if exists is False:
                        print("this microfilm doesn't exist yet, creating it")
                        current = this_container
                        current['indicator'] = temp2
                        response = client.post('/repositories/2/top_containers', json=this_container)
                        print("created top container, waiting 30 seconds for changes to take effect")
                        time.sleep(30)
                        response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                        print(response)
                        for widget in response['response']['docs']:
                            if widget['indicator'] == temp2:
                                listy.append({'jsonmodel_type': 'instance', 'instance_type': 'Mixed Materials',
                                              'sub_container': {'jsonmodel_type': 'sub_container',
                                                                'top_container': {'ref': widget['id']}}})
                        selection = True
                        del instance['sub_container']['type_3']
                        del instance['sub_container']['indicator_3']
            else:
                print("no third key exists, checking second keys")
            if 'type_2' in instance['sub_container']:
                print("yes, key 2 exists")
                if instance['sub_container']['type_2'] == "Volume":
                    print("yes")
                    selection = True
                    exists = False
                    temp1 = "Volume"
                    temp2 = instance['sub_container']['indicator_2']
                    #temp2 = "2022/008-6"
                    print(f"checking for microfilm {temp2} in top containers before creating it")
                    response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                    print(response)
                    if response['response']['numFound'] > 0:
                        for widget in response['response']['docs']:
                            if widget['indicator'] == temp2:
                                listy.append({'jsonmodel_type': 'instance', 'instance_type': 'Mixed Materials',
                                              'sub_container': {'jsonmodel_type': 'sub_container',
                                                                'top_container': {'ref': widget['id']}}})
                                exists = True
                                del instance['sub_container']['type_2']
                                del instance['sub_container']['indicator_2']
                    if exists is False:
                        print("this microfilm doesn't exist yet, creating it")
                        current = this_container
                        current['indicator'] = temp2
                        response = client.post('/repositories/2/top_containers', json=this_container)
                        print("created top container, waiting 30 seconds for changes to take effect")
                        time.sleep(30)
                        response = (client.get('repositories/2/top_containers/search?q=' + temp2).json())
                        print(response)
                        for widget in response['response']['docs']:
                            if widget['indicator'] == temp2:
                                listy.append({'jsonmodel_type': 'instance', 'instance_type': 'Mixed Materials',
                                              'sub_container': {'jsonmodel_type': 'sub_container',
                                                                'top_container': {'ref': widget['id']}}})
                        selection = True
                        del instance['sub_container']['type_2']
                        del instance['sub_container']['indicator_2']
            else:
                print("no third key exists, checking second keys")
        if selection is True:
            print(listy)
            for item in listy:
                res_record['instances'].append(item)
            response = (client.post(rec_uri, json=res_record)).json()
            print(response)
            res_record = client.get(rec_uri).json()
            output = open("sample.json", "w")
            output.write(json.dumps(res_record))
            output.close()
end = time.asctime()
print(f"all done! Started at {start} and ended at {end}")