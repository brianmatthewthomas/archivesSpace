from asnake.client import ASnakeClient
import asnake.logging as logging
import datetime
import pandas as PD
import json
import time
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')

#logging.setup_logging(filename="../../.config/JetBrains/PyCharmCE2021.3/scratches/aris.log", filemode="a")
def row_converter(row=tuple, listy=list, verbose=True):
    #convert pandas row to a dictionary
    #requires a list of columns and a row as a tuple
    count = 1
    pictionary = {}
    pictionary['Index'] = row[0]
    for item in listy:
        pictionary[item] = row[count]
        count += 1
    if verbose is True:
        print(pictionary)
    return pictionary

spreadsheet = "/media/sf_Documents/top_container_changes.xlsx"
df = PD.read_excel(spreadsheet, dtype=object)
listy = df.columns

title_dict = {}
for row in df.itertuples():
    valuables = row_converter(row, listy, verbose=False)
    title_dict[valuables['Old Top Container Indicator']] = [valuables['New top container indicator'], valuables['identifier']]
print(title_dict)
start_up = input("press enter to continue")
client = ASnakeClient()
responses = (client.get('repositories/2/top_containers?all_ids=True').json())
print(responses)
'''
responses2 = responses['response']['docs']
for response in responses2:
    if "223-" in response['title']:
        container = client.get(response['id']).json()
        indicator = container['indicator']
        if indicator.startswith("223-"):
            print(container['indicator'])
            temp = container['indicator']
            temp2 = temp.split("-")[1]
            while len(temp2) < 4:
                temp2 = "0" + temp2
            temp = temp.replace(temp.split("-")[1], temp2)
            print(temp)
            container['indicator'] = temp
            submission = client.post(container['uri'], json=container).json()
            print(f"update status: {submission}")
'''
counter = 0
for key in title_dict.keys():
    ref = title_dict[key][-1]
    container = client.get(f"repositories/2/top_containers/{ref}").json()
    if container['indicator'] in title_dict.keys():
        print(container)
        old = container['indicator']
        new_indicator = title_dict[container['indicator']][0]
        print(container['indicator'])
        print(new_indicator)
        container['indicator'] = new_indicator
        submission = client.post(container['uri'], json=container).json()
    '''
    if "type" in container:
        if container['type'] == "Reel":
            container['type'] = "Microfilm"
            container['container_profile'] = {}
            container['container_profile']['ref'] = '/container_profiles/9'
            submission = client.post(response['ref'], json=container).json()
            print(container)
            print("update status:",submission)
            counter += 1
    output = open("./sample.json", "w")
    output.write(json.dumps(response))
    output.close()
print(counter,"items updated")
    '''