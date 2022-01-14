import json
from tqdm import tqdm
from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import pandas as PD

today_date = datetime.datetime.today().strftime('%Y-%m-%d')

logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

logging.setup_logging(filename="aris.log", filemode="a")

client = ASnakeClient()
# create the csv headers
headers = "structure|structure_name|location_label_1|location_label_1_text|location_label_2|location_label_2_text|coordinate_1_label|coordinate_1_text|coordinate_2_label|coordinate_2_text|coordinate_3_label|coordinate_3_text|location_ref"
with open("/media/sf_Documents/locations_list.csv", "a") as w:
    w.write(headers + "\n")
w.close()
def locationater (identifier):
    location = (client.get(f'/locations/{identifier}')).json()
    location.pop('lock_version')
    location.pop('title')
    listy = []
    for key in location.keys():
        listy.append(key)
    x = "|"
    stringy = listy[0] + x + location[listy[0]] + x + listy[1]  + x + location[listy[1]] + x + listy[2] + x + location[listy[2]] + x
    if 'coordinate_1_label' in listy:
        stringy += location['coordinate_1_label'] + x
    else:
        stringy += x
    if 'coordinate_1_indicator' in listy:
        stringy += location['coordinate_1_indicator'] + x
    else:
        stringy += x
    if 'coordinate_2_label' in listy:
        stringy += location['coordinate_2_label'] + x
    else:
        stringy += x
    if 'coordinate_2_indicator' in listy:
        stringy += location['coordinate_2_indicator'] + x
    else:
        stringy += x
    if 'coordinate_3_label' in listy:
        stringy += location['coordinate_3_label'] + x
    else:
        stringy += x
    if 'coordinate_3_indicator' in listy:
        stringy += location['coordinate_3_indicator'] + x
    else:
        stringy += x
    stringy += location['uri']
    with open("/media/sf_Documents/locations_list.csv", "a") as w:
        w.write(stringy + "\n")
    w.close()
locations = (client.get('/locations', params={'all_ids': True})).json()
for item in tqdm(locations):
    locationater(item)
# change from a pipe-delimited to a comma separated for better compatibility
df = PD.read_csv("/media/sf_Documents/locations_list.csv", dtype=object, delimiter="|")
writer = df.to_csv("/media/sf_Documents/locations_list2.csv", index=False)
print("all done")
#this_container = json.dumps(this_container)
#response = client.post('/repositories/2/top_containers', json=this_container)
#print(this_container)
#print(response.status_code)